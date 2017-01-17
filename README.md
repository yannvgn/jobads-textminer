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

Then, you should create your configuration files: copy `config/*.sample.json` to `config/*.private.json` and change the values in your private files according to your environment (see _Configuration_ paragraph).

## Directory structure

- `config/` (configuration directory, see _Configuration_ paragraph)
- `docs/` (documentations)
- `jobads/` (jobads main package, see _main package_ paragraph)

## Configuration

All configuration variables (API keys, database connection information, ...) should be stored in a JSON file in the `config/` directory.

By convention, we distinguish 2 types of configuration files:
- `*.sample.json` containing __every__ configuration variable keys but with sample values. __Such files are committed: they must not contain any credentials__.
- `*.private.json` containing the same variables as the corresponding sample file, but with actual values. __They should never be committed__.

## jobads main package

The main package is located in the `jobads/` directory. It implements job ads fetching and analysis logic.

> __Note, configuration__.
> When importing the package, the configuration is automatically loaded. By default, the file `./config/development.private.json` is loaded (where `.` is the current directory, from which python was loaded).
>
> The environment variable `JOBADS_CONFIG` overwrites this value.
>
> To read a value from the configuration:
> `from jobads import config` and `config['someKey']`.

For the moment, the jobads package is made up of 2 entities, described below.

### Ad collector (`jobads/collector/`)

- fetches job ads from remote APIs (for each vendor API, the fetching logic is implemented in `jobads/collector/providers/` subdirectory)
- stores them into a database (_raw job ads database_)

### Ad processor (`jobads/processor/`)

- takes job ads from the _raw job ads database_
- processes them (via ElasticSearch or custom data mining)

## Notes

Do not forget to update `setup.py` (especially _packages_ and _install\_requires_ values), `requirements.txt` and this README when modifying the code.
