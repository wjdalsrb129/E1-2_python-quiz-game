"""프로그램 실행 진입점"""

from quiz_game import QuizGame


def main():
    game = QuizGame()

    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Ctrl+C 입력으로 프로그램을 중단합니다.")
        exit_safely(game)
    except EOFError:
        print("\n\n⚠️ 입력이 종료되어(EOF) 프로그램을 중단합니다.")
        exit_safely(game)


def exit_safely(game):
    """현재 데이터를 저장한 뒤 종료 메시지를 출력한다."""
    if game.save_state():
        print("💾 현재까지의 데이터를 저장했습니다.")
    print("👋 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()