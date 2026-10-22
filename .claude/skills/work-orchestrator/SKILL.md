---
name: work-orchestrator
description: workplace 의 대상 폴더(예 apps/service-a, tools/service-b)를 지정한 기능 추가·변경·리팩터링 요청을 설계-구현-테스트-회귀-리뷰 파이프라인으로 처리한다. 초기 실행뿐 아니라 "이어서", "리뷰만 다시", "테스트만 다시", "구현부터 다시", "regression skip 으로 다시", "부분 수정" 같은 재실행 요청도 처리한다. 자연어 예) "apps/service-a 에 X 추가해줘", "service-b 의 Y 리팩터링", "리뷰만 다시 실행". 대상 폴더의 코드 변경이면 한 줄·문구·docstring 수정처럼 작은 요청도 이 스킬을 거치며 직접 편집하지 않는다. 하네스 자체를 고치는 요청은 harness-lab 이 맡는다.
---

# work-orchestrator

## 목적

대상 폴더 하나에 대한 변경 요청을 표준 파이프라인으로 처리한다. 프로젝트 지식을 로드하고, 설계 승인 → 구현 → targeted 테스트 → 회귀 → 리뷰 → 마무리 순으로 서브에이전트를 한 단계씩 호출한다. 도메인 지식은 이 스킬이 아니라 `knowledge/docs/{대상}/` 에 있다.

## 실행 모드

**Subagent 순차 파이프라인.** `Agent` 도구로 `work-architect`, `work-implementer`, `work-tester`, `work-reviewer` 를 한 번에 하나씩 호출하고 단계 사이는 `RUN_DIR` 의 파일로 넘긴다. `TeamCreate`, `Task*`, `SendMessage` 는 쓰지 않는다. `Agent` 도구가 보이지 않으면 우회하지 말고 사용자에게 보고하고 멈춘다.

서브에이전트는 사용자에게 직접 질문할 수 없다. 질문·승인(Gate)은 모두 이 스킬이 메인 대화에서 중계한다.

## 경로 규약

| 이름 | 값 |
| --- | --- |
| `TARGET` | 대상 폴더, workplace 기준 (예 `apps/service-a`) |
| `TARGET_SLUG` | `/` → `-` (예 `apps-service-a`) |
| `RUN_DIR` | `knowledge/runs/{YYYYMMDD}-{TARGET_SLUG}-{slug}/` (파일 지도와 양식: `.claude/docs/runs.md`) |
| 프로젝트 지식 | `knowledge/docs/{TARGET}/overview.md`, `rules.md` (자세한 규약은 `project-context-loader`) |
| baseline | `knowledge/baselines/{TARGET_SLUG}/failures.txt`, `inventory.txt` |
| 커밋 규칙 | `.claude/rules/commit.md` |

## 진입 확인

1. **대상 폴더**: 요청에서 `TARGET` 을 뽑는다. 없거나 애매하면 임의로 고르지 않고 사용자에게 묻는다. 폴더 존재를 확인한다. 요청이 여러 대상에 걸치면 대상별로 따로 실행하자고 안내한다.
2. **프로젝트 지식**: `knowledge/` 가 없으면 workplace `README.md` 의 셋업 절차를 안내하고 멈춘다. `knowledge/docs/{TARGET}/overview.md` 가 없으면 파이프라인을 시작하지 않고 "이 대상은 하네스에 등록되지 않았습니다. `project-onboarding` 을 먼저 실행하시겠어요?" 로 안내한다.
3. **regression_mode**: 요청에서 `regression skip`, `no regression`, `quick` 마커를 찾으면 `skip`, 아니면 `full`.
4. **기존 실행**: `knowledge/runs/` 에서 같은 `TARGET_SLUG` 의 실행 폴더와 `status.md` 를 찾는다.
   - 미완료 실행이 있으면 "이어서 / 부분 재실행 / 새 실행" 중 확인한다.
   - 재실행 키워드를 해당 단계로 매핑한다 (아래 표).
   - 없으면 새 실행.

## 실행 폴더와 status.md

새 실행이면 `RUN_DIR` 을 만들고 `00-input.md`(대상, 요청 요약, 제약, `regression_mode`)와 `status.md` 를 저장한다. `00-input.md` 는 60줄 이하로 짧게 쓰고 긴 자료는 경로만 적는다.

```md
mode: subagent
target: {TARGET}
regression_mode: full | skip
created: {YYYY-MM-DD HH:MM}

| step | owner | status | output | updated | note |
| --- | --- | --- | --- | --- | --- |
| T00 input | orchestrator | done | 00-input.md |  |  |
| T01 design | work-architect | pending | 01-design.md, design.md |  |  |
| Gate1 | 사용자 | pending |  |  |  |
| T02 implement | work-implementer | pending | 02-implementation.md |  |  |
| T03 test | work-tester | pending | 03-tests.md |  |  |
| T04 regression | work-tester | pending | 04-regression.md |  |  |
| T05 review | work-reviewer | pending | 05-review.md |  |  |
| Gate2 | orchestrator | pending |  |  |  |
| T06 integrate | orchestrator | pending | final.md, improvement-log.md |  |  |
```

status 값: `pending` / `in_progress` / `done` / `blocked`(사유를 note 에 필수) / `skipped`. 각 단계 호출 직전에 `in_progress`, 직후에 결과를 반영해 갱신한다. 이때 `updated` 와 note 까지 채워 `in_progress` 행이 남지 않게 하고, 승인·결정으로 상태가 바뀌면 산출물 안의 앞선 "보류·대기" 서술도 함께 고쳐 모순이 남지 않게 한다.

## 단계

| 단계 | 담당 | 입력 | 출력 | 선행 | 완료 기준 |
| --- | --- | --- | --- | --- | --- |
| T00 | orchestrator | 사용자 요청 | `00-input.md`, `status.md` | 없음 | 대상, 요약, regression_mode 정리 |
| T01 | work-architect | `00-input.md`, `decisions.md`, 프로젝트 지식 | `01-design.md`, `design.md`, `decisions.md` | T00 | 브리프 완결, `design.md` 가 정본과 일치, 미확정 항목이 `decisions.md` 에 등록 |
| **Gate 1** | 사용자 | `design.md`, `decisions.md` | 승인 / 수정 | T01 | 명시적 승인 표현 |
| T02 | work-implementer | `01-design.md` (해당 단계 절) | 코드 diff, `02-implementation.md` | Gate 1 | 브리프 항목 100% + lint/type pass |
| T03 | work-tester | `01`, `02` | 테스트 파일, `03-tests.md` | T02 | targeted 실행 완료 |
| T04 | work-tester | `00`, `03` | `04-regression.md` (+ baseline) | T03 통과 | 전체 회귀 또는 skip 완료 |
| T05 | work-reviewer | `01`~`04` | `05-review.md` | T04 | 항목별 근거 있는 판정 |
| **Gate 2** | orchestrator | `05-review.md` | pass → T06 / fail → 재작업 | T05 | 재작업 라우팅 확정 |
| T06 | orchestrator | 모든 산출물 | `final.md`, `improvement-log.md` | Gate 2 | 커밋 메시지 초안 + 남은 위험 |

## 에이전트 호출 규약

`Agent` 도구를 `subagent_type` = 해당 에이전트 이름으로 호출한다. 프롬프트에는 아래를 모두 넣는다. 에이전트는 이 대화를 보지 못한다.

```
TARGET: {TARGET}
TARGET_SLUG: {TARGET_SLUG}
RUN_DIR: {RUN_DIR}
단계: {T01 | T02 | T03 | T04 | T05}
읽을 파일: {입력 파일 경로 목록}
쓸 파일: {출력 파일 경로}
regression_mode: {full | skip}      (tester 만)
제약: {사용자가 준 제약, 재작업이면 05-review.md 의 지시}
반환: 에이전트 파일의 '반환 형식' 으로 10줄 이내
```

`읽을 파일` 에 `01-design.md` 를 넣을 때 설계에 '단계별 읽기 범위' 표가 있으면 해당 단계의 절(공통 절 포함)만 읽도록 프롬프트에 적는다.

호출 후:

1. 쓸 파일이 실제로 생겼는지 확인한다. 없으면 `blocked` 로 기록하고 사용자에게 보고한다.
2. 반환값이 `blocked` 이거나 질문이 있으면 `status.md` 에 사유를 적고 사용자에게 **그대로 전달**한다. 브리프 모순은 architect 를 다시 호출한다.
   - 에이전트가 `blocked` 가 아니라 "결정 필요"(결정을 받으면 이어갈 수 있는 질문)를 돌려주면 사용자에게 전달하거나 설계 범위 안이면 직접 정해 같은 단계를 다시 호출한다. 이 재호출은 Gate 2 의 재작업 횟수에 세지 않고, 무슨 결정을 했는지 `status.md` note 에 남긴다.
3. 반환 요약을 사용자에게 한두 문장으로 보고하고 `status.md` 를 갱신한 뒤 다음 단계로 간다.

## Gate

### Gate 1 (설계 승인)

1. `decisions.md` 의 `[ ]` 항목 목록을 먼저 알린다.
2. `design.md`(읽기용 요약)를 보여주고 승인을 기다린다. `design.md` 가 없거나 `01-design.md` 와 어긋나면 architect 를 다시 불러 새로 쓰게 한다. 승인 표현이 없으면 T02 로 가지 않는다.
3. 사용자가 `decisions.md` 에 단 질문(`  ->`)에 Claude 답(`  - `)이 없으면 먼저 답한다. 사용자 답이 달린 항목은 해결 여부를 판단해 `[x]` / `[ ]` 를 갱신한다 (`[x]` = 해결됨, 판단은 Claude).
4. 결정이 설계를 바꾸면 architect 를 다시 호출한다.

### Gate 2 (리뷰 판정)

- **pass** → T06.
- **fail** → 실패 유형으로 라우팅한다.

| 유형 | 재작업 | 이후 |
| --- | --- | --- |
| 코드 이슈, 회귀 | implementer (T02) | T03 → T04 → T05 |
| 테스트 이슈 | tester (T03) | T04 → T05 |
| 브리프 애매 | 사용자에게 확인 후 필요 시 architect (T01) | Gate 1 부터 |

- 재작업은 **대상별 최대 1회**. 같은 대상이 두 번째로 fail 이면 현재 상태, 실패 근거, 선택지를 사용자에게 보고하고 확인을 받는다.
- targeted 테스트가 실패하면 T04 를 건너뛰고(`skipped`) T05 로 보내 실패 분류를 받는다.
- 회귀 skip 인데 위험 경고가 있으면 사용자 확인 없이 확정하지 않는다.

## T06 마무리

- `final.md`: 요청 요약, 변경 파일 목록, 테스트·회귀 결과, 남은 위험, **커밋 메시지 초안**(`.claude/rules/commit.md` 형식: 제목 + 본문 한두 줄, 결과물만), 프로젝트 규칙 문서의 '배포 노트 항목' 중 해당 사항, **커밋이 필요한 저장소**(코드 저장소의 변경, `knowledge/` 의 `runs/` · baseline · 승인된 문서 변경).
- `improvement-log.md`: 프로젝트 지식 문서 갱신 후보(`02-implementation.md` 의 '지식 문서 반영 후보' 포함), 하네스 개선 아이디어, 이번 실행의 특이점. 문서 반영은 후보로만 남기고 사용자가 승인하면 따로 한다.
- 커밋·푸시·PR·배포는 하지 않는다. 커밋은 사용자가 요청할 때 `commit.md` 에 따라 한다.

## 후속 요청 처리

| 사용자 표현 | 처리 |
| --- | --- |
| "이어서" | `status.md` 에서 첫 `pending` / `blocked` 단계부터 |
| "리뷰만 다시" | T05 재실행 (앞 산출물 재사용) |
| "테스트만 다시" | T03 → T04 → T05 |
| "구현부터 다시" | T02 부터 |
| "regression skip 으로 다시" | `regression_mode` 만 바꿔 T04 재실행 |
| "다른 대상 X" / "새 요청" | 새 `RUN_DIR` 로 새 실행 (기존 실행 폴더는 그대로 둔다) |

재실행하는 단계와 그 뒤 단계의 `status.md` 행은 `pending` 으로 되돌리고 이유를 note 에 남긴다.

## 하지 않는 일

- 외부 push, PR 생성, 배포.
- 승인 없는 baseline 변경, 승인 없는 코드 커밋.
- 사용자 승인 없이 `knowledge/docs/` 나 하네스 파일(`.claude/agents`, `.claude/skills`, `.claude/rules`, `.claude/docs`)을 수정하기. 실행 결과는 `RUN_DIR` 과 baseline 에만 쓴다.
- 서브에이전트 대신 직접 코드를 고치기 (메인 대화에서는 조율만 한다).
- 도구가 없다는 이유로 방식을 몰래 바꾸기. 바꿔야 하면 사용자에게 보고하고 `status.md` 의 `mode` 에 반영한다.

## 확장 자리 (지금은 만들지 않음)

읽기 전용 검증자 `work-ruler` 를 T02 와 동시에 `Agent` 도구 백그라운드로 호출해 규약 위반을 `RUN_DIR` 의 파일로 쓰게 할 수 있다. 쓰기 충돌이 없는 읽기 전용 역할만 병렬로 둔다. 기계가 판정할 수 있는 규칙은 hook 으로 걸고 판단이 필요한 규칙만 ruler 가 맡는다.
