import random
import math

class QuestionGenerator:
    def generate_questions(self, section):
        if section == 1:
            questions, answers = self._generate_section1()
            choices = [None] * len(questions)  # Ensure choices is always returned
        elif section == 2:
            questions, answers = self._generate_section2()
            choices = [None] * len(questions)  # Ensure choices is always returned
        elif section == 3:
            questions, answers, choices = self._generate_section3()
        
        return questions, answers, choices  # Always return three values

    def evaluate_answer(self, user_answer, correct_answer, section):
        if section == 3:
            return int(user_answer) == int(correct_answer)
        else:
            try:
                user_answer = float(user_answer)
                correct_answer = float(correct_answer)
                return math.isclose(user_answer, correct_answer, abs_tol=1e-5)
            except ValueError:
                return False

    def _generate_section1(self):
        questions, answers = [], []
        for _ in range(30):
            v1, v2 = random.randint(10, 1000), random.randint(10, 10000)
            op = random.choice(['-', '+', '*', '/'])
            if op == '/':
                ans = v1
                v1 *= v2
            else:
                ans = eval(f"{v1}{op}{v2}")
            questions.append(f"{v1} {op} {v2}")
            answers.append(ans)
        return questions, answers

    def _generate_section2(self):
        questions = ["0.5 * 0.5", "0.002 * 40", "0.6 / 15", "0.1 - 0.04", "0.012 * 40"]
        answers = [eval(q) for q in questions]
        return questions, answers

    def _generate_section3(self):
        questions, answers, choices = [], [], []
        for _ in range(15):
            v1, v2 = random.randint(101, 9999), random.randint(101, 9999)
            q = f"{v1} * {v2}"
            ans = eval(q)
            choices_set = [ans, ans + random.randint(1, 100), ans - random.randint(1, 100)]
            questions.append(q)
            answers.append(ans)
            choices.append(choices_set)
        return questions, answers, choices

