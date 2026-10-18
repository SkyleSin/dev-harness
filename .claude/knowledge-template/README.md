# knowledge

이 workplace 환경의 **지식 저장소**. 하네스 저장소와 별개의 git 저장소로 관리한다 (회사 환경이면 회사 git, 개인 환경이면 개인 저장소).

| 무엇 | 어디 | 계약 |
| --- | --- | --- |
| 프로젝트 지식 문서 | `docs/{그룹}/{대상 \| common}/` | `../.claude/docs/README.md` |
| 경계 사전 (문서 그룹, 도메인 금지 용어) | `boundary.txt` | `../.claude/docs/README.md` |
| 실행 산출물 | `runs/`, `baselines/` | `../.claude/docs/runs.md` |

커밋 전 점검: `git config core.hooksPath ../.claude/scripts/hooks` (clone 직후 한 번).

## 대상 인덱스

대상 폴더에 `overview.md` 가 생기면 아래 표에 한 줄을 추가한다 (점검 스크립트가 누락을 잡는다).

| 대상 | 문서 | 상태 |
| --- | --- | --- |
| (아직 없음) | | 편입 필요 |
