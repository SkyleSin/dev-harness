---
name: regression-run
description: targeted 테스트 통과 후 전체 테스트를 실행해 side-effect 회귀를 감지한다. work-tester 가 T04 에서 사용한다. baseline 파일(알려진 실패 / 통과 인벤토리)과 대조해 신규 실패만 회귀로 분류한다. regression_mode 가 skip 이면 스킵 처리한다.
---

# regression-run

## Overview

전체 테스트를 실행하고, `failures.txt` 에 기록된 알려진 실패를 제외한 신규 실패만 회귀로 분류한다. 테스트 실행 명령은 프로젝트 규칙 문서의 '명령'을 그대로 쓴다.

baseline 위치: `knowledge/baselines/{TARGET_SLUG}/`

## Workflow

1. `{RUN_DIR}/00-input.md` 에서 `regression_mode` 를 확인한다. `skip` 이면 3, `full` 이면 2.
2. 전체 실행: 프로젝트 규칙 문서의 전체 테스트 명령. 실패 노드 ID 를 수집한다. 명령이 없으면 추측하지 않고 `blocked` 로 반환한다.
3. skip 인 경우:
   - `{RUN_DIR}/04-regression.md` 에 "사용자 요청으로 스킵" 을 명시한다.
   - baseline 은 갱신하지 않는다.
   - tester 가 위험 상황(마이그레이션 편집, 핸들러 전면 변경, 공용 유틸 편집)을 감지했으면 상단에 ⚠️ 경고를 추가한다.
4. baseline 처리 — **파일 두 개의 성격이 다르다. 절대 섞지 말 것.**

   | 파일 | 담는 것 | 용도 |
   | --- | --- | --- |
   | `failures.txt` | **알려진 실패** 노드 ID | delta 계산 (5번) |
   | `inventory.txt` | **통과한 전체** 노드 ID | 테스트 소실 감지 (5-1번) |

   - 각 파일 한 줄에 노드 ID 하나.
   - 실패가 0건이면 `failures.txt` 는 **빈 파일이 정상**이다. 통과 목록을 여기 넣으면 delta 규칙이 정반대로 동작한다 (통과하던 테스트가 깨졌을 때 "기존 실패" 로 오분류).
   - 각 파일이 없으면 `knowledge/baselines/` 에 쓰지 않고 `{RUN_DIR}/baseline-proposal/` 에 이번 실행 결과로 제안을 만들어 "최초 제안(승인 대기)" 로 표기한다. 사용자 승인 뒤 오케스트레이터가 `knowledge/baselines/{TARGET_SLUG}/` 로 옮긴다.
5. Delta 규칙 (`failures.txt` 기준):
   - 현재 실패 ∈ baseline → 기존 실패 (무시, `improvement-log.md` 기록 후보)
   - 현재 실패 ∉ baseline → **회귀 (blocker)**
   - baseline 항목이 현재 통과 → baseline 에서 제거하고 "묵혀둔 실패 해소" 로그
5-1. 인벤토리 대조 (`inventory.txt` 기준):
   - 인벤토리에 있는데 이번 실행에 **없는** 노드 = 삭제되었거나 이름이 바뀐 테스트.
   - 이번 변경으로 의도한 것인지, 이전 작업에서 갱신이 누락된 것인지 구분해 `04-regression.md` 에 적는다 (`git show HEAD:<파일>` 로 확인 가능).
   - 확인 후 인벤토리를 이번 통과 목록으로 갱신한다.
6. 아래 양식으로 `{RUN_DIR}/04-regression.md` 를 저장한다.

## 산출물 형식 (`04-regression.md`)

```md
# 04. Regression

## 모드
- {full / skip}

## 실행 명령 (full 모드)
- `{실제 실행한 명령}`

## 요약
- 총 실행: N
- Pass: N / Fail: N / Skip: N

## Baseline 상태
- 경로: `knowledge/baselines/{TARGET_SLUG}/`
- failures: {최초 제안(승인 대기) / 갱신 없음 / 항목 제거 N건}
- inventory: {최초 제안(승인 대기) / 갱신됨 / 소실 N건}

## 회귀 (신규 실패)
| 노드 ID | 실패 요지 | 근거 로그 |
| --- | --- | --- |

## 기존 실패 (baseline 유지)
| 노드 ID | 계속 실패 |
| --- | --- |

## 소실된 테스트 (인벤토리 대조)
| 노드 ID | 의도 여부 | 근거 |
| --- | --- | --- |
```

## 품질 기준

- baseline 파일 조작은 명시된 규칙에만 따른다.
- 스킵 모드에서도 `04-regression.md` 는 반드시 생성한다 (내용이 스킵 명시).
- 실행 결과는 실제 출력 기반이다.

## 예외와 금지 행동

- targeted 가 실패한 상태에서 이 스킬을 실행하지 않는다.
- 신규 실패를 baseline 에 자동 추가하지 않는다 (사용자 승인 필요).
- 위험 상황에서 skip 요청이 들어와도 `04-regression.md` 에 위험을 숨기지 않는다.
