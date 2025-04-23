import json
import os 

class FeedbackHandler:
    def __init__(self, file_path="feedback.json"):
        self.file_path = file_path
        self.corrections = []
    def load_feedback(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                feedback_data = json.load(file)
        else:
            feedback_data = []
        return feedback_data
    def save_feedback(self, feedback_data):
        with open(self.file_path, "w") as file:
            json.dump(feedback_data, file, indent=4)
    def handle_feedback(self, question, answer, feedback):
        feedback_data = self.load_feedback()
        if feedback.lower() == "no":
            correct_answer = input("Please provide the correct answer: ")
            feedback_entry = {
                "question": question,
                "incorrect_answer": answer,
                "correct_answer": correct_answer
            }
            feedback_data.append(feedback_entry)
            self.corrections.append(feedback_entry)
            self.save_feedback(feedback_data)
            print("Feedback saved. Thank you!")
        else:
            print("Thank you for your feedback!")
        return self.corrections