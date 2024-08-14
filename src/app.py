# app.py
import threading
from flask import Flask, render_template, jsonify
from observer import start_observer
from log_analyzer import LogAnalyzer


app = Flask(__name__)
log_analyzer = LogAnalyzer()


@app.route('/status')
def get_status():
    return jsonify(log_analyzer.status_dict)


@app.route('/trace_logs')
def get_trace_logs():
    return jsonify(log_analyzer.log_trace_lines)


@app.route('/')
def home():
    return render_template('index.html', status=log_analyzer.status_dict)


if __name__ == '__main__':
    observer_thread = threading.Thread(
        target=start_observer, args=(log_analyzer,))
    observer_thread.start()
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5612, debug=True)
