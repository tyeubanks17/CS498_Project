'''
metrics.py

A module to handle metrics per session. 

History:
30 October 2025 - Created
4 Nov 2025 - Updated to integrate with tracker.py

'''

import csv, time
from collections import defaultdict

class Metrics:
    def __init__(self):
        # List of all flashcards loaded from CSV
        self.all_cards = []

        # One dictionary to track stats per term
        # Maps term to a dictionary with keys 'correct' and 'incorrect'
        self.term_stats = defaultdict(lambda: {"correct": 0, "incorrect": 0})

        self.start_time = None
        self.total_time_spent = 0

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
        return True
        
    def start_study_session(self):
        self.start_time = time.time()
        print("Study session started.")

    def end_study_session(self):
        if self.start_time is None:
            print("Study session was not started.")
            return
        elapsed_time = time.time() - self.start_time
        self.total_time_spent += elapsed_time
        self.start_time = None # Reset start time
        return elapsed_time

    # Record an answer for a term
    # Term: str - the term being answered
    # Correct: bool - whether the answer was correct
    def record_answer(self, term, correct):
        if correct:
            self.term_stats[term]["correct"] += 1
        else:
            self.term_stats[term]["incorrect"] += 1

    # Compute and return metrics summary
    def get_metrics(self):
        if self.start_time:
            self.end_study_session()

        correct_counts = 0
        incorrect_counts = 0
        problem_areas = {}

        for term, stats in self.term_stats.items():
            correct_counts += stats["correct"]
            incorrect_counts += stats["incorrect"]
            if stats["incorrect"] > stats["correct"]:
                problem_areas[term] = stats["incorrect"]

        total_answers = correct_counts + incorrect_counts
        accuracy = (correct_counts / total_answers * 100) if total_answers > 0 else 0

        sorted_problem_areas = sorted(problem_areas.items(), key=lambda item: item[1], reverse=True)

        return {
            "Total Answers": total_answers,
            "Correct Answers": correct_counts,
            "Incorrect Answers": incorrect_counts,
            "Accuracy (%)": accuracy,
            "Problem Areas": sorted_problem_areas,
            "Total Time Spent (s)": self.total_time_spent,
            "term_stats": dict(self.term_stats)
        }