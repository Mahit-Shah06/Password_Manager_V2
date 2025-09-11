import os
import tempfile
import atexit
import signal
import json
import base64

class SessionHandler:
    def __init__(self):
        self.session_file = os.path.join(tempfile.gettempdir(), "pm_session.json")

        atexit.register(self.clear_session)
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)

    def create_session(self, uuid, key):
        if not os.path.exists(self.session_file):
            with open(self.session_file, "w") as f:
                json.dump({"uuid": uuid, "key" : base64.b64encode(key).decode('utf-8')}, f)

    def load_session(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, "r") as f:
                data = json.load(f)
                return data["uuid"], base64.b64decode(data["key"])
        else:
            return None

    def clear_session(self):
        if os.path.exists(self.session_file):
            try:
                os.remove(self.session_file)
            except:
                pass

    def handle_exit(self):
        self.clear_session()
        raise SystemExit(0)