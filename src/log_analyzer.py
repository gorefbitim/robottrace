import re
from src.third_parties.openai import completion_with_backoff, MODEL_HIGH
from ai import prompts
from src import status_color


class LogAnalyzer:
    """
    A class to analyze robotic operation logs, update statuses based on
    specific patterns, and interact with an AI model to generate
    summaries or responses based on log contents.
    """

    def __init__(self):
        """
        Initializes the LogAnalyzer with default status for robots and an empty
        log trace list.
        """
        self.status_dict = {
            "Robot 1": {"color": "green", "step": "0"},
            "Robot 2": {"color": "off", "step": "0"},
            "Robot 3": {"color": "off", "step": "0"},
            "Robot 4": {"color": "off", "step": "0"}
        }
        self.log_trace_lines = []

    def ai(self, line):
        """
        Sends log lines to an AI model if they contain specific keywords and
        appends the AI response to log_trace_lines.
        """
        if 'complete' in line and ('STAR' in line or 'err' in line):
            messages = [
                {"role": "system", "content": prompts.log},
                {"role": "user", "content": line}
            ]
            m = completion_with_backoff(model=MODEL_HIGH, messages=messages)
            self.log_trace_lines.append(m["choices"][0]["message"]["content"])

    def ai_summary(self):
        """
        Generates a summary of collected log traces using the AI model.
        """
        messages = [
            {"role": "system", "content": prompts.summary},
            {"role": "user", "content": '|'.join(self.log_trace_lines)}
        ]
        m = completion_with_backoff(model=MODEL_HIGH, messages=messages)
        return f'DONE! AI SUMMARY: {m["choices"][0]["message"]["content"]}'

    def analyze(self, line, robot="Robot 1"):
        """
        Analyzes a single log line to update robot status, trigger AI
        interactions, and possibly change status LED colors.
        """
        method_start_pattern = r"Analyze method - start; Method file (.+)"
        kinesin_log_pattern = r"Trace - complete; Kinesin (\w+)"

        match = re.search(method_start_pattern, line)
        if match:
            self.log_trace_lines.append(f"Start method: {match.group(1)}")

        match = re.search(kinesin_log_pattern, line)
        if match:
            self.status_dict[robot]["step"] = match.group(1)
            self.log_trace_lines.append(line.strip())

        self.ai(line)
        print(line, self.status_dict)

        if "SYSTEM : End method - complete;" in line:
            self.log_trace_lines.append(self.ai_summary())

        new_color = status_color.assign(line.lower())
        if new_color is not None:
            self.status_dict[robot]["color"] = new_color
