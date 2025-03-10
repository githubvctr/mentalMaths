from mental_maths.question_generator import QuestionGenerator
from mental_maths.performance_tracker import PerformanceTracker
import time

class Assessment:
    def __init__(self, question_generator: QuestionGenerator):
        self.question_generator = question_generator
        self.history = []
        self.performance_file = "data/assessment_performance.csv"
        self.performance_tracker = PerformanceTracker(self.performance_file)

    def assess(self, sections=None):
        print("Wait 5 seconds...")
        time.sleep(5)
        print("Starting test...")
        start_time = time.time()
        self.history = []
        total_points = 0

        sections_to_run = sections if sections is not None else [1, 2, 3]

        for sec in sections_to_run:
            questions, answers, choices = self.question_generator.generate_questions(sec)
            total_points += self._run_section(sec, questions, answers, choices)

        total_time = time.time() - start_time

        self.performance_tracker.save_performance(total_points, total_time, self.history)
        self.performance_tracker.plot_performance()
        self.performance_tracker.plot_insights(self.history)

    def _run_section(self, sec, questions, answers, choices):
        points = 0
        print(f"Section {sec}")
        for question, answer in zip(questions, answers):
            result = self.question_generator.ask_question(question, answer, sec, choices)
            points_awarded = self._calculate_points(sec, result['correct'])
            points += points_awarded
            self.history.append(result)

        return points

    def _calculate_points(self, section, correct):
        points_table = {
            1: (1, -3),
            2: (2, -1),
            3: (2, -2)
        }
        return points_table[section][0] if correct else points_table[section][1]
