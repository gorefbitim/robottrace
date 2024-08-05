import re


status_dict = {
    "Robot 1": {"color": "green", "step": "0"},
    "Robot 2": {"color": "red", "step": "0"},
    "Robot 3": {"color": "green", "step": "0"},
    "Robot 4": {"color": "green", "step": "0"}
}

# List to store specific log lines
log_trace_lines = []


def analyze(line, robot="Robot 1"):
    # Capture trace lines
    match = re.search(r"Trace - complete; Kinesin (\w+)", line)
    if match:
        status_dict[robot]["step"] = match.group(1)
        log_trace_lines.append(line.strip())

    print(line, status_dict)

    if "Execute method - start; Method file" in line:
        status_dict[robot]["color"] = "green"
    elif "SYSTEM : End method - complete" in line:
        status_dict[robot]["color"] = "yellow"
    elif "error" in line:
        status_dict[robot]["color"] = "red"
