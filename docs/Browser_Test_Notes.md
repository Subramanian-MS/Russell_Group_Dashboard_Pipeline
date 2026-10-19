# Browser test notes

Tested in headless Chromium (Playwright) against the built HTML file.

| Test | Result |
|---|---|
| Desktop 1920, 1440 px, light theme: no horizontal page overflow, table cells on one line, key figures fit | Pass |
| Desktop 1280 px: table scrolls inside its card (99 px at the test font) | Works, scrolls |
| Dark theme toggle | Loads and switches without errors |
| Phone width 390 px: no horizontal page overflow (a header and top-bar overflow was found and fixed) | Pass |
| Click a row, use the dropdown, sort a column, select with the Enter key | Pass |
| Chart code (ticks, tooltips, labels) run for 24 universities including small groups | No errors |
| Chart.js blocked or offline: table and key figures still work, charts show a message | Pass |

Not verified here (the test machine had no internet, so Chart.js was replaced by a stand-in that runs the chart code but draws nothing):
- how the charts actually look and whether labels overlap;
- real Segoe UI / Open Sans rendering;
- touch interaction on a real phone; screen-reader behaviour.

Please open the page on your own machine, in light and dark mode and at phone width, and check the three charts before sharing.
