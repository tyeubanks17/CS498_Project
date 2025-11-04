'''
To do:
- Implement delete stats for a set
'''

import json

class StatsTracker:
    ''' A class to track study statistics across sessions.'''
    def __init__(self, file_path='stats.json'):
        self.file_path = file_path
        # This holds all-time stats loaded from file
        # { set name: { term: {correct: 10, incorrect: 2} ... } }
        self.all_time_stats = {}
        self.load_stats()

    # Load stats from the JSON file into all-_time_stats
    def load_stats(self):
        try:
            with open(self.file_path, 'r') as f:
                self.all_time_stats = json.load(f)
        except (FileNotFoundError):
            print(f"Stats file not found at {self.file_path}, initializing new stats.")
            self.all_time_stats = {}
        except (json.JSONDecodeError):
            print("Stats file is corrupted, initializing new stats.")
            self.all_time_stats = {}
        except Exception as e:
            print(f"Error loading stats: {e}")
            self.all_time_stats = {}
    
    def save_stats(self):
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
        # If no term_stats found, nothing to update
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

