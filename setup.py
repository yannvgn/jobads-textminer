#!/usr/bin/env python

from setuptools import setup

setup(name='jobads-textminer',
      version='0.1',
      description='Job Ads Text Miner',
      url='https://github.com/tpucci/jobads-textminer',
      packages=['jobads', 'jobads.collector', 'jobads.collector.providers', 'jobads.processor', 'jobads.fetch'],
      install_requires=[
            'pymongo>=3.4,<3.5',
            'Flask>=0.12',
            'gevent',
            'gunicorn',
            'elasticsearch>=2.3.0,<3.0.0',
            'certifi',
            'gensim',
            'numpy',
            'nltk',
            'sklearn'
            ]
     )
