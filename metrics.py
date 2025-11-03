'''
Reading on comma delimited csv file with a header rows "term" and "definition"

Metrics to track:
- Time spent studying 
    - Per session
- Accuracy (number of correct definitions)
- Problem areas (terms frequently answered incorrectly)
'''

import csv, time
from collections import defaultdict

class Metrics:
    def __init__(self):
        self.all_cards = []

        self.correct_counts = 0
        self.incorrect_counts = 0
        
        self.start_time = None
        self.problem_areas = defaultdict(int)  # term -> incorrect count

    def load_from_csv(self, file_path):
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Check for required headers
                if 'term' not in reader.fieldnames or 'definition' not in reader.fieldnames:
                    raise ValueError("CSV file must contain 'term' and 'definition' columns.")
                for row in reader:
                    self.all_cards.append(row)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return False
        except Exception as e:
            print(f"Error loading metrics: {e}")
            return False
        
    def start_study_session(self):
        self.start_time = time.time()
        print("Study session started.")

    def end_study_session(self):
        if self.start_time is None:
            print("Study session was not started.")
            return
        elapsed_time = time.time() - self.start_time
        print(f"Study session ended. Time spent: {elapsed_time:.2f} seconds.")
        self.start_time = None # Reset start time

    def record_answer(self, term, correct):
        if correct:
            self.correct_counts += 1
        else:
            self.incorrect_counts += 1
            self.problem_areas[term] += 1

    def metrics_summary(self):
        if self.start_time:
            Metrics.end_study_session(self)

        total_answers = self.correct_counts + self.incorrect_counts
        accuracy = (self.correct_counts / total_answers * 100) if total_answers > 0 else 0

        sorted_problem_areas = dict(sorted(self.problem_areas.items(), key=lambda item: item[1], reverse=True))

        return {
            "Total Answers": total_answers,
            "Correct Answers": self.correct_counts,
            "Incorrect Answers": self.incorrect_counts,
            "Accuracy (%)": accuracy,
            "Problem Areas": sorted_problem_areas
        }