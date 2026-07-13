"""Salvaged palette + shared Altair theme for the observatory charts.

Colours come from the original visual study's validated reference instance:
categorical blue/green tuned for CVD contrast, and a 7-step sequential blue ramp.
Charts render on a transparent background so the page (Quarto light/dark) shows
through; ink/grid use mid-tones that stay legible on both.
"""
import altair as alt

BLUE = "#2a78d6"
GREEN = "#1baf7a"
GRAY = "#b5b3ab"
INK = "#52514e"
MUTED = "#898781"
GRID = "#d9d8d1"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

# Verdict scale: kept inside the validated blue ramp + a neutral, no new hue.
VERDICT_DOMAIN = ["blocked", "partial", "allowed"]
VERDICT_RANGE = ["#2a78d6", "#9ec5f4", "#d8d6cf"]

# Sequential blue ramp (e.g. share-blocked heatmaps).
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def themed(chart):
    """Apply the shared look to a finished Altair chart."""
    return (
        chart
        .configure(background="transparent")
        .configure_view(stroke=None)
        .configure_axis(
            labelColor=INK, titleColor=INK, gridColor=GRID, domainColor=GRID,
            tickColor=GRID, labelFont=FONT, titleFont=FONT,
            labelFontSize=11, titleFontSize=12)
        .configure_legend(
            labelColor=INK, titleColor=INK, labelFont=FONT, titleFont=FONT,
            labelFontSize=11, titleFontSize=12, orient="top", title=None)
        .configure_title(color=INK, font=FONT, fontSize=15, anchor="start")
    )
