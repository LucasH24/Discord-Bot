def calc_color(value):
    returnColor = ""
    if value > 234:
        returnColor = "#bd0808"

    elif value > 219:
        returnColor = "#e64e4e"

    elif value > 100:
        returnColor = "#f29f5e"

    elif value > 25:
        returnColor = "yellow"

    elif value > 10:
        returnColor = "#6bed90"

    elif value > 1:
        returnColor = "#5389ed"

    elif value == 1:
        returnColor = "#f030e3"

    return returnColor