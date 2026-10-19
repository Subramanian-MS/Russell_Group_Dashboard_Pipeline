# Russell Group Graduate Outcomes dashboard

An interactive one-page dashboard comparing the 24 Russell Group universities on what graduates were doing 15 months after finishing (HESA Graduate Outcomes 2023/24, with trends from 2017/18). Click any university to compare it with the group.

- `Russell_Group_Dashboard.html`: the dashboard (open in a browser).
- `docs/Calculation_Rules.md`: every measure with its numerator and denominator, and the rules for rounding and small groups.
- `docs/Validation_Report.md`: 22 automated checks against the HESA tables (rerun with `validate.py`).
- `docs/Accessibility_Check.md` and `docs/Browser_Test_Notes.md`: contrast and browser testing.
- Scripts: a repeatable Python/shell pipeline (below) that rebuilds everything from the HESA download.

Data: HESA Graduate Outcomes open data, Creative Commons Attribution 4.0. Independent project, not endorsed by HESA.

# Russell Group Graduate Outcomes dashboard: reproducible build

Turns the HESA "Graduate Outcome" download (zip of 11 detailed tables, all years) into the one-page dashboard, the Power BI tables, and a validation report.

## Run it
    ./run_all.sh /path/to/Graduate_Outcome.zip          # needs bash, unzip, awk, Python 3 with pandas and numpy
    LATEST_YEAR="2024/25" ./run_all.sh ...              # after HESA publishes a new year

Outputs: `Russell_Group_Dashboard.html` (open in a browser), `work/dash/*.csv` (clean tables for Power BI), `docs/Validation_Report.md` (re-run every time, the dashboard shows how many checks pass).

## Steps
filter_rows.sh (keep the 24 universities) > clean.py (headers, % to numbers, drop duplicate country rows) > dims.py (lookup tables) > dropzeros.py > dash.py / ext.py / extend.py (headline slice, per-university data) > validate.py (independent reconciliation to HESA tables) > build_html.py (template + data).
Edit the university list in `filter_rows.sh` (UKPRN list) and `dims.py` (names) if Russell Group membership changes.

## Using SharePoint
1. Store the HESA zip in a SharePoint library and sync it (OneDrive) or download it before the run: the pipeline reads a file path, so SharePoint only needs to be where the source lives.
2. Run `run_all.sh` on a schedule (Task Scheduler, Azure DevOps/GitHub Actions, or Power Automate calling a script) whenever a new zip lands.
3. Publish the generated HTML to a web location your stakeholders can open. SharePoint document libraries usually download .html files rather than display them, so check with IT; an internal web app, Azure Static Web Apps or similar works, and the data is public open data.
The page itself cannot read SharePoint live: browsers block that without a Microsoft sign-in and an approved host, and many hosting previews block outside requests entirely. The build-time approach above is the standard way to keep a static dashboard repeatable.
