import random
import decimal
import time
import csv
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Assessment:
    def __init__(self):
        self.section1 = {}
        self.section2 = {}
        self.section3 = {}
        self.history = []
        self.performance_file = "assessment_performance.csv"

        self._init_questions()
        self.performance_data = self._load_performance_data()

    def assess(self, section=None):
        """ This runs the test. Choose section or leave it at None to do the full test. """
        print('Wait 5 seconds...')
        time.sleep(5)
        self.history = []
        print('Starting test...')
        start_time = time.time()
        points = 0

        if section is None or section == 1:
            print('Section 1')
            for i, q in enumerate(self.section1['questions']):
                res = self._ask_question(q, self.section1['answers'][i], 1)
                if res is not None:
                    points += 1 if res else -3

            section1_end_time = time.time()
            section1_time = section1_end_time - start_time
            print('Section 1 took {:.1f}s'.format(section1_time))
            print('Points: {} / 30'.format(points))
            section1_points = points

        if section is None or section == 2:
            print('Section 2')
            for i, q in enumerate(self.section2['questions']):
                res = self._ask_question(q, self.section2['answers'][i], 2)
                if res is not None:
                    points += 2 if res else -1

            section2_end_time = time.time()

            if section is None:
                section2_time = section2_end_time - section1_end_time
                print('Section 2 took {:.1f}s... test so far took {:.1f}s'.format(section2_time, section2_end_time - start_time))
                print('Points: {} / 60'.format(points - section1_points))
                print('Total points: {} / 90'.format(points))
                section2_points = points
            else:
                print('Test took {:.1f}s'.format(section2_end_time - start_time))
                print('Points: {} / 60'.format(points))

        if section is None or section == 3:
            print('Section 3')
            for i, q in enumerate(self.section3['questions']):
                res = self._ask_question(q, self.section3['answers'][i], 3, choices=self.section3['choices'][i])
                if res is not None:
                    points += 2 if res else -2

            end_time = time.time()

            if section is None:
                section3_time = end_time - section2_end_time
                print('Section 3 took {:.1f}s... test took {:.1f}s'.format(section3_time, end_time - start_time))
                print('Points: {} / 30'.format(points - section2_points))
                print('Total points: {} / 120'.format(points))
                print('Test passed' if points >= 72 else 'Test failed')
            else:
                print('Test took {:.1f}s'.format(end_time - start_time))
                print('Points: {} / 60'.format(points))

        self.print_history()
        self._save_performance(points, end_time - start_time)
        self._plot_performance()
        self._plot_insights()

    def print_history(self):
        """ Print the history of the test with details of each question. """
        sect = 0
        correct_count = 0
        valid_q_count = 0
        tot_time = 0

        for i, q in enumerate(self.history):
            if q['section'] > sect:
                sect = q['section']
                print('Section {}'.format(sect))

            if q['correct'] is not None:
                tot_time += q['time']
                valid_q_count += 1
                correct_count += 1 if q['correct'] else 0

            print('{}| Correct: {} | Time: {:.1f} | Q: {} | A: {} | Given A: {}'.format(
                i, q['correct'], q['time'], q['question'], q['answer'], q['user answer']))

        print('{} / {} questions answered correctly'.format(correct_count, valid_q_count))
        print('Total test time: {:.1f}s, Average question time: {:.1f}s'.format(tot_time, tot_time / valid_q_count))

    def _ask_question(self, question, answer, section, choices=None):
        """ Ask a question and record the response and time taken. """
        question_start_time = time.time()

        if section < 3:
            user_answer = input(question + ' = ')
            if user_answer != 'o':
                user_answer = float(user_answer)
        else:
            random.shuffle(choices)
            print(question)
            print(choices)
            user_answer = choices[int(input('1, 2, or 3: ')) - 1]

        time_taken = time.time() - question_start_time

        if not isinstance(user_answer, str):
            result = math.isclose(user_answer, answer, abs_tol=1e-5)
        else:
            result = None

        self.history.append({
            'section': section,
            'correct': result,
            'question': question,
            'user answer': user_answer,
            'answer': answer,
            'time': time_taken
        })

        return result

    def _init_questions(self):
        """ Initialize questions for all sections. """
        # Initialize questions for section 1
        questions = []
        answers = []
        for i in range(30):
            op = random.choice(['-', '+', '*', '/'])
            if op == '/' or op == '*':
                v1 = random.randint(10, 100)
                v2 = random.randint(10, 1000)
                if op == '/':
                    answ = v1 * v2
                    v2 = v1
                    v1 = answ
            else:
                v1 = random.randint(10, 1000)
                v2 = random.randint(10, 10000)
            question = '{} {} {}'.format(v1, op, v2)
            answ = eval(question)
            questions.append(question)
            answers.append(answ)
        self.section1 = {'questions': questions, 'answers': answers}

        # Initialize questions for section 2
        questions = []
        answers = []
        questions.append(self.section2_question_gen(0.5, '*', 0.5, 3, 3, 0.05, 0.05))
        questions.append(self.section2_question_gen(0.002, '*', 40, 3, 3, 0.01, 0.1))
        questions.append(self.section2_question_gen(0.6, '/', 15, 3, 3, [0.6, 1.2, 0.06], [15, 20, 30, 1.5, 12, 1.2]))
        questions.append(self.section2_question_gen(0.1, '-', 0.04, 4, 4, 0.01, 0.08))
        questions.append(self.section2_question_gen(0.012, '*', 40, 3, 3, 0.01, [20, 30, 40, 50, 60]))
        random.shuffle(questions)
        for q in questions:
            answers.append(eval(q))
        self.section2 = {'questions': questions, 'answers': answers}

        # Initialize questions for section 3
        questions = []
        answers = []
        multi_choice = []
        for i in range(15):
            v1 = random.randint(101, 9999)
            v2 = random.randint(101, 9999)
            op = '*'
            question = '{} {} {}'.format(v1, op, v2)
            questions.append(question)
            answ = eval(question)
            answers.append(answ)
            multi_choice.append([answ, self.section3_answer_gen(answ), self.section3_answer_gen(answ)])
        self.section3 = {'questions': questions, 'answers': answers, 'choices': multi_choice}

    def section2_question_gen(self, v1, op, v2, sf1, sf2, lim1, lim2):
        """ Generate questions for section 2 with specific parameters. """
        if isinstance(lim1, list):
            v1 = random.choice(lim1)
        elif sf1 > 0:
            decimal.getcontext().prec = sf1
            v1 = decimal.Decimal(v1) + decimal.Decimal((random.random() - 0.1) * lim1)
        elif sf1 == 0:
            v1 += random.randint(-lim1, lim1)

        if isinstance(lim2, list):
            v2 = random.choice(lim2)
        elif sf2 > 0:
            decimal.getcontext().prec = sf2
            v2 = decimal.Decimal(v2) + decimal.Decimal((random.random() - 0.1) * lim2)
        else:
            v2 += random.randint(-lim2, lim2)

        return '{} {} {}'.format(v1, op, v2)

    def section3_answer_gen(self, answer):
        """ Generate multiple choice answers for section 3. """
        var = 0
        while var == 0:
            var = random.randint(-10, 10)
        return random.choice([answer + 10 * var, answer + var])

    def _save_performance(self, points, total_time):
        """ Save the performance data to a CSV file. """
        header = ['Points', 'Total Time', 'Date Time']
        file_exists = os.path.isfile(self.performance_file)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(self.performance_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(header)
            writer.writerow([points, total_time, current_time])

    def _load_performance_data(self):
        """ Load the performance data from a CSV file. """
        if not os.path.isfile(self.performance_file):
            return []
        with open(self.performance_file, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def _plot_performance(self):
        """ Plot the performance data over time. """
        if not self.performance_data:
            return
        points = [int(row['Points']) for row in self.performance_data]
        total_times = [float(row['Total Time']) for row in self.performance_data]
        sessions = list(range(1, len(points) + 1))
        average_score = np.mean(points) * np.ones(len(points))

        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        # Plot points over sessions
        axs[0, 0].plot(sessions, points, label='Points', marker='o')
        axs[0, 0].plot(sessions, average_score, label='Average Score', linestyle='--', color='red')
        axs[0, 0].set_xlabel('Session')
        axs[0, 0].set_ylabel('Points')
        axs[0, 0].set_title('Assessment Performance Over Time')
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        # Plot total time per session
        axs[0, 1].plot(sessions, total_times, label='Total Time', marker='o', color='green')
        axs[0, 1].set_xlabel('Session')
        axs[0, 1].set_ylabel('Total Time (s)')
        axs[0, 1].set_title('Total Time per Session')
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        # Plot correct answers per section
        correct_answers_section1 = sum(1 for q in self.history if q['section'] == 1 and q['correct'])
        correct_answers_section2 = sum(1 for q in self.history if q['section'] == 2 and q['correct'])
        correct_answers_section3 = sum(1 for q in self.history if q['section'] == 3 and q['correct'])
        sections = ['Section 1', 'Section 2', 'Section 3']
        correct_answers = [correct_answers_section1, correct_answers_section2, correct_answers_section3]
        axs[1, 0].bar(sections, correct_answers, color=['blue', 'orange', 'green'])
        axs[1, 0].set_xlabel('Sections')
        axs[1, 0].set_ylabel('Correct Answers')
        axs[1, 0].set_title('Correct Answers per Section')
        axs[1, 0].grid(True)

        # Plot average time per question
        times_per_question = [float(row['Total Time']) / len(self.history) for row in self.performance_data]
        average_time_per_question = np.mean(times_per_question)
        axs[1, 1].plot(list(range(1, len(times_per_question) + 1)), times_per_question, label='Time per Question', marker='o')
        axs[1, 1].axhline(average_time_per_question, color='red', linestyle='--', label='Average Time per Question')
        axs[1, 1].set_xlabel('Session')
        axs[1, 1].set_ylabel('Time per Question (s)')
        axs[1, 1].set_title('Average Time per Question Over Sessions')
        axs[1, 1].legend()
        axs[1, 1].grid(True)

        plt.tight_layout()
        plt.show()

    def _plot_insights(self):
        """ Plot insights such as performance metrics and weak spots. """
        if not self.performance_data:
            return

        # Calculate average time per question
        times_per_question = [float(row['Total Time']) / len(self.history) for row in self.performance_data]
        average_time_per_question = np.mean(times_per_question)

        # Calculate correct answers per section
        correct_answers_section1 = sum(1 for q in self.history if q['section'] == 1 and q['correct'])
        correct_answers_section2 = sum(1 for q in self.history if q['section'] == 2 and q['correct'])
        correct_answers_section3 = sum(1 for q in self.history if q['section'] == 3 and q['correct'])

        sections = ['Section 1', 'Section 2', 'Section 3']
        correct_answers = [correct_answers_section1, correct_answers_section2, correct_answers_section3]

        # Plot correct answers per section
        plt.figure(figsize=(12, 6))
        plt.bar(sections, correct_answers, color=['blue', 'orange', 'green'])
        plt.xlabel('Sections')
        plt.ylabel('Correct Answers')
        plt.title('Correct Answers per Section')
        plt.grid(True)
        plt.show()

        # Plot average time per question
        plt.figure(figsize=(12, 6))
        plt.plot(list(range(1, len(times_per_question) + 1)), times_per_question, label='Time per Question', marker='o')
        plt.axhline(average_time_per_question, color='red', linestyle='--', label='Average Time per Question')
        plt.xlabel('Session')
        plt.ylabel('Time per Question (s)')
        plt.title('Average Time per Question Over Sessions')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    assessment = Assessment()
    try:
        assessment.assess(section=None)
    except Exception as e:
        print(e)
        print(assessment.history)
