def assign(line):
    # TODO - how do we know we're off ? color = "off"
    color = None

    if "Execute method - start; Method file".lower() in line:
        color = "green"
    elif "SYSTEM : End method - complete".lower() in line:
        color = "green"
    elif "err" in line:
        color = "yellow"
    elif "abort" in line:
        color = "red"

    # print(line, color)

    return color
