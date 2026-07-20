"""Salvaged palette + shared Altair theme for the observatory charts.

Colours come from the original visual study's validated reference instance:
categorical blue/green tuned for CVD contrast, and a 7-step sequential blue ramp.
Charts render on a transparent background so the page (Quarto light/dark) shows
through; ink/grid use mid-tones that stay legible on both.
"""
ACCENT = "#1a1a19"      # observatory signature (ink); used sparingly, for emphasis
PAPER = "#f9f9f7"       # page plane; also text laid on top of an ink-dark bar
BAR_GRAY = "#cbc9c2"    # de-emphasised bars in an emphasis chart
GRAY = "#b5b3ab"
INK = "#52514e"         # secondary text ink (labels, values)
MUTED = "#898781"
GRID = "#e6e4dd"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

# Verdict is an ordered scale (blocked > partial > allowed): one-hue ink ramp,
# darker = more restricted. "blocked" carries the signature ink.
VERDICT_DOMAIN = ["blocked", "partial", "allowed"]
VERDICT_RANGE = ["#1a1a19", "#a7a59e", "#dcdad3"]

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
            labelFontSize=13, titleFontSize=14)
        .configure_legend(
            labelColor=INK, titleColor=INK, labelFont=FONT, titleFont=FONT,
            labelFontSize=13, titleFontSize=13, orient="top", title=None,
            symbolSize=140)
        .configure_title(color=INK, font=FONT, fontSize=15, anchor="start")
    )
