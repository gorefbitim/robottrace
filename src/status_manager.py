import re
from src.third_parties.openai import completion_with_backoff, MODEL_HIGH
from ai import prompts
from src import status_color


status_dict = {
    "Robot 1": {"color": "green", "step": "0"},
    "Robot 2": {"color": "off", "step": "0"},
    "Robot 3": {"color": "off", "step": "0"},
    "Robot 4": {"color": "off", "step": "0"}
}

# 2024-07-31 15:09:28> SYSTEM : Analyze method - start; Method file
# C:\Program Files (x86)\HAMILTON\Methods\elad\aliquotes_1_3_slack.hsl
METHOD_START_PATTERN = r"Analyze method - start; Method file (.+)"

# 2024-07-31 15:09:43> USER : Trace - complete; Kinesin Init
KINESIN_LOG_PATTERN = r"Trace - complete; Kinesin (\w+)"

# List to store specific log lines
log_trace_lines = []


def ai(line):
    if (('complete' in line) and ('STAR' in line) or ('err' in line)):
        messages = [
            {"role": "system", "content": prompts.log},
            {"role": "user", "content": line}]
        m = completion_with_backoff(
            model=MODEL_HIGH,
            messages=messages
        )
        log_trace_lines.append(m["choices"][0]["message"]["content"])


def ai_summary(line):
    messages = [
        {"role": "system", "content": prompts.summary},
        {"role": "user", "content": '|'.join(log_trace_lines)}]

    m = completion_with_backoff(
        model=MODEL_HIGH,
        messages=messages
    )
    return f'DONE! AI SUMMARY: {m["choices"][0]["message"]["content"]}'


def analyze(line, robot="Robot 1"):
    match = re.search(METHOD_START_PATTERN, line)
    if match:
        log_trace_lines.append(f"Start method: {match.group(1)}")

    match = re.search(KINESIN_LOG_PATTERN, line)
    if match:
        status_dict[robot]["step"] = match.group(1)
        log_trace_lines.append(line.strip())

    ai(line)

    print(line, status_dict)

    if "SYSTEM : End method - complete;" in line:
        log_trace_lines.append(ai_summary(log_trace_lines))

    new_color = status_color.assign(line.lower())
    if new_color is not None:
        status_dict[robot]["color"] = new_color
