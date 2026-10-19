#!/bin/bash
# Rebuilds the dashboard from the HESA download.  Usage: ./run_all.sh /path/to/Graduate_Outcome.zip
# Optional: LATEST_YEAR="2024/25" ./run_all.sh ...   (when HESA publishes a new year)
set -e
ZIP=$(realpath "$1"); HERE=$(pwd); mkdir -p work && cd work && mkdir -p go flt out dash
unzip -q -o "$ZIP" -d go
for t in 1 2 3 4 5 6 8 19 22 26 28; do bash "$HERE/filter_rows.sh" $t; python3 "$HERE/clean.py" $t; done
python3 "$HERE/dims.py" >/dev/null
python3 "$HERE/dropzeros.py"
python3 "$HERE/dash.py"            # headline-slice tables (Dash_*.csv) + dash/data.json
python3 "$HERE/ext.py"             # + per-university detail -> dash/data2.json
python3 "$HERE/extend.py"          # + subject and salary per university -> dash/data3.json
python3 "$HERE/validate.py" flt dash/data3.json "$HERE/docs/Validation_Report.md" out/Dim_Provider.csv
python3 "$HERE/build_html.py" "$HERE/template/dashboard_template.html" dash/data3.json "$HERE/docs/Validation_Report.md" "$HERE/Russell_Group_Dashboard.html"
echo "Done. Dashboard: Russell_Group_Dashboard.html   Power BI tables: work/dash/*.csv   Checks: docs/Validation_Report.md"
