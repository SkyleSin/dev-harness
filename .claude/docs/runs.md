# 실행 산출물 — 계약

`work-orchestrator` 하네스의 실행 산출물 규약. 산출물은 하네스 저장소가 아니라 환경별 지식 저장소(`knowledge/`)에 쌓인다.

## 폴더

```
knowledge/
├── runs/{YYYYMMDD}-{TARGET_SLUG}-{slug}/   한 번의 실행 (실행마다 폴더가 따로 생긴다)
└── baselines/{TARGET_SLUG}/                 대상별 테스트 baseline (실행 사이에 공유)
```

`TARGET_SLUG` 는 대상 폴더의 `/` 를 `-` 로 바꾼 값이다 (`apps/service-a` → `apps-service-a`). 실행 폴더는 옮기거나 지우지 않고 그대로 쌓는다.

## 실행 폴더의 파일 지도

| 파일 | 만드는 역할 | 다음 읽는 역할 | 재사용 |
| --- | --- | --- | --- |
| `status.md` | orchestrator | orchestrator | 진행 상태, 재개·부분 재실행의 기준 |
| `00-input.md` | orchestrator | 전원 | 요청 정리, `regression_mode` (60줄 이하, 긴 자료는 경로만 적는다) |
| `01-design.md` | work-architect | implementer, tester, reviewer | 설계 정본. 여러 단계면 맨 앞에 '단계별 읽기 범위' 표 |
| `design.md` | work-architect | Gate 1 사용자 | `01-design.md` 에서 뽑아 쓴 읽기용 요약 (80줄 안팎) |
| `decisions.md` | architect·orchestrator(항목 등록) + 사용자(답) + Claude(답변·체크) | architect, 사용자, 이후 전원 | 결정·승인 요청과 답변 기록 (양식: '결정과 승인 기록' 절) |
| `02-implementation.md` | work-implementer | tester, reviewer | 변경 요약 |
| `03-tests.md` | work-tester | reviewer | targeted 테스트 결과 |
| `04-regression.md` | work-tester | reviewer | 전체 회귀 결과 |
| `05-review.md` | work-reviewer | orchestrator(Gate 2) | 최종 판정 |
| `light.md` | orchestrator | 사용자, 다음 실행 | 간단 경로 전용 요약: `final.md` 와 `improvement-log.md` 를 대신한다. 이 경로에는 `01`, `design.md`, `decisions.md`(승인 항목 제외), `05` 가 없다 |
| `final.md` | orchestrator | 사용자, 다음 실행 | 커밋 메시지 초안, 변경 요약, 남은 위험, 커밋이 필요한 저장소(코드·`knowledge/`) |
| `improvement-log.md` | orchestrator | 다음 개선 | 프로젝트 문서 갱신 후보, 하네스 개선 아이디어 |

파일 이름에 번호가 있으면 단계 사이를 넘기는 파일이고, 번호가 없는 `design.md`, `decisions.md` 는 사용자가 읽고 답하는 파일이다.

## status.md 양식

```md
mode: subagent
target: apps/service-a
regression_mode: full | skip
path: full | light
created: 2026-10-16 14:00

| step | owner | status | output | updated | note |
```

status 값: `pending` / `in_progress` / `done` / `blocked`(사유 필수) / `skipped`.

## decisions.md 양식

설계 중 생기는 질문과 사용자 결정을 한 파일에 모은다. 설계 문서(`01-design.md`)에는 질문을 쓰지 않고 항목 제목으로만 인용한다.

```md
- [ ] psycopg2 를 pyproject 에 남겨도 될까요?
  - 배경: ... 가 sync 드라이버로 요구합니다 (근거: engine.py:to_sync_url).
  - 권장: 남김.
  -> psycopg2 가 뭔지 알려줘
  - psycopg2 란 ... 이라서 ... 때문에 남기는 것을 권장합니다.
  ->
```

- 항목 제목은 `- [ ] ` 로 시작하는 **대답할 수 있는 질문 한 문장**이다. 값만 적지 않는다 ("포트: 9024" ✗ → "앱 포트를 9024 로 해도 될까요?" ✓).
- `  - ` 로 시작하는 줄은 **Claude** 발언 (배경, 권장, 설명, 답변). `  ->` 로 시작하는 줄은 **사용자** 발언 (답, 질문, 결정). 서로의 줄은 고치지 않고 아래에 이어 쓴다.
- 항목마다 끝에 빈 `  ->` 줄을 둔다. 사용자가 답을 적는 자리다. 사용자가 `->` 로 질문하면 Claude 가 그 아래에 `  - ` 줄로 답하고 새 빈 `  ->` 줄을 남긴다.
- `[x]` 는 **해결됐다**는 뜻이며 **Claude 가 판단**해서 표시한다. 사용자의 마지막 `->` 가 결정이고 남은 질문·모호함·확인할 사실이 없으면 `[x]`, 하나라도 남으면 `[ ]` 로 두고 이유를 `  - ` 줄에 적는다. `->` 가 빈 칸이면 권장안 수락 신호로 보되 Claude 가 확인한 뒤 확정한다.
- `[x]` 뒤에 사용자가 이의를 적으면 Claude 가 `[ ]` 로 되돌리고 답한다.
- 항목 등록은 architect 가 한다 (사용자가 정해야 하는 결정만). **Claude 가 직접 확인할 수 있는 사실은 항목으로 올리지 않고** 확인해서 근거로 쓴다. 사용자도 같은 형식으로 항목을 추가할 수 있다.
- 설계는 `[x]` 항목만 확정으로 취급한다. `[ ]` 항목은 권장안을 가정하되 설계에 "미확정 (decisions.md: 제목)" 으로 표시한다.
- Gate 1 에서 `[ ]` 항목 목록을 먼저 사용자에게 알린다.

## 결정과 승인 기록

`decisions.md` 는 설계 단계의 질문뿐 아니라 파이프라인 중 사용자에게 받아야 하는 모든 승인과 결정을 담는다. 사용자가 채팅창에서 질문을 찾아 답하지 않고 이 파일에서 한꺼번에 읽고 답하게 하려는 것이다. 문체는 `.claude/rules/user-communication.md` 를 따른다.

항목은 유형 꼬리표를 붙인다. 꼬리표가 없는 기존 항목은 `[결정]` 으로 본다.

| 유형 | 용도 | 제목 형식 | 해결 조건 |
| --- | --- | --- | --- |
| `[결정]` | 방향을 고르는 질문 | `- [ ] [결정] ...할까요?` | 위의 `[x]` 규칙 |
| `[승인]` | 허락 한 건 | `- [ ] [승인] ...을 승인하시겠습니까?` | `->` 줄에 명시적 승인 표현이 있을 때만 `[x]`. 빈 칸은 승인이 아니다 |

등록 주체와 시점:

| 상황 | 등록하는 쪽 | 유형 |
| --- | --- | --- |
| 설계 중 정해야 할 결정 | architect | `[결정]` |
| 설계 승인 (Gate 1) | orchestrator, architect 반환 직후 | `[승인]` |
| 요청 변경으로 기존 승인이 무효가 됨 | orchestrator | `[승인]` (새 항목) |
| 에이전트가 돌려준 "결정 필요", 리뷰어의 "사용자 재확인 요청" | orchestrator | `[결정]` |
| 위험 경고가 있는 회귀 skip 확정, 재작업 두 번째 실패 후 진행 방향, 브리프 애매 확인 | orchestrator | `[결정]` |
| 최초 baseline 제안을 `knowledge/baselines/` 로 옮기기 | orchestrator | `[승인]` |

규칙:

- 항목마다 배경, 선택지(승인이면 "승인 / 수정 요청"), 권장안, 선택에 따른 결과를 `  - ` 줄에 풀어 쓰고 끝에 빈 `  ->` 줄을 둔다.
- 채팅에는 등록했다는 안내와 건수만 쓴다. 질문 내용을 채팅에 되풀이하지 않는다.
- 사용자가 채팅으로 답하면 orchestrator 가 해당 항목의 `->` 줄에 `(채팅 답변, {날짜}) 답 내용` 으로 옮겨 적은 뒤 진행한다. 어느 항목에 대한 답인지 애매하면 확인한다.
- 승인 항목이 `[ ]` 인 동안에는 그 승인이 필요한 단계로 가지 않는다.
- 실행 폴더가 생기기 전의 확인은 파일이 없으므로 채팅으로 한다.

## design.md (읽기용 요약)

- `01-design.md` 가 정본이다. `design.md` 는 `01-design.md` 를 다 쓴 뒤 그 내용에서 뽑아 새로 쓰고, `design.md` 에만 있는 정보는 두지 않는다.
- 설계가 바뀌면 `01-design.md` 를 먼저 고치고 `design.md` 를 다시 쓴다. 사용자는 `design.md` 를 직접 고치지 않고 의견을 `decisions.md` 로 남긴다.
- 80줄 안팎(점검 스크립트는 100줄을 넘으면 경고). 맨 위에 기준(`기준: 01-design.md, {날짜}`), 하는 일, 바뀌는 것, 승인받을 것, 지금 결정할 것(decisions.md 항목 제목, 없으면 "없음"), 구조 표 한 장, 상위 위험과 `확인 필요` 건수, 각 항목의 `01-design.md` 절 링크를 둔다.

## 단계별 읽기 범위

여러 단계로 나뉜 변경은 `01-design.md` 맨 앞에 표를 둔다: 단계, 읽을 절, 대상 파일. Orchestrator 가 뒷단계 에이전트를 부를 때 해당 단계의 절(공통 절 포함)만 읽도록 지정한다. 단계가 하나뿐이면 표를 생략한다.

## baselines

- `failures.txt` — **알려진 실패** 노드 ID. 실패가 0건이면 빈 파일이 정상이다.
- `inventory.txt` — **통과한 전체** 노드 ID. 테스트 소실 감지용.
- 두 파일의 성격을 섞지 않는다. 자세한 규칙은 `regression-run` 스킬.
- 최초 baseline 은 tester 가 직접 저장하지 않고 `{RUN_DIR}/baseline-proposal/` 에 제안으로 만든다. 사용자 승인 뒤 이 폴더로 옮긴다.

## 승인 게이트

- **Gate 1** (`design.md` 와 `decisions.md` 를 보고): `decisions.md` 의 설계 `[승인]` 항목에 사용자가 승인해야 T02 진행.
- **Gate 2** (`05-review.md` 뒤): 리뷰가 pass 여야 `final.md` 진행.
- 승인과 결정 요청은 모두 `decisions.md` 항목으로 등록한다 ('결정과 승인 기록' 절).

## 실패 라우팅

`05-review.md` 의 실패 유형별:

| 유형 | 대상 |
| --- | --- |
| 코드 이슈, 회귀 | implementer 재작업 |
| 테스트 이슈 | tester 재작업 |
| 브리프 애매 | architect + 사용자 |

재작업은 대상별 최대 1회이고 두 번째 실패는 `decisions.md` 에 `[결정]` 항목으로 등록해 사용자에게 알린다.
