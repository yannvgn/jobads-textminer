import os
import json
import re

# To use the configuration in the project,
# just "from jobads import config"
# and get configuration variables with "config['someValue']"

# TODO: why not splitting configuration files (database.json, elastic.json, indeed.json, etc.)
defaultConfigurationFile = 'config/development.json'
configurationFile = os.getenv('JOBADS_CONFIG', defaultConfigurationFile)

with open(configurationFile, 'r') as jsonFile:
    config = json.load(jsonFile)

env_re = re.compile(r'^ENV:([A-Za-z0-9-_]+)$')

def parseEnv(configPart):
    if type(configPart) is dict:
        for k in configPart:
            configPart[k] = parseEnv(configPart[k])
    elif type(configPart) is list:
        for i in range(len(configPart)):
            configPart[i] = parseEnv(configPart[i])
    elif type(configPart) is str:
        m = env_re.match(configPart)
        if m:
            return os.getenv(m.group(1), m.group(1))
    return configPart

config = parseEnv(config)
