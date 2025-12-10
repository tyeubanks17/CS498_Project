'''
tracker.py

A module to track study statistics across sessions. Helps maintain and manage the stats.json file.

History:
4 Nov 2025 - Created
9 Dec 2025 - Added methods for retrieving overall stats and problem terms

To do:
- Implement delete stats for a set
'''

import json

class StatsTracker:
    """
        A class to track study statistics across sessions\
    """
    def __init__(self, file_path='stats.json'):
        self.file_path = file_path
        # This holds all-time stats loaded from file
        # { set name: { term: {correct: 10, incorrect: 2} ... } }
        self.all_time_stats = {}
        self.load_stats()

    # Load stats from the JSON file into all-_time_stats
    def load_stats(self):
        """
        Load the stats from the JSON file into the all_time_stats dictionary
        """
        try:
            with open(self.file_path, 'r') as f:
                self.all_time_stats = json.load(f)
        except (FileNotFoundError):
            print(f"Stats file not found at {self.file_path}, initializing new stats")
            self.all_time_stats = {}
        except (json.JSONDecodeError):
            print("Stats file is corrupted, initializing new stats")
            self.all_time_stats = {}
        except Exception as e:
            print(f"Error loading stats: {e}")
            self.all_time_stats = {}
    
    def save_stats(self):
        """
        Save the all_time_stats dictionary back to the JSON file
        """
        # Write the all_time_stats dictionary back to the JSON file
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.all_time_stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")

    # Update stats after a study session
    # session_metrics is expected to be a dictionary with metrics
    def update_stats(self, set_name, session_metrics):
        # Extract term_stats from session_metrics
        session_term_data = session_metrics.get('term_stats')
        if not session_term_data:
            print("No term stats found in session metrics, skipping update.")
            return
        
        # Ensure set_name entry exists in allTimeStats
        if set_name not in self.all_time_stats:
            self.all_time_stats[set_name] = {}

        for term, stats in session_term_data.items():
            # Ensure term entry exists
            if term not in self.all_time_stats[set_name]:
                self.all_time_stats[set_name][term] = {"correct": 0, "incorrect": 0}
            self.all_time_stats[set_name][term]["correct"] += stats.get("correct", 0)
            self.all_time_stats[set_name][term]["incorrect"] += stats.get("incorrect", 0)

        self.save_stats()

    # Retrieve stats for a specific set
    def get_stats(self, set_name):
        return self.all_time_stats.get(set_name, {})

    def get_all_time_accuracy(self, set_name):
        """
        Get overall accuracy for a set across all sessions
        Returns a percentage
        """
        stats = self.get_stats(set_name)
        if not stats:
            return 0
        total_correct = sum(t["correct"] for k, t in stats.items() if k != "__metadata__")
        total = sum(t["correct"] + t["incorrect"] for k, t in stats.items() if k != "__metadata__")
        return (total_correct / total * 100) if total > 0 else 0

    def get_problem_terms(self, set_name, limit=10):
        """
        Get terms with lowest accuracy (most incorrect relative to correct)
        Returns list of tuples: (term, accuracy_percent, incorrect_count)
        sorted by accuracy (lowest first)
        """
        stats = self.get_stats(set_name)
        if not stats:
            return []
        
        problem_areas = []
        for term, counts in stats.items():
            if term == "__metadata__":
                continue
            total = counts["correct"] + counts["incorrect"]
            if total > 0 and counts["incorrect"] > 0:
                accuracy = counts["correct"] / total * 100
                problem_areas.append((term, accuracy, counts["incorrect"]))
        
        # Sort by accuracy (worst terms first)
        return sorted(problem_areas, key=lambda x: x[1])[:limit]

    def get_all_sets_summary(self):
        """
        Get a summary of all sets with overall accuracy and total answers
        Returns list of tuples: (set_name, accuracy_percent, total_answers, correct_answers)
        """
        summary = []
        for set_name in self.all_time_stats.keys():
            stats = self.get_stats(set_name)
            total_correct = sum(t["correct"] for k, t in stats.items() if k != "__metadata__")
            total_answers = sum(t["correct"] + t["incorrect"] for k, t in stats.items() if k != "__metadata__")
            accuracy = (total_correct / total_answers * 100) if total_answers > 0 else 0
            summary.append((set_name, accuracy, total_answers, total_correct))
        
        # Sort by accuracy (descending) so best sets are first
        return sorted(summary, key=lambda x: x[1], reverse=True)

    def get_term_difficulty(self):
        """
        Get overall difficulty ranking across all sets
        Returns list of tuples: (term, accuracy_percent, total_incorrect)
        for terms that appear across multiple sets
        """
        term_stats = {}
        for set_name, stats in self.all_time_stats.items():
            for term, counts in stats.items():
                if term == "__metadata__":
                    continue
                if term not in term_stats:
                    term_stats[term] = {"correct": 0, "incorrect": 0}
                term_stats[term]["correct"] += counts["correct"]
                term_stats[term]["incorrect"] += counts["incorrect"]
        
        difficulties = []
        for term, counts in term_stats.items():
            total = counts["correct"] + counts["incorrect"]
            if total > 0:
                accuracy = counts["correct"] / total * 100
                difficulties.append((term, accuracy, counts["incorrect"]))
        
        return sorted(difficulties, key=lambda x: x[1])

    def get_total_answers_across_sets(self):
        """Get total number of answers across all sets and sessions"""
        total = 0
        for set_name in self.all_time_stats.keys():
            stats = self.get_stats(set_name)
            total += sum(t["correct"] + t["incorrect"] for k, t in stats.items() if k != "__metadata__")
        return total

    def get_total_correct_across_sets(self):
        """Get total correct answers across all sets and sessions"""
        total = 0
        for set_name in self.all_time_stats.keys():
            stats = self.get_stats(set_name)
            total += sum(t["correct"] for k, t in stats.items() if k != "__metadata__")
        return total

    def get_overall_accuracy(self):
        """Get overall accuracy across all sets and sessions"""
        total_correct = self.get_total_correct_across_sets()
        total_answers = self.get_total_answers_across_sets()
        return (total_correct / total_answers * 100) if total_answers > 0 else 0

    def delete_all_stats(self):
        """
        Delete all stored statistics (clear stats.json)
        Returns True if successful, False otherwise
        """
        try:
            self.all_time_stats = {}
            self.save_stats()
            print("All statistics deleted.")
            return True
        except Exception as e:
            print(f"Error deleting stats: {e}")
            return False
