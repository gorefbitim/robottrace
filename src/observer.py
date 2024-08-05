import os
import time
from dotenv import load_dotenv
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from status_manager import analyze


load_dotenv()
directory_to_watch = os.getenv("directory_to_watch2")


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.cur_fn = None
        self.cur_f = None
        self.file_size = 0

    def on_created(self, event):
        print(f"C: {event}")
        if not event.is_directory:
            print(f'File created: {event.src_path}')
            self.process_file(event.src_path)

    def on_modified(self, event):
        print(f"M: {event}")
        if not event.is_directory:
            print(f'File modified: {event.src_path}')
            self.process_file(event.src_path)

    def process_file(self, file_path):
        print(self.cur_fn, file_path)

        if (
                self.cur_fn != file_path
                or self.file_size > os.path.getsize(file_path)
        ):
            self.cur_fn = file_path
            self.cur_f = open(self.cur_fn, 'r')

        cur_line = self.cur_f.readline()

        print(cur_line)

        while cur_line:
            analyze(cur_line, "Robot 1")

            # print(cur_line)
            cur_line = self.cur_f.readline()

        self.file_size = os.path.getsize(self.cur_fn)


def start_observer():
    event_handler = MyHandler()
    observer = PollingObserver()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
