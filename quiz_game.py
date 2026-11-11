"""퀴즈 게임 전체를 관리하는 QuizGame 클래스"""

import json
from pathlib import Path

from quiz import Quiz

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_QUIZ_PATH = BASE_DIR / "default_quizzes.json"

LINE = "=" * 40
MENU_MIN = 1
MENU_MAX = 5


class QuizGame:
    """메뉴 표시, 입력 처리, 기능 분기를 담당하는 클래스"""

    def __init__(self):
        self.quizzes = self.load_default_quizzes()
        self.best_score = 0
        self.best_correct = 0
        self.best_total = 0

    def load_default_quizzes(self):
        """default_quizzes.json에서 기본 퀴즈를 읽어 Quiz 객체 리스트로 반환한다.

        파일이 없거나 손상된 경우 안내 메시지를 출력하고 빈 리스트를 반환한다.
        """
        try:
            with open(DEFAULT_QUIZ_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = []
            for item in data["quizzes"]:
                quizzes.append(Quiz.from_dict(item))
            return quizzes

        except FileNotFoundError:
            print("⚠️ 기본 퀴즈 파일(default_quizzes.json)을 찾을 수 없습니다.")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("⚠️ 기본 퀴즈 파일(default_quizzes.json)이 손상되어 읽을 수 없습니다.")
        except OSError:
            print("⚠️ 기본 퀴즈 파일(default_quizzes.json)을 읽는 중 오류가 발생했습니다.")

        return []

    def run(self):
        """메뉴를 반복해서 보여 주고, 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.get_number_input("선택: ", MENU_MIN, MENU_MAX)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("\n👋 프로그램을 종료합니다.")
                break

    def show_menu(self):
        """메뉴를 출력한다."""
        print()
        print(LINE)
        print("        🎯 Python & Git 개념 퀴즈 🎯")
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def get_number_input(self, prompt, min_value, max_value):
        """min_value~max_value 범위의 정수를 입력받아 반환한다.

        공백 제거, 빈 입력, 숫자 변환 실패, 범위 밖 입력을 처리하고
        올바른 값이 들어올 때까지 다시 입력받는다.
        """
        while True:
            user_input = input(prompt).strip()

            if user_input == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue

            try:
                number = int(user_input)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if number < min_value or number > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 정답/오답을 알려 준다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print()
            print("-" * 40)
            quiz.display(number)
            user_answer = self.get_number_input("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                answer_text = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 {answer_text}입니다.")

        score = self.calculate_score(correct, total)

        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE)

    def calculate_score(self, correct, total):
        """맞힌 개수와 전체 문제 수로 100점 만점 점수를 계산한다.

        정답률 × 100을 사사오입 반올림한 정수를 반환한다.
        (Python의 round()는 .5를 짝수 쪽으로 보내므로 사용하지 않는다.)
        """
        if total == 0:
            return 0
        return int(correct * 100 / total + 0.5)

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = self.get_text_input("문제를 입력하세요: ")

        choices = []
        for number in range(1, 5):
            choice = self.get_text_input(f"선택지 {number}: ")
            choices.append(choice)

        answer = self.get_number_input("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print(f"\n✅ 퀴즈가 추가되었습니다! (현재 총 {len(self.quizzes)}개)")

    def get_text_input(self, prompt):
        """빈 값이 아닌 문자열을 입력받아 앞뒤 공백을 제거해 반환한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
                continue
            return text

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 번호와 함께 출력한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        """점수 확인 (9단계에서 구현)"""
        print("\n🚧 점수 확인 기능은 준비 중입니다.")