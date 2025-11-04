import json

class StatsTracker:
    ''' A class to track study statistics across sessions.'''
    def __init__(self, file_path='stats.json'):
        self.file_path = file_path
        # This holds all-time stats loaded from file
        # { set name: { term: {correct: 10, incorrect: 2} ... } }
        self.allTimeStats = {}
        self.load_stats()

    # Load stats from the JSON file into allTimeStats
    def load_stats(self):
        try:
            with open(self.file_path, 'r') as f:
                self.allTimeStats = json.load(f)
        except (FileNotFoundError):
            print("Stats file not found at {self.file_path}, initializing new stats.")
            self.allTimeStats = {}
        except (json.JSONDecodeError):
            print("Stats file is corrupted, initializing new stats.")
            self.allTimeStats = {}
        except Exception as e:
            print(f"Error loading stats: {e}")
            self.allTimeStats = {}
    
    def save_stats(self):
        # Write the allTimeStats dictionary back to the JSON file
        try:
            with open(self.filePath, 'w') as f:
                json.dump(self.allTimeStats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")

    # Update stats after a study session
    # sessionMetrics is expected to be a dictionary with metrics
    def update_stats(self, setName, sessionMetrics):
        # Extract termStats from sessionMetrics
        sessionTermData = sessionMetrics.get('termStats')
        # If no termStats found, nothing to update
        if not sessionTermData:
            print("No term stats found in session metrics, skipping update.")
            return
        # Ensure setName entry exists in allTimeStats
        if setName not in self.allTimeStats:
            self.allTimeStats[setName] = {}

        for term, stats in sessionTermData.items():
            # Ensure term entry exists
            if term not in self.allTimeStats[setName]:
                self.allTimeStats[setName][term] = {"correct": 0, "incorrect": 0}
            self.allTimeStats[setName][term]["correct"] += stats.get("correct", 0)
            self.allTimeStats[setName][term]["incorrect"] += stats.get("incorrect", 0)

        self.save_stats()

    # Retrieve stats for a specific set
    def get_stats(self, setName):
        return self.allTimeStats.get(setName, {})

