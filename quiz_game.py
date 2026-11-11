"""퀴즈 게임 전체를 관리하는 QuizGame 클래스"""

LINE = "=" * 40
MENU_MIN = 1
MENU_MAX = 5


class QuizGame:
    """메뉴 표시, 입력 처리, 기능 분기를 담당하는 클래스"""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.best_correct = 0
        self.best_total = 0

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
        """퀴즈 풀기 (6단계에서 구현)"""
        print("\n🚧 퀴즈 풀기 기능은 준비 중입니다.")

    def add_quiz(self):
        """퀴즈 추가 (7단계에서 구현)"""
        print("\n🚧 퀴즈 추가 기능은 준비 중입니다.")

    def list_quizzes(self):
        """퀴즈 목록 (8단계에서 구현)"""
        print("\n🚧 퀴즈 목록 기능은 준비 중입니다.")

    def show_score(self):
        """점수 확인 (9단계에서 구현)"""
        print("\n🚧 점수 확인 기능은 준비 중입니다.")