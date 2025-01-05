#!/usr/bin/python
# Tool to watch a log folder for new files / change of files.
import os
import time
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scripts.slack import post_message_to_slack


# Load environment variables from .env file
load_dotenv()

directory_to_watch = os.getenv('directory_to_watch1')


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.cur_fn = None
        self.cur_f = None

    def on_created(self, event):
        if not event.is_directory:
            print(f'File created: {event.src_path}')
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f'File modified: {event.src_path}')
            self.process_file(event.src_path)

    def process_file(self, file_path):
        if self.cur_fn != file_path:
            self.cur_fn = file_path
            self.cur_f = open(self.cur_fn, 'r')
            self.cur_f.seek(0, 2)

        cur_line = self.cur_f.readline()
        while (cur_line):
            print(cur_line)
            if 'error' in cur_line.lower() or 'abort' in cur_line.lower():
                post_message_to_slack(cur_line)
            cur_line = self.cur_f.readline()


def main():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
