# Local demo verification

Verified on 24 November 2026 in a fresh GitHub-hosted Ubuntu environment with Python 3.12.16. The local demo command completed successfully; this is CI execution evidence, not a successful run on the current Mac.

- [Successful workflow run](https://github.com/AmenBouallagui/fabric-sales-marketing-platform/actions/runs/45308704980)
- Source head: `5161f00c28ec224558aef606f148b3d021e5c228`
- Tested PR merge commit: `51e0b67dc339cbfabd2d56427ae5b12d3672b3ca`
- Completion: 2026-11-24 01:57:08 UTC.

## Executed checks

| Check | Observed result |
| --- | --- |
| Synthetic data generator and pandas pipeline | Completed successfully |
| dbt dependencies and seed loading | Completed successfully before build |
| dbt model build | 21 models succeeded |
| dbt data tests | 39 passed |
| Python regressions | 5 passed; none skipped |
| Business metric SQL | All 8 queries executed |
| Repository hygiene | Generated data, DuckDB databases, and dbt artifacts not tracked |

The regressions cover campaign fact fanout and payment/refund filtering, invalid quantities and dates, tied update ordering, unknown members, orphan orders, and foreign-key membership.

## Synthetic warehouse totals

These totals cover all committed fixture dates and only Paid orders with refund_flag = false. Revenue includes tax. These are synthetic demonstration values, not client results or verified DAX outputs.

| Metric | Value |
| --- | ---: |
| Eligible orders | 8,767 |
| Revenue | 6,295,643.44 |
| Net revenue | 5,829,300.00 |

| SQL result | Rows |
| --- | ---: |
| Monthly revenue | 24 |
| Product category margin | 7 |
| Campaign ROAS | 36 |
| Channel spend | 7 |
| Customer segments | 4 |
| Support quality | 4 |
| Seeded failed checks | 2 |
| Seeded pipeline runs | 14 |

## Reproduce and inspect evidence

From a Python 3.12 environment with the requirements installed:

```bash
python scripts/run_local_demo.py
```

The command generates inputs with seed 123, builds a fresh DuckDB database, and retains `verification.md`, `execution.json`, `metrics.json`, and six command logs in ignored `outputs/local_demo/`. The execution record includes SHA-256 hashes of the committed CSV fixtures. Choose a different `--output-dir` for another fresh run; the command refuses to overwrite an existing warehouse.

The successful workflow uploaded the same evidence as [local-demo-evidence](https://github.com/AmenBouallagui/fabric-sales-marketing-platform/actions/runs/45308704980/artifacts/14881288858), plus dbt diagnostics. Artifacts have seven-day retention; regenerate them with a new workflow run after expiry.

## Limits

The current Mac could not finish dependency installation because the disk ran out of space. Its fresh demo execution remains unverified. The isolated, incomplete environment was removed; no unrelated user files were deleted.

pandas uses generated CSVs while dbt uses separate committed fixtures, so totals between the two implementations are not expected to match. The Operations page uses seeded demonstration telemetry, not the current CI run.

Power BI rendering, corrected DAX execution, Snowflake deployment/refresh, access controls, and new screenshots remain unverified. Existing screenshots and recording are historical. Source definitions and portability macros are not proof of a deployed cloud solution.
