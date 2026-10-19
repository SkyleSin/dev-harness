# 하네스 변경 이력

하네스(`.claude/`)와 하네스 문서(`.claude/docs/harness/`)의 변경만 기록한다. 대상 프로젝트의 변경은 해당 프로젝트 문서나 git 에 남긴다.
양식: 날짜 / 변경 / 대상 / 사유.

| 날짜 | 변경 | 대상 | 사유 |
| --- | --- | --- | --- |
| (설치일) | 하네스 뼈대 설치 | `.claude/`, `CLAUDE.md`, `artifacts/`, `.gitignore` | 개발 하네스 도입 |
| 2026-10-18 | 지식 저장소 분리: 프로젝트 문서·실행 산출물·`[doc-groups]`·`[harness-forbidden]` 을 `knowledge/`(환경별 git)로 이동, `knowledge-template/` 추가, `artifacts/README.md` → `.claude/docs/runs.md`, `.gitignore` 화이트리스트, 점검 스크립트·pre-commit 이 두 저장소를 함께 점검 | `.claude/`, `CLAUDE.md`, `README.md`, `.gitignore`, `knowledge-template/` | 하네스를 여러 환경에서 공유하면서 프로젝트 지식의 히스토리를 남기고 회사 정보 유출을 막기 위해 |
| 2026-10-18 | `knowledge-template/` → `.claude/knowledge-template/` 이동, `.gitignore` 화이트리스트에서 제외 줄 삭제 | `.claude/knowledge-template/`, `.gitignore`, `CLAUDE.md`, `README.md`, `project-onboarding`, `check-harness.py` | 템플릿은 하네스 소유이므로 `.claude/` 경계 안에 둔다 |
| 2026-10-19 | `harness-lab` 스킬(Subagent 기본 개정본)을 하네스에 포함. `lessons.md`·`blueprint.md` 를 범용 내용만 남기고 중립화(경로를 `knowledge/…` 로 갱신). 환경별 이력은 하네스에서 제거 | `.claude/skills/harness-lab/`, `.claude/docs/harness/`, `README.md`, `CLAUDE.md` | 하네스를 환경 공통으로 발전시키고 환경별 기록을 하네스 저장소에서 빼기 위함 |
| 2026-10-19 | `blueprint.md` 의 산출물 계약·에이전트/스킬 표·오케스트레이터 흐름·테스트 프롬프트 표를 정본(`runs.md`, 에이전트·스킬 파일, `work-orchestrator`, `todo.md`) 참조로 줄임. `README.md` 구성 트리를 `CLAUDE.md` 위치 표 참조로 대체 | `.claude/docs/harness/blueprint.md`, `todo.md`, `README.md` | 같은 내용이 여러 문서에 있어 한쪽만 고치면 어긋나는 문제를 막기 위함 |
| 2026-10-19 | 커밋 대상을 하네스·`knowledge/`·코드 저장소 세 곳으로 명시하고 저장소별로 따로 커밋하도록 `commit` 스킬 1·3단계, `CLAUDE.md` 규칙, `work-orchestrator` T06 의 `final.md`, `runs.md` 파일 지도를 갱신 | `.claude/skills/commit/`, `CLAUDE.md`, `.claude/skills/work-orchestrator/`, `.claude/docs/runs.md` | 저장소를 셋으로 나눈 뒤 커밋할 곳을 빠뜨리지 않게 하기 위함 |
| 2026-10-19 | `todo.md` 에서 환경 셋업 항목(경계 사전 채우기, 첫 대상 편입)을 삭제 | `.claude/docs/harness/todo.md` | 하네스 개선 항목이 아니라 설치 절차(`README.md` 3·6단계)와 중복이었음 |
| 2026-10-19 | 첫 실전 완료: 소규모 기능 1건을 전 단계(두 Gate 포함)로 완주. 리뷰 pass, 회귀 신규 실패 0건, baseline 신설은 승인 후 저장. 막힌 지점: 테스트·타입 체크 실행 방식이 프로젝트 규칙 문서에 명시되지 않아 실행마다 에이전트 프롬프트로 전달됨 | `.claude/docs/harness/todo.md` | 첫 실전 검증. 도메인 보강은 해당 프로젝트 문서 갱신 후보로 처리 |
| 2026-10-19 | `work-reviewer` 와 `code-review-checklist` 에 "baseline 상태는 앞 산출물이 아니라 리뷰 시점의 실제 파일로 확인" 지침을 추가 | `.claude/agents/work-reviewer.md`, `.claude/skills/code-review-checklist/SKILL.md` | "리뷰만 다시" 재실행 시 리뷰어가 낡은 `04` 의 baseline 없음 서술을 그대로 옮겨 이미 신설된 baseline 을 없다고 판정함 |
| 2026-10-19 | `CLAUDE.md` 라우팅과 `work-orchestrator` description 에 "대상 폴더의 코드 변경은 규모와 무관하게 오케스트레이터를 거치고 직접 편집하지 않는다" 명시 | `CLAUDE.md`, `.claude/skills/work-orchestrator/SKILL.md` | 테스트에서 한 줄짜리 수정 요청이 오케스트레이터를 우회해 직접 편집되고 설계·테스트·리뷰가 생략됨 |
