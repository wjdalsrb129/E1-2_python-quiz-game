# E1-2
컴퓨터에게 명령 내리는 말(파이썬) 처음 배우기## 6. 파일 구조

```
E1-2_python-quiz-game/
├── main.py                # 프로그램 실행 진입점
├── quiz.py                # Quiz 클래스 (퀴즈 1개를 표현)
├── quiz_game.py           # QuizGame 클래스 (게임 전체 관리)
├── default_quizzes.json   # 기본 퀴즈 원본 (읽기 전용)
├── state.json             # 퀴즈 목록·최고 점수 저장 파일
├── README.md
├── .gitignore
└── docs/
    └── screenshots/       # 실행 화면 캡처
```

## 7. 데이터 파일 설명

### state.json

- **경로**: 프로젝트 루트의 `state.json`
- **인코딩**: UTF-8
- **역할**: 퀴즈 목록과 최고 점수를 저장하여, 프로그램을 다시 실행해도 데이터가 유지되도록 함

#### 스키마

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int | 최고 점수 (0~100). 정답률 × 100을 사사오입 반올림한 정수 |
| `best_correct` | int | 최고 점수 기록 당시 맞힌 문제 수 |
| `best_total` | int | 최고 점수 기록 당시 전체 문제 수 |

#### 예시

```json
{
    "quizzes": [
        {
            "question": "변경한 파일을 다음 커밋에 포함하도록 스테이징 영역에 올리는 Git 명령어는?",
            "choices": ["commit", "add", "push", "init"],
            "answer": 2
        }
    ],
    "best_score": 75,
    "best_correct": 6,
    "best_total": 8
}
```

#### Git 포함 여부

- `state.json`은 `.gitignore`에 넣지 않고 저장소에 포함
- 이유: 저장소를 clone한 사용자도 추가된 퀴즈가 포함된 상태로 바로 실행할 수 있도록 하기 위함

### default_quizzes.json

- **경로**: 프로젝트 루트의 `default_quizzes.json`
- **역할**: 기본 퀴즈 8문제의 원본 데이터. 프로그램이 수정하지 않는 읽기 전용 파일
- **형식**: state.json의 `quizzes`와 동일한 구조
- **코드가 아닌 별도 파일로 분리한 이유**: 문제 내용(데이터)과 프로그램 로직(코드)을 분리하여, 코드를 수정하지 않고도 기본 문제를 바꿀 수 있도록 하기 위함

### 예외 상황 처리

- **state.json이 없는 경우(첫 실행)**: default_quizzes.json의 기본 퀴즈로 시작
- **state.json이 손상된 경우**: 손상된 파일을 `state.json.bak`으로 백업한 뒤, 안내 메시지 출력 후 기본 퀴즈로 복구
- **default_quizzes.json도 없거나 손상된 경우**: 안내 메시지 출력 후 퀴즈 0개로 시작 (퀴즈 추가 기능으로 등록 가능)

## 8. 클래스 설계

> 메서드 이름은 구현 과정에서 변경될 수 있습니다.

### Quiz (quiz.py)

퀴즈 1개를 표현하는 클래스

| 구분 | 이름 | 설명 |
|---|---|---|
| 속성 | `question` | 문제 |
| 속성 | `choices` | 선택지 4개 |
| 속성 | `answer` | 정답 번호 (1~4) |
| 메서드 | `display()` | 문제와 선택지 출력 |
| 메서드 | `is_correct()` | 사용자 입력이 정답인지 확인 |
| 메서드 | `to_dict()` | 저장을 위해 dict로 변환 |
| 메서드 | `from_dict()` | 불러온 dict로 Quiz 객체 생성 |

### QuizGame (quiz_game.py)

게임 전체를 관리하는 클래스

| 구분 | 이름 | 설명 |
|---|---|---|
| 속성 | `quizzes` | Quiz 객체 목록 |
| 속성 | `best_score` / `best_correct` / `best_total` | 최고 점수 기록 |
| 속성 | `state_path` | 저장 파일 경로 |
| 메서드 | `run()` | 메뉴 반복 실행 |
| 메서드 | `show_menu()` | 메뉴 출력 |
| 메서드 | `get_number_input()` | 숫자 입력 공통 처리 (공백 제거, 문자·빈 입력·범위 검증) |
| 메서드 | `play_quiz()` | 퀴즈 풀기 |
| 메서드 | `add_quiz()` | 퀴즈 추가 |
| 메서드 | `list_quizzes()` | 퀴즈 목록 출력 |
| 메서드 | `show_score()` | 최고 점수 확인 |
| 메서드 | `load_state()` | state.json 불러오기 |
| 메서드 | `save_state()` | state.json 저장 |

### 화면 출력 형식

- 퀴즈 결과: `결과: 5문제 중 4문제 정답! (80점)`
- 최고 점수: `최고 점수: 80점 (5문제 중 4문제 정답)`

## 9. 예외 처리 정책

> 작성 예정

## 10. Git 작업 기록

> 작성 예정

## 11. 실행 화면

> 작성 예정

---

# Part 2. 보너스 과제

> 작성 예정

---

# Part 3. 개념 정리

> 작성 예정