# Local demo verification

The reproducible demo command is `python scripts/run_local_demo.py` after installing requirements in a Python 3.12 virtual environment. It generates synthetic inputs, runs the pandas pipeline, seeds/builds a fresh DuckDB database, runs Python regressions, and executes eight SQL metric queries.

The current Mac could not complete dependency installation because the disk ran out of space. A fresh run of the command is being verified in GitHub CI. This record will be updated with its observed results; previous test results are not presented as a new execution.

Power BI rendering, corrected DAX execution, Snowflake deployment/refresh, access controls, and new screenshots remain unverified. Existing media is historical.
