# 프로젝트 지식 문서 — 계약

`work` 하네스가 실행 중에 읽는 **대상 프로젝트 문서**의 계약. 문서 자체는 환경별 지식 저장소의 `knowledge/docs/` 에 두고 프로젝트 사실만 담는다. 이 폴더(`.claude/docs/`)에는 계약(`README.md`, 실행 산출물 계약 `runs.md`)과 하네스 설계 기록(`harness/`)만 둔다. 하네스 절차(역할, 양식, 파이프라인)는 `.claude/agents|skills|rules` 에 둔다.
이 계약은 `.claude/scripts/check-harness.py` 가 커밋 때 점검한다.

## 구조

```
knowledge/docs/{그룹}/{대상 | common}/
├─ overview.md        대상 현황: 목적, 구조, 계층, 실행 방법, 인프라 (필수)
├─ rules.md           하네스 접점: 명령, 브리프·리뷰 추가 항목 등 (선택)
├─ todo.md            할 일 (선택)
├─ design/{주제}.md   설계 노트 (선택)
└─ reference/         원본 그대로 복사한 비정형 자료 + SOURCES.md
```

- 그룹(최상위 폴더): 이름 목록은 `knowledge/boundary.txt` 의 `[doc-groups]` 에 둔다 (예: `apps`, `tools`). 서로 다른 그룹에 같은 이름의 대상이 있을 수 있으므로 경로에 그룹을 반드시 포함한다.
- `common/` 은 그룹 공통 문서다. `overview.md`, `rules.md` 외의 가이드는 `common/{이름}.md` (kind: guide).
- 위 이름과 위치 밖의 파일은 두지 않는다. 비정형 자료는 `reference/` 로 간다.
- `.claude/docs/` 에는 `README.md`, `runs.md`, `harness/` 만 둔다. `harness/` 는 하네스 자체의 설계 기록(`decisions.md`, `todo.md`, `blueprint.md`, `lessons.md`, `changelog.md`, `boundary.txt`)이고 대상 문서가 아니다. 프로젝트 이름·사실은 하네스 쪽에 남기지 않는다.

## 꼬리표

`reference/` 를 뺀 모든 `.md` 맨 위에 둔다.

```md
---
kind: overview | rules | todo | design | guide
target: apps/service-a            # 경로와 일치해야 한다
source: apps/service-a/.claude/CLAUDE.md   # 원본이 있으면 경로, 직접 쓴 문서면 생략
status: raw | curated          # 정제 전 | 정제됨
updated: 2026-10-16
---
```

## rules.md 의 고정 제목

하네스가 프로젝트 지식을 읽는 유일한 접점이다. 아래 여섯 제목을 모두 둔다 (해당 없으면 "없음"). 이 밖의 제목은 하네스가 읽지 않는다.

`## 명령` · `## 설계 브리프 추가 섹션` · `## 리뷰 추가 점검 항목` · `## 구현 금지 · 주의` · `## 배포 노트 항목` · `## 회귀 위험 신호`

## reference/

- 흩어진 원본(옛 CLAUDE.md, DESIGN, WIKI, SQL 등)을 **그대로 복사**해 모아 두는 곳이다. 내용을 고치지 않는다.
- `SOURCES.md` 에 `| 파일 | 원본 경로 | 복사일 |` 로 출처를 기록한다. 비정형 파일에는 꼬리표를 달 수 없으므로 이 표가 출처 기록이다.
- 개발 실행(설계·구현·테스트·리뷰)은 `reference/` 를 읽지 않는다. 읽는 때는 `overview.md` 등을 만드는 온보딩뿐이다.
- 정제가 끝나 `overview.md` 등으로 옮겨진 뒤에도 출처 가치가 있으면 남기고, 불필요하면 정리한다.

## 쓰기 규칙

- 개발 실행은 `knowledge/docs/` 를 **자동으로 수정하지 않는다.** 문서에 반영할 만한 내용은 실행 폴더의 `improvement-log.md` 에 후보로만 남기고, 반영은 사용자 승인 후에 한다.
- 문서를 고치면 `updated` 를 갱신한다.

## 경계

- 하네스 파일(`agents`, `skills` — `harness-lab` 제외, `rules`, `CLAUDE.md`)에는 도메인 용어를 쓰지 않는다.
- `knowledge/docs/` 의 문서(`reference/` 제외)에는 하네스 식별자를 쓰지 않는다.
- 금지 용어는 두 곳에서 관리한다. 도메인 용어 `[harness-forbidden]` 는 `knowledge/boundary.txt`(환경별, 하네스 저장소에 올리지 않음), 하네스 식별자 `[docs-forbidden]` 는 `.claude/docs/harness/boundary.txt`.

## 대상 인덱스

환경마다 다르므로 `knowledge/README.md` 에 둔다. 대상 폴더에 `overview.md` 가 생기면 그 표에 한 줄을 추가한다 (점검 스크립트가 누락을 잡는다).
