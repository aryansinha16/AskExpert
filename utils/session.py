import os 
import json

class SessionManager:
    def __init__(self, file_path="session_history.json"):
        self.file_path = file_path

    def load_session_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                session_history = json.load(file)
        else:
            session_history = []
        return session_history

    def save_session_history(self, session_history):
        with open(self.file_path, "w") as file:
            json.dump(session_history, file, indent=4)

    def clear_session_history(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)