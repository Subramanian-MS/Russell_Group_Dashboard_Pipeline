# Accessibility check (default light theme)

WCAG AA requires a contrast ratio of at least 4.5:1 for normal text.

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| Green cell text | #1d5a34 | #a9d8b8 | 5.15 | Pass |
| Orange cell text | #7a3a07 | #f3ae7b | 4.58 | Pass |
| Table heading | #ffffff | #16285a | 14.14 | Pass |
| Body text on page | #2b3552 | #eef0f3 | 10.61 | Pass |
| Muted text on white (was #7b869e, 3.65, failed) | #5d6780 | #ffffff | 5.65 | Pass |
| Muted text on page (was 3.20, failed) | #5d6780 | #eef0f3 | 4.95 | Pass |
| Amber-dark text on white (was #9a7b0a, 4.03, failed) | #7d6400 | #ffffff | 5.68 | Pass |
| Green text on white | #3f7d4f | #ffffff | 4.93 | Pass |
| Highlight blue on white | #3f64b9 | #ffffff | 5.62 | Pass |
| Ink on average row | #16285a | #c4cad8 | 8.61 | Pass |

Not relying on colour alone: every coloured table cell also carries a printed value and a triangle (up = above the Russell Group average, down = below); chart bars carry value labels and a key; hovering gives the exact gap in points.
Not yet checked: the optional dark theme, screen-reader reading order of the charts (each chart has a text description), keyboard focus order beyond the table rows.
