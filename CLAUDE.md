# CLAUDE.md

이 workplace 의 개발 하네스(`work`) 안내. 작업은 **workplace 에서 시작**하고 대상 폴더를 지정한다. 저장소는 셋으로 나뉜다: 이 하네스 저장소(환경 공통), `knowledge/`(환경별 지식 저장소: 프로젝트 문서·실행 기록), 실제 프로젝트(각자 별도 저장소).

## 개발 하네스 (work)

대상 폴더의 기능 추가·변경·리팩터링 요청은 `work-orchestrator` 로 처리한다. 스킬 이름을 입력하지 않아도 아래처럼 대상과 작업이 드러나면 이 오케스트레이터로 라우팅한다.

- "apps/service-a 에 {기능} 추가해줘" / "service-b 의 {부분} 리팩터링" → `work-orchestrator`
- 대상 폴더의 코드를 바꾸는 요청은 변경 규모와 상관없이 `work-orchestrator` 를 거친다. 한 줄·문구·docstring 수정도 예외가 아니며, 직접 편집하지 않는다. 동작을 바꾸지 않는 작은 수정은 orchestrator 가 설계·리뷰를 생략하는 간단 경로로 처리한다. `Agent` 도구가 없으면 직접 하지 말고 보고하고 멈춘다.
- "리뷰만 다시" / "구현부터 다시" / "이어서" / "regression skip 으로 다시" → `work-orchestrator`
- "{폴더} 를 하네스에 추가" / "온보딩" / "개발 문서 만들어줘" → `project-onboarding`
- "커밋해줘" / "/commit" → `commit`
- "하네스 수정·점검·설계" / "에이전트·스킬 추가" → `harness-lab`

파이프라인: 대상 지정 → 설계 브리프 → **Gate 1 승인** → 구현 → 테스트 → 회귀 → 리뷰 → **Gate 2** → 마무리. 서브에이전트(`Agent` 도구)를 한 단계씩 호출하고 단계 사이는 파일로 넘긴다.
`knowledge/docs/{그룹}/{대상}/overview.md` 가 없으면 파이프라인을 시작하지 않고 편입을 제안한다.

## 위치

| 무엇 | 어디 |
| --- | --- |
| 에이전트 | `.claude/agents/work-{architect,implementer,tester,reviewer}.md` |
| 스킬 | `.claude/skills/` (`work-orchestrator`, `project-context-loader`, `design-brief`, `implementation-log`, `test-authoring-and-run`, `regression-run`, `code-review-checklist`, `project-onboarding`, `commit`, `harness-lab`) |
| 규칙 | `.claude/rules/commit.md` (커밋 규약. 절차는 `commit` 스킬), `.claude/rules/user-communication.md` (사용자에게 묻고 보고하는 문체, 승인·결정은 `decisions.md` 항목으로) |
| 프로젝트 지식 | `knowledge/docs/` (계약: `.claude/docs/README.md`, 인덱스: `knowledge/README.md`) |
| 실행 산출물 | `knowledge/runs/`, `knowledge/baselines/` (계약: `.claude/docs/runs.md`) |
| 지식 저장소 골격 | `.claude/knowledge-template/` (새 환경에서 `knowledge/` 를 만들 때 복사) |
| 하네스 설계 기록 | `.claude/docs/harness/` (`decisions.md`, `todo.md`, `changelog.md`, `lessons.md`, `boundary.txt`) |
| 점검 | `.claude/scripts/check-harness.py`, git hook `.claude/scripts/hooks/pre-commit` |

## 규칙

- 지침과 강제를 구분한다. 이 문서와 `rules/` 는 지침이고, 멈춤·허용·차단은 `settings.json` 의 permissions 와 hooks 로 건다.
- 하네스를 고치면 `.claude/docs/harness/changelog.md` 에 날짜·변경·대상·사유를 남긴다.
- 도메인 지식(규약, 명령)은 하네스 스킬에 넣지 않고 `knowledge/docs/` 의 프로젝트 문서에 둔다. 문서 구조·꼬리표·`reference/` 규칙은 `.claude/docs/README.md`, 금지 용어는 `knowledge/boundary.txt`(도메인 용어)와 `.claude/docs/harness/boundary.txt`(하네스 식별자).
- 하네스 저장소(`.claude/`, `CLAUDE.md`, `README.md`)에는 프로젝트 이름·사실을 쓰지 않는다. 대상 편입 기록도 `knowledge/` 에만 남긴다.
- 저장소를 새로 clone 했다면 한 번 `git config core.hooksPath .claude/scripts/hooks` 를, `knowledge/` 에서는 `git config core.hooksPath ../.claude/scripts/hooks` 를 실행한다. `core.hooksPath` 는 `.git/config` 에 저장되어 추적되지 않는다.
- 커밋 대상은 하네스(workplace 루트), `knowledge/`, 실제 코드 저장소 세 곳이다. 저장소마다 따로 커밋한다 (절차: `commit` 스킬).
- 하네스나 문서를 고친 뒤에는 `python3 -I .claude/scripts/check-harness.py` 를 실행한다. 커밋 때 git hook 이 같은 점검을 하고 위반이면 커밋을 막는다.
- 개발 실행은 `knowledge/docs/` 를 자동으로 수정하지 않는다. 반영은 `improvement-log.md` 후보 → 사용자 승인 순서다.
