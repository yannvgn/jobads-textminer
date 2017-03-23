from jobads import config
from gensim.models import Word2Vec
import pickle
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
import sklearn.manifold

nltk.data.path.append(config['nltk']['data'])

# The model is loaded only once. Restart the server to reload it.
# TODO : the model should periodically be trained by the server.
ads_word2vec_model = Word2Vec.load(config['ads_word2vec']['trained_model'])

# Idem
with open(config['skills']['tokenized_skills_by_nb_words'], 'rb') as f:
    tokenizedSkillsByNbWords = pickle.load(f)


def extract_skills_from_cv(text_content, lang='french', window=10, limit=10):
    text_content = re.sub(r'-+page \(\d+\) break-+', '', text_content.lower())

    tokens = [x for x in nltk.word_tokenize(text_content, lang) if x not in stopwords.words(lang)]

    skillOccurrences = {}
    usedOccurrences = []
    for key in sorted(tokenizedSkillsByNbWords, reverse=True):
        ngrams = list(nltk.ngrams(tokens,key))
        for skill in tokenizedSkillsByNbWords[key]:
            indices = []
            for index, sk in enumerate(ngrams):
                if sk == skill and not index in usedOccurrences:
                    indices.append(index)
                    usedOccurrences += range(index, index+key)
            if indices:
                skillOccurrences[skill] = indices

    results = {}
    for skill in skillOccurrences:
        closeSkillsCounter = 0
        for occurrence in skillOccurrences[skill]:
            localCloseSkillsCounter = 0
            for otherSkill in skillOccurrences:
                if otherSkill != skill:
                    for otherOccurrence in skillOccurrences[otherSkill]:
                        if abs(occurrence-otherOccurrence) <= window:
                            localCloseSkillsCounter+=1
                            break
            if localCloseSkillsCounter > closeSkillsCounter:
                closeSkillsCounter = localCloseSkillsCounter
            #closeSkillsCounter += localCloseSkillsCounter
        #closeSkillsCounter /= len(skillOccurrences[skill])
        #closeSkillsCounter /= ' '.join(tokens).count(' '.join(skill))
        results[' '.join(skill)] = closeSkillsCounter
    
    sortedResult = sorted(results.items(), key=lambda x:x[1], reverse=True)

    if limit <= 0:
        limit = len(sortedResult)
    else:
        limit = min(limit, len(sortedResult))
    
    return sortedResult[0:limit]

def get_similar_skills(skills, limit=10):
    words = []
    for skill in skills:
        for x in skill.split():
            x = x.lower()
            if x in ads_word2vec_model and x not in words:
                words.append(x)
                
    if not words:
        return {'similar_skills': [], 'query': []}
        
    similar_words = ads_word2vec_model.most_similar(positive=words, topn=limit)

    all_words = words.copy()
    for similar_word in similar_words:
        all_words.append(similar_word[0])
    vectors = np.asfarray([ads_word2vec_model[word] for word in all_words], dtype='float')
    
    tsne = sklearn.manifold.TSNE(n_components=2, random_state=42, perplexity=10)
    projected_vectors = tsne.fit_transform(vectors).tolist()
    named_projected_vectors = {}
    for i in range(len(all_words)):
        named_projected_vectors[all_words[i]] = projected_vectors[i]

    return {
        'similar_skills': [
            {'skill': similar_word[0], 'similarity': similar_word[1], 'vector': named_projected_vectors[similar_word[0]]} for similar_word in similar_words
        ],
        'query': [
            {'skill': word, 'vector': named_projected_vectors[word]} for word in words
        ]
    }
    