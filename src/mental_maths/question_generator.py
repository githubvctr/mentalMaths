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
        """ 
        Generate 30 varied questions, including multiplication, addition, subtraction, and division.
        Multiplication uses different digit-lengths (3×2, 2×2, 4×2, 4×3).
        """
        questions, answers = [], []
        for _ in range(30):
            op = random.choice(['+', '-', '*', '/'])  # Now includes all four operations
            
            if op == '*':
                pattern = random.choice([(3,2), (2,2), (4,2), (4,3)])  # Different digit-length multiplications
                v1 = random.randint(10**(pattern[0]-1), 10**pattern[0]-1)
                v2 = random.randint(10**(pattern[1]-1), 10**pattern[1]-1)
                answer = v1 * v2
            
            elif op == '+':
                v1 = random.randint(100, 9999)  # Random numbers for addition
                v2 = random.randint(100, 9999)
                answer = v1 + v2
            
            elif op == '-':
                v1 = random.randint(100, 9999)  # Ensure non-negative results
                v2 = random.randint(100, v1)  # v2 is always ≤ v1
                answer = v1 - v2
            
            elif op == '/':
                v2 = random.randint(2, 20)  # Simple divisors for cleaner results
                answer = random.randint(10, 500)  # Ensure a valid quotient
                v1 = answer * v2  # Ensure division is exact
                answer = v1 / v2  # Avoiding remainders
            
            question = f"{v1} {op} {v2}"
            questions.append(question)
            answers.append(answer)
        
        return questions, answers

    def _generate_section2(self):
        """ 
        Generate 10 decimal-based questions with varied arithmetic operations.
        Includes multiplication, division, addition, and subtraction.
        """
        questions, answers = [], []
        for _ in range(10):
            v1 = round(random.uniform(0.1, 99.9), random.choice([1, 2]))  # Random decimals with 1 or 2 decimal places
            v2 = round(random.uniform(0.1, 99.9), random.choice([1, 2]))  
            op = random.choice(['-', '+', '*', '/'])
            
            # Ensure valid division by avoiding divide by zero
            if op == '/':
                v1 = round(v1 * v2, 2)  # Ensure division results in a simpler number
                answer = round(v1 / v2, 2)
            else:
                answer = round(eval(f"{v1} {op} {v2}"), 2)
            
            question = f"{v1} {op} {v2}"
            questions.append(question)
            answers.append(answer)
        
        return questions, answers

    def _generate_section3(self):
        """ 
        Generate 10 multiple-choice multiplication questions.
        The answer choices include the correct answer and two incorrect but close alternatives.
        """
        questions, answers, choices = [], [], []
        for _ in range(10):
            v1, v2 = random.randint(101, 999), random.randint(11, 99)  # Ensuring more reasonable multiplications
            question = f"{v1} × {v2}"
            answer = v1 * v2

            # Create choices (correct + two incorrect)
            choices_set = [answer, 
                           answer + random.randint(10, 100), 
                           answer - random.randint(10, 100)]
            random.shuffle(choices_set)

            questions.append(question)
            answers.append(answer)
            choices.append(choices_set)

        return questions, answers, choices
