# CCL 2024 Wrapped

## Obtain Datasets

1. Actions: export to CSV from [here](https://community.citizensclimate.org/actions/home), make sure you filter for proper dates

2. Members: export all chapter members from [here](https://community.citizensclimate.org/tools/chapter-roster)

3. replace the file names used to `read_csv` in `stats.py` (I know this could be a config or command line arg but I am tired)

## Run

```
pip install -r requirements.txt
python stats.py
```