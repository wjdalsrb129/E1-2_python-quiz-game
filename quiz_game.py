"""퀴즈 게임 전체를 관리하는 QuizGame 클래스"""

import json
from pathlib import Path

from quiz import CHOICE_COUNT, Quiz

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_QUIZ_PATH = BASE_DIR / "default_quizzes.json"
STATE_PATH = BASE_DIR / "state.json"
BACKUP_PATH = BASE_DIR / "state.json.bak"
TEMP_PATH = BASE_DIR / "state.json.tmp"

LINE = "=" * 40
SEPARATOR = "-" * 40
MENU_MIN = 1
MENU_MAX = 5


class QuizGame:
    """메뉴 진행, 퀴즈 기능, 점수 기록, 입력 처리, 데이터 저장/불러오기를 담당하는 클래스"""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.best_correct = 0
        self.best_total = 0
        self.load_state()

    # ------------------------------------------------------------
    # 1. 메뉴 진행
    # ------------------------------------------------------------
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
                self.save_state()
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

    # ------------------------------------------------------------
    # 2. 퀴즈 기능 (풀기 / 추가 / 목록 / 점수 확인)
    # ------------------------------------------------------------
    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고, 결과와 최고 점수 갱신 여부를 알려 준다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            if self.ask_question(number, quiz):
                correct += 1

        score = self.calculate_score(correct, total)
        is_new_record = self.update_best_score(score, correct, total)
        if is_new_record:
            self.save_state()
        self.show_result(score, correct, total, is_new_record)

    def ask_question(self, number, quiz):
        """문제 1개를 출제하고 정답을 입력받아, 맞혔으면 True를 반환한다."""
        print()
        print(SEPARATOR)
        quiz.display(number)
        user_answer = self.get_number_input("정답 입력: ", 1, CHOICE_COUNT)

        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            return True

        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 {quiz.get_answer_text()}입니다.")
        return False

    def show_result(self, score, correct, total, is_new_record):
        """퀴즈 결과를 출력한다."""
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if is_new_record:
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

    def add_quiz(self):
        """문제, 선택지, 정답 번호를 입력받아 새 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = self.get_text_input("문제를 입력하세요: ")

        choices = []
        for number in range(1, CHOICE_COUNT + 1):
            choice = self.get_text_input(f"선택지 {number}: ")
            choices.append(choice)

        answer = self.get_number_input(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print(f"\n✅ 퀴즈가 추가되었습니다! (현재 총 {len(self.quizzes)}개)")

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 번호와 함께 출력한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(SEPARATOR)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(SEPARATOR)

    def show_score(self):
        """최고 점수를 출력한다. 아직 퀴즈를 푼 기록이 없으면 안내한다."""
        if self.best_total == 0:
            print("\n⚠️ 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어 보세요.")
            return

        print(
            f"\n🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )

    # ------------------------------------------------------------
    # 3. 점수 계산 / 최고 점수 기록
    # ------------------------------------------------------------
    def calculate_score(self, correct, total):
        """맞힌 개수와 전체 문제 수로 100점 만점 점수를 계산한다.

        정답률 × 100을 사사오입 반올림한 정수를 반환한다.
        (Python의 round()는 .5를 짝수 쪽으로 보내므로 사용하지 않는다.)
        """
        if total == 0:
            return 0
        return int(correct * 100 / total + 0.5)

    def update_best_score(self, score, correct, total):
        """이번 점수가 최고 점수보다 높으면 기록을 갱신하고 True를 반환한다.

        첫 기록(best_total == 0)이면 점수와 관계없이 기록한다.
        """
        if self.best_total == 0 or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            return True
        return False

    # ------------------------------------------------------------
    # 4. 입력 처리 (검증)
    # ------------------------------------------------------------
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

    def get_text_input(self, prompt):
        """빈 값이 아닌 문자열을 입력받아 앞뒤 공백을 제거해 반환한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
                continue
            return text

    # ------------------------------------------------------------
    # 5. 데이터 불러오기 / 저장
    # ------------------------------------------------------------
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
        except (ValueError, KeyError, TypeError):
            print("⚠️ 기본 퀴즈 파일(default_quizzes.json)이 손상되어 읽을 수 없습니다.")
        except OSError:
            print("⚠️ 기본 퀴즈 파일(default_quizzes.json)을 읽는 중 오류가 발생했습니다.")

        return []

    def load_state(self):
        """state.json에서 퀴즈 목록과 최고 점수를 불러온다.

        - 파일이 없으면(첫 실행) 기본 퀴즈로 시작한다.
        - 파일이 손상되었으면 state.json.bak으로 백업한 뒤 기본 퀴즈로 복구한다.
        - 파일을 읽을 수 없으면(권한 문제 등) 기본 퀴즈로 시작하되 파일은 건드리지 않는다.
        """
        if not STATE_PATH.exists():
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = self.load_default_quizzes()
            return

        try:
            with open(STATE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = []
            for item in data["quizzes"]:
                quizzes.append(Quiz.from_dict(item))

            best_score = data["best_score"]
            best_correct = data["best_correct"]
            best_total = data["best_total"]
            self.validate_best_record(best_score, best_correct, best_total)

        except (ValueError, KeyError, TypeError):
            # ValueError에는 JSON 문법 오류(JSONDecodeError)와 인코딩 오류도 포함된다.
            print("⚠️ 저장 파일(state.json)이 손상되었습니다.")
            self.backup_broken_state()
            print("🔄 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = self.load_default_quizzes()
            self.save_state()
            return

        except OSError:
            print("⚠️ 저장 파일(state.json)을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = self.load_default_quizzes()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total
        print(
            f"📂 저장된 데이터를 불러왔습니다. "
            f"(퀴즈 {len(self.quizzes)}개, 최고 점수 {self.best_score}점)"
        )

    def validate_best_record(self, best_score, best_correct, best_total):
        """최고 점수 기록 값이 올바른지 확인하고, 아니면 ValueError를 발생시킨다."""
        for value in (best_score, best_correct, best_total):
            if type(value) is not int or value < 0:
                raise ValueError("최고 점수 기록은 0 이상의 정수여야 합니다.")
        if best_score > 100 or best_correct > best_total:
            raise ValueError("최고 점수 기록의 값이 올바르지 않습니다.")

    def backup_broken_state(self):
        """손상된 state.json을 state.json.bak으로 옮겨 보관한다."""
        try:
            STATE_PATH.replace(BACKUP_PATH)
            print("💾 손상된 파일은 state.json.bak으로 백업했습니다.")
        except OSError:
            print("⚠️ 손상된 파일을 백업하지 못했습니다.")

    def save_state(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다.

        임시 파일(state.json.tmp)에 먼저 쓴 뒤 state.json과 교체하여,
        저장 도중 오류가 나도 기존 state.json이 손상되지 않도록 한다.
        저장에 성공하면 True, 실패하면 False를 반환한다.
        """
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }

        try:
            with open(TEMP_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            TEMP_PATH.replace(STATE_PATH)
            return True
        except OSError:
            print("⚠️ 데이터를 저장하지 못했습니다. (state.json 쓰기 오류)")
            return False