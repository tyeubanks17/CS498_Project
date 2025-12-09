'''
alltimestats.py

Screen for displaying all-time statistics across multiple sessions and sets.

History:
9 December 2025 - Created
'''

from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, DictProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.screen import MDScreen
from tracker import StatsTracker

# Load KV layout
Builder.load_file("./screens/alltimestats.kv")


class AllTimeStatsScreen(MDScreen):
    '''
    A screen to display all-time statistics across all sessions and sets.
    Shows overall accuracy, problem terms, per-set performance, etc.
    '''
    sets_summary = ListProperty([])  # List of (set_name, accuracy, total_answers, correct_answers)
    sets_problem_terms = ListProperty([])  # List of (set_name, problem_terms_list) tuples
    problem_terms_display = StringProperty("")  # Formatted text for display
    overall_accuracy_text = StringProperty("Overall Accuracy: 0%")
    total_stats_text = StringProperty("Total Answers: 0 | Correct: 0")

    def on_enter(self):
        '''
        Called when screen is displayed. Load and display all-time stats.
        '''
        try:
            tracker = StatsTracker()
            
            # Get overall stats
            overall_acc = tracker.get_overall_accuracy()
            total_answers = tracker.get_total_answers_across_sets()
            total_correct = tracker.get_total_correct_across_sets()
            
            self.overall_accuracy_text = f"Overall Accuracy: {overall_acc:.1f}%"
            self.total_stats_text = f"Total Answers: {total_answers} | Correct: {total_correct}"
            
            # Get per-set summary and problem terms for each set
            self.sets_summary = tracker.get_all_sets_summary()
            
            # Build list of (set_name, problem_terms_list) for display
            sets_with_problems = []
            for set_name, accuracy, total_answers, correct_answers in self.sets_summary:
                problem_terms = tracker.get_problem_terms(set_name, limit=5)
                if problem_terms:
                    sets_with_problems.append((set_name, problem_terms))
            
            self.sets_problem_terms = sets_with_problems
            
            # Build formatted text for display
            if sets_with_problems:
                display_text = ""
                for set_name, problem_terms in sets_with_problems:
                    display_text += f"{set_name}:\n"
                    for term, accuracy, incorrect in problem_terms:
                        display_text += f"{term}: {accuracy:.1f}% ({incorrect} incorrect)\n"
                    display_text += "\n"
                self.problem_terms_display = display_text
            else:
                self.problem_terms_display = "No statistics yet. Better start studying!"
                
        except Exception as e:
            print(f"Error in AllTimeStatsScreen: {e}")

    def return_to_menu(self):
        '''
        Return to main menu
        '''
        App.get_running_app().root.current = 'menu'

    def delete_all_stats(self):
        '''
        Delete all stored statistics after user confirmation.
        '''
        try:
            tracker = StatsTracker()
            if tracker.delete_all_stats():
                # Reload the screen to show empty state
                self.on_enter()
        except Exception as e:
            print(f"Error deleting stats: {e}")

    def view_set_stats(self, set_name):
        '''
        Navigate to a detailed view of stats for a specific set.
        (Optional: could create a SetDetailStatsScreen for this)
        '''
        # For now, just print the set name
        print(f"Viewing details for: {set_name}")
