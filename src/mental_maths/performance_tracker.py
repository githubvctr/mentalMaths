# src/mental_maths/performance_tracker.py
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class PerformanceTracker:
    def __init__(self, filepath):
        self.filepath = filepath

    def save_performance(self, points, total_time, history):
        exists = os.path.isfile(self.filepath)
        with open(self.filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            if not exists:
                writer.writerow(['Points', 'Total Time', 'Date Time'])
            writer.writerow([points, total_time, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    def plot_performance(self):
        data = self._load_data()
        if not data:
            return

        points = [int(d['Points']) for d in data]
        sessions = np.arange(1, len(points) + 1)

        plt.figure(figsize=(10, 6))
        plt.plot(sessions, points, marker='o')
        plt.title('Performance Over Time')
        plt.xlabel('Session')
        plt.ylabel('Points')
        plt.grid(True)
        plt.show()

    def plot_insights(self, history):
        sections = ['Section 1', 'Section 2', 'Section 3']
        correct_answers = [
            sum(q['correct'] for q in history if q['section'] == i)
            for i in range(1, 4)
        ]

        plt.bar(sections, correct_answers, color=['blue', 'orange', 'green'])
        plt.title('Correct Answers per Section')
        plt.xlabel('Section')
        plt.ylabel('Correct Answers')
        plt.grid(True)
        plt.show()

    def _load_data(self):
        if not os.path.isfile(self.filepath):
            return []
        with open(self.filepath, 'r') as file:
            return list(csv.DictReader(file))
