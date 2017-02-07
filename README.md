# jobads-textminer
Job Ads Text Mining Project text miner and main backend.

_This project aims at fetching and storing job ads raw data and processing it._

## Cloning the repository

```
git clone https://github.com/tpucci/jobads-textminer.git
```

## Installing the dependencies

The projets relies on some python packages. To install them, run the following command from the project's root folder:
```
pip install -r requirements.txt
```

## Directory structure

- `config/` (configuration directory, see _Configuration_ paragraph)
- `docs/` (documentations)
- `jobads/` (jobads main package, see _main package_ paragraph)

## Configuration

The application configuration should be stored in a JSON file in the `config/` directory.

**Sensitive information, such as API keys, database credentials, etc. should not be stored in the configuration file.** Environment variables are used instead.

To refer to environment variables in the JSON configuration variables, use `ENV:XXXX` sythax.
 ```json
...
"API_key": "ENV:JOBADS_INDEED_API_KEY",
...
```


## jobads main package

The main package is located in the `jobads/` directory. It implements job ads fetching and analysis logic.

> __Note, configuration__.
> When importing the package, the configuration is automatically loaded. By default, the file `./config/development.json` is loaded (where `.` is the current directory, from which python was loaded).
>
> The environment variable `JOBADS_CONFIG` overwrites this value.
>
> To read a value from the configuration:
> `from jobads import config` and `config['someKey']`.

For the moment, the jobads package is made up of 3 entities, described below.

### Ad collector (`jobads/collector/`)

- fetches job ads from remote APIs (for each vendor API, the fetching logic is implemented in `jobads/collector/providers/` subdirectory)
- stores them into a database (_raw job ads database_)

### Ad processor (`jobads/processor/`)

- takes job ads from the _raw job ads database_
- processes them (via ElasticSearch or custom data mining)

### Fetching ads (`jobads/fetch/`)

- processes queries over job ads

## API

The API server is the backend entry point. It handles requests from the frontend server.

To launch the API server locally,
```bash
gunicorn api:app -c gunicorn_config.private.py
```
assuming `gunicorn_config.private.py` is the gunicorn local configuration file.

`gunicorn_config.private.py` can be used to set environment variables :
```python
raw_env = ['JOBADS_INDEED_API_KEY=0123456789', 'JOBADS_ELASTICSEARCH_HOST=xxx.yyy.zzz.amazonaws.com']
```

## Notes

Do not forget to update `setup.py` (especially _packages_ and _install\_requires_ values), `requirements.txt` and this README when modifying the code.
