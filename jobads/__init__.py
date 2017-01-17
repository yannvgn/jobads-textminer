import os
import json

# To use the configuration in the project,
# just "from jobads import config"
# and get configuration variables with "config['someValue']"

# TODO: why not splitting configuration files (database.json, elastic.json, indeed.json, etc.)
# defaultConfigurationFile = os.path.join(os.path.dirname(__file__), '../config/development.private.json')
defaultConfigurationFile = 'config/development.private.json'
configurationFile = os.getenv('JOBADS_CONFIG', defaultConfigurationFile)

with open(configurationFile, 'r') as jsonFile:
    config = json.load(jsonFile)
