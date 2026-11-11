"""개별 퀴즈를 표현하는 Quiz 클래스"""


class Quiz:
    """문제 1개와 선택지 4개, 정답 번호를 관리하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list[str])
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 함께 문제와 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True, 아니면 False를 반환한다."""
        return user_answer == self.answer

    def to_dict(self):
        """state.json에 저장할 수 있도록 dict로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json에서 읽어 온 dict로 Quiz 객체를 만든다."""
        return cls(data["question"], data["choices"], data["answer"])