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
        # List of all flashcards loaded from CSV
        self.allCards = []

        # One dictionary to track stats per term
        # Maps term to a dictionary with keys 'correct' and 'incorrect'
        self.termStats = defaultdict(lambda: {"correct": 0, "incorrect": 0})

        self.startTime = None
        self.totalTimeSpent = 0

    def load_from_csv(self, file_path):
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Check for required headers
                if 'term' not in reader.fieldnames or 'definition' not in reader.fieldnames:
                    raise ValueError("CSV file must contain 'term' and 'definition' columns.")
                for row in reader:
                    self.allCards.append(row)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return False
        except Exception as e:
            print(f"Error loading metrics: {e}")
            return False
        return True
        
    def start_study_session(self):
        self.startTime = time.time()
        print("Study session started.")

    def end_study_session(self):
        if self.startTime is None:
            print("Study session was not started.")
            return
        elapsedTime = time.time() - self.startTime
        self.totalTimeSpent += elapsedTime
        self.startTime = None # Reset start time
        return "Total time spent: {elapsedTime} seconds."

    # Record an answer for a term
    # Term: str - the term being answered
    # Correct: bool - whether the answer was correct
    def record_answer(self, term, correct):
        if correct:
            self.termStats[term]["correct"] += 1
        else:
            self.termStats[term]["incorrect"] += 1

    # Compute and return metrics summary
    def get_metrics(self):
        if self.startTime:
            self.end_study_session()

        correctCounts = 0
        incorrectCounts = 0
        problemAreas = {}

        for term, stats in self.termStats.items():
            correctCounts += stats["correct"]
            incorrectCounts += stats["incorrect"]
            if stats["incorrect"] > stats["correct"]:
                problemAreas[term] = stats["incorrect"]

        totalAnswers = correctCounts + incorrectCounts
        accuracy = (correctCounts / totalAnswers * 100) if totalAnswers > 0 else 0

        sortedProblemAreas = sorted(problemAreas.items(), key=lambda item: item[1], reverse=True)

        return {
            "Total Answers": totalAnswers,
            "Correct Answers": correctCounts,
            "Incorrect Answers": incorrectCounts,
            "Accuracy (%)": accuracy,
            "Problem Areas": sortedProblemAreas,
            "Total Time Spent (s)": self.totalTimeSpent,
            "termStats": self.termStats
        }