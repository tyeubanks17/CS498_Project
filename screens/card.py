'''
card.py

The flashcard viewer components.

History:
7 November 2025 - Created
11 November 2025 - Refactored into CardWidget (display) and CardStudyScreen (study flow)
11 November 2025 - Added MetricsScreen for displaying study results
'''

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.screen import MDScreen
from metrics import Metrics
from set import Set

# Load card KV layout at module level
Builder.load_file("./screens/card.kv")


class CardWidget(BoxLayout):
    '''
    A reusable flashcard display widget.
    Shows term/definition and handles flipping.
    '''
    term = StringProperty("Term")
    definition = StringProperty("Definition")
    is_term_side = True  # Track which side is showing

    def flip_card(self):
        '''
        Toggle between showing term and definition
        '''
        self.is_term_side = not self.is_term_side
        self._update_display()

    def load_card(self, term, definition):
        '''
        Load a new card and reset to show term side
        '''
        self.term = term
        self.definition = definition
        self.is_term_side = True
        self._update_display()

    def _update_display(self):
        '''
        Update the displayed label based on current side
        '''
        if hasattr(self, 'ids') and 'term_label' in self.ids:
            self.ids.term_label.text = "TERM" if self.is_term_side else "DEFINITION"
            self.ids.content_label.text = self.term if self.is_term_side else self.definition


class CardStudyScreen(MDScreen):
    '''
    A screen for studying flashcards from a set.
    Manages card navigation, metrics tracking, and study flow.
    '''
    current_card_index = NumericProperty(0)
    total_cards = NumericProperty(0)
    current_set = ObjectProperty(None, allow_none=True)

    def __init__(self, default_set_path=None, **kwargs):
        super().__init__(**kwargs)
        self.cards = []  # List of {term, definition} dicts
        self.metrics = Metrics()
        self.default_set_path = default_set_path or 'sets/Test Set B - Italian.csv'
        # Don't load here - wait for on_enter() to ensure fresh session each time

    def load_study_set(self, csv_file_path):
        '''
        Load a study set from a CSV file and reset to first card
        '''
        try:
            # If this set is already loaded and cards exist, don't reload it.
            if self.current_set and getattr(self.current_set, 'path', None) == csv_file_path and self.cards:
                return
            self.current_set = Set.from_file(csv_file_path)
            # Convert _Entry objects to dicts
            self.cards = [{'term': card.term, 'definition': card.definition} 
                          for card in self.current_set.data]
            self.total_cards = len(self.cards)
            self.current_card_index = 0
            self.metrics = Metrics()  # Reset metrics for new session
            self.metrics.load_from_csv(csv_file_path)
            self.metrics.start_study_session()
            self._load_current_card()
        except Exception as e:
            print(f"Error loading study set: {e}")

    def _load_current_card(self):
        '''
        Display the card at the current index
        '''
        if 0 <= self.current_card_index < len(self.cards):
            card = self.cards[self.current_card_index]
            # Check if ids and card_widget are available (widget tree built)
            if hasattr(self, 'ids') and 'card_widget' in self.ids:
                self.ids.card_widget.load_card(card['term'], card['definition'])
            else:
                # Schedule update for next frame if widget not ready yet
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self._load_current_card(), 0.1)

    def next_card(self):
        '''
        Move to the next card; return True if there are more, False if at end
        '''
        if self.current_card_index < len(self.cards) - 1:
            self.current_card_index += 1
            self._load_current_card()
            return True
        return False

    def prev_card(self):
        '''
        Move to the previous card; return True if there are more, False if at start
        '''
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self._load_current_card()
            return True
        return False

    def record_answer_correct(self):
        '''
        Record that the current card was answered correctly
        '''
        if 0 <= self.current_card_index < len(self.cards):
            term = self.cards[self.current_card_index]['term']
            self.metrics.record_answer(term, correct=True)

    def record_answer_incorrect(self):
        '''
        Record that the current card was answered incorrectly
        '''
        if 0 <= self.current_card_index < len(self.cards):
            term = self.cards[self.current_card_index]['term']
            self.metrics.record_answer(term, correct=False)

    def end_study_session(self):
        '''
        End the study session and navigate to metrics screen
        '''
        metrics = self.metrics.get_metrics()
        # Persist session metrics to all-time stats via StatsTracker
        try:
            from tracker import StatsTracker
            tracker = StatsTracker()
            # Extract set name from path (e.g., "sets/Test Set B - Italian.csv" -> "Test Set B - Italian.csv")
            set_name = getattr(self.current_set, 'path', 'unknown').split('/')[-1]
            tracker.update_stats(set_name, metrics)
        except Exception as e:
            print(f"Error updating tracker: {e}")
        
        # Display session metrics
        metrics_screen = App.get_running_app().root.get_screen('metrics')
        metrics_screen.set_metrics(metrics)
        # Navigate to metrics screen
        App.get_running_app().root.current = 'metrics'

    def back_to_menu(self):
        '''
        End the study session timer and return to main menu without showing metrics
        '''
        # End the session to stop the timer and finalize time tracking
        self.metrics.end_study_session()
        # Reset cards so next study session loads fresh
        self.cards = []
        # Navigate to menu
        App.get_running_app().root.current = 'menu' 

    def flip_card(self):
        '''
        Flip the current card (delegate to CardWidget)
        '''
        if hasattr(self, 'ids') and 'card_widget' in self.ids:
            self.ids.card_widget.flip_card()

    def on_enter(self):
        '''
        Called when screen is displayed. Always reset and reload the study set for a fresh session.
        '''
        try:
            # Only load the default set if no cards are already loaded.
            # When a set is selected from the SetSelectScreen it calls
            # `card_screen.load_study_set(path)` before switching to this
            # screen, so we must not overwrite that selection here.
            if not self.cards:
                self.load_study_set(self.default_set_path)
        except Exception as e:
            print(f"Error loading study set on screen enter: {e}")


class MetricsScreen(MDScreen):
    '''
    A screen to display study session metrics and results.
    Shows accuracy, time spent, problem areas, and overall performance.
    '''
    metrics_data = ObjectProperty(None, allow_none=True)

    def set_metrics(self, metrics_dict):
        '''
        Set the metrics data to display
        '''
        self.metrics_data = metrics_dict
        self._update_display()

    def _update_display(self):
        '''
        Update the display with current metrics data
        '''
        if self.metrics_data and hasattr(self, 'ids'):
            # Update labels with metrics
            if 'accuracy_label' in self.ids:
                accuracy = self.metrics_data.get('Accuracy (%)', 0)
                self.ids.accuracy_label.text = f"Accuracy: {accuracy:.1f}%"
            
            if 'total_label' in self.ids:
                total = self.metrics_data.get('Total Answers', 0)
                correct = self.metrics_data.get('Correct Answers', 0)
                incorrect = self.metrics_data.get('Incorrect Answers', 0)
                self.ids.total_label.text = f"Correct: {correct} | Incorrect: {incorrect} | Total: {total}"
            
            if 'time_label' in self.ids:
                time_spent = self.metrics_data.get('Total Time Spent (s)', 0)
                minutes = int(time_spent // 60)
                seconds = int(time_spent % 60)
                self.ids.time_label.text = f"Time Spent: {minutes}m {seconds}s"
            
            if 'problem_areas_label' in self.ids:
                problem_areas = self.metrics_data.get('Problem Areas', [])
                if problem_areas:
                    problem_text = "Problem Areas (most incorrect first):\n"
                    for term, count in problem_areas[:5]:  # Show top 5
                        problem_text += f"  • {term}: {count} incorrect\n"
                    self.ids.problem_areas_label.text = problem_text
                else:
                    self.ids.problem_areas_label.text = "No problem areas - Great job!"

    def on_enter(self):
        '''
        Called when screen is displayed. Ensure metrics are displayed.
        '''
        self._update_display()

    def return_to_menu(self):
        '''
        Return to main menu
        '''
        from kivy.app import App
        App.get_running_app().root.current = 'menu'