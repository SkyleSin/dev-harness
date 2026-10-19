# 하네스 변경 이력

하네스(`.claude/`)와 하네스 문서(`.claude/docs/harness/`)의 변경만 기록한다. 대상 프로젝트의 변경은 해당 프로젝트 문서나 git 에 남긴다.
양식: 날짜 / 변경 / 대상 / 사유.

| 날짜 | 변경 | 대상 | 사유 |
| --- | --- | --- | --- |
| (설치일) | 하네스 뼈대 설치 | `.claude/`, `CLAUDE.md`, `artifacts/`, `.gitignore` | 개발 하네스 도입 |
| 2026-10-18 | 지식 저장소 분리: 프로젝트 문서·실행 산출물·`[doc-groups]`·`[harness-forbidden]` 을 `knowledge/`(환경별 git)로 이동, `knowledge-template/` 추가, `artifacts/README.md` → `.claude/docs/runs.md`, `.gitignore` 화이트리스트, 점검 스크립트·pre-commit 이 두 저장소를 함께 점검 | `.claude/`, `CLAUDE.md`, `README.md`, `.gitignore`, `knowledge-template/` | 하네스를 여러 환경에서 공유하면서 프로젝트 지식의 히스토리를 남기고 회사 정보 유출을 막기 위해 |
| 2026-10-18 | `knowledge-template/` → `.claude/knowledge-template/` 이동, `.gitignore` 화이트리스트에서 제외 줄 삭제 | `.claude/knowledge-template/`, `.gitignore`, `CLAUDE.md`, `README.md`, `project-onboarding`, `check-harness.py` | 템플릿은 하네스 소유이므로 `.claude/` 경계 안에 둔다 |
| 2026-10-19 | `harness-lab` 스킬(Subagent 기본 개정본)을 하네스에 포함. `lessons.md`·`blueprint.md` 를 범용 내용만 남기고 중립화(경로를 `knowledge/…` 로 갱신). 환경별 이력은 `knowledge/harness-history/` 로 분리 | `.claude/skills/harness-lab/`, `.claude/docs/harness/`, `README.md`, `CLAUDE.md` | 하네스를 환경 공통으로 발전시키고 환경별 기록을 하네스 저장소에서 빼기 위함 |
| 2026-10-19 | `blueprint.md` 의 산출물 계약·에이전트/스킬 표·오케스트레이터 흐름·테스트 프롬프트 표를 정본(`runs.md`, 에이전트·스킬 파일, `work-orchestrator`, `todo.md`) 참조로 줄임. `README.md` 구성 트리를 `CLAUDE.md` 위치 표 참조로 대체 | `.claude/docs/harness/blueprint.md`, `todo.md`, `README.md` | 같은 내용이 여러 문서에 있어 한쪽만 고치면 어긋나는 문제를 막기 위함 |
