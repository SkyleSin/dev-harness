# 개발 하네스 뼈대 (skeleton)

Claude Code 로 여러 프로젝트를 한 workplace 에서 개발할 때 쓰는 **도메인 중립 하네스 뼈대**다. 한 workplace 에서 운영하며 다듬은 하네스에서 범용 부분만 뽑았다. 프로젝트 지식, 실행 산출물, 회사 고유 규약은 들어 있지 않다.

## 무엇을 하는가

대상 폴더를 지정한 변경 요청을 **설계 → 승인 → 구현 → 테스트 → 회귀 → 리뷰 → 승인 → 마무리** 순서로 처리한다.

- 서브에이전트 4개(`work-architect`, `work-implementer`, `work-tester`, `work-reviewer`)를 오케스트레이터(`work-orchestrator`)가 `Agent` 도구로 **한 단계씩** 호출하고, 단계 사이는 실행 폴더의 파일로 넘긴다. 진행 상태는 `status.md` 에 남아 재개·부분 재실행("리뷰만 다시")의 기준이 된다.
- 사람이 확인하는 지점이 둘이다: **Gate 1**(설계 승인), **Gate 2**(리뷰 판정). 재작업은 대상별 1회, 두 번째 실패는 사용자에게 보고한다.
- 하네스 스킬에는 도메인 지식을 넣지 않는다. 프로젝트마다 `knowledge/docs/{그룹}/{대상}/` 의 `overview.md`(현황)와 `rules.md`(명령, 브리프·리뷰 추가 항목 등 고정 제목 여섯 개)를 두고 하네스는 그것만 읽는다.
- 경계는 점검 스크립트가 강제한다: 하네스 파일에 도메인 용어가 들어가거나, 프로젝트 문서에 하네스 식별자가 들어가면 커밋이 막힌다.

## 구성

에이전트 4개, 스킬 10개, 커밋 규약, 지식 저장소 골격(`.claude/knowledge-template/`), 문서 계약(`.claude/docs/README.md`, `runs.md`), 하네스 설계 기록(`.claude/docs/harness/`), 점검 스크립트와 pre-commit 훅으로 이루어진다. 파일별 위치는 `CLAUDE.md` 의 위치 표를 본다.

## 저장소 구성

```
workplace/            하네스 저장소 (이 저장소, 환경 공통)
├── .claude/ ...
├── knowledge/        지식 저장소 (환경별 별도 git, 하네스는 무시)
│   ├── README.md     대상 인덱스
│   ├── boundary.txt  [doc-groups], [harness-forbidden]
│   ├── docs/{그룹}/{대상}/
│   ├── runs/
│   └── baselines/
└── {프로젝트}/       각 프로젝트 저장소 (하네스는 무시)
```

- 하네스 저장소의 `.gitignore` 는 화이트리스트다. workplace 에 어떤 폴더가 생겨도 추적되지 않는다.
- 회사 환경의 지식 저장소는 회사 git 에, 개인 환경은 개인 저장소에 둔다. 도메인 용어(`[harness-forbidden]`)도 지식 저장소에만 적는다.

## 설치

1. 하네스 저장소를 workplace 로 clone 한다: `git clone <하네스 저장소> <workplace>` 후 `git config core.hooksPath .claude/scripts/hooks`
2. 지식 저장소를 준비한다.
   - 이미 있으면: `git clone <지식 저장소> <workplace>/knowledge`
   - 처음이면: `cp -r .claude/knowledge-template knowledge && git -C knowledge init -b main`
   - 어느 쪽이든: `git -C knowledge config core.hooksPath ../.claude/scripts/hooks`
3. `knowledge/boundary.txt` 를 고친다.
   - `[doc-groups]`: 프로젝트 폴더들의 최상위 그룹 이름 (예: `apps`, `services`)
   - `[harness-forbidden]`: 하네스에 나오면 안 되는 도메인 용어 (프레임워크, 사내 서비스·시스템 이름 등)
4. 프로젝트 저장소를 workplace 아래에 clone 한다 (하네스·지식 저장소 모두 무시한다).
5. `python3 -I .claude/scripts/check-harness.py` — 오류 0건이어야 한다.
6. workplace 에서 새 Claude Code 세션을 열고 첫 대상을 편입한다: "apps/service-a 를 하네스에 추가해줘" → `project-onboarding` 이 `overview.md`·`rules.md` 초안을 만들고 승인 후 저장한다.
7. 이후 "apps/service-a 에 {기능} 추가해줘" 처럼 요청한다. 대상 문서가 없으면 파이프라인이 시작되지 않고 편입을 제안한다.

## 고칠 곳

- **이름 접두사 `work-`**: 에이전트 파일명과 frontmatter `name`, 스킬 폴더·`name`, 스킬·`CLAUDE.md`·`.claude/docs/harness/boundary.txt` 안의 참조를 함께 바꾼다. 바꾼 뒤 점검 스크립트가 이름·참조 불일치를 잡는다.
- **커밋 규약** `.claude/rules/commit.md`: 접두사 표를 조직의 이슈 트래커 형식에 맞춘다. 테스트 실행 방식은 `commit` 스킬 5단계에서 프로젝트에 맞게 바꾼다.
- **프로젝트 규칙 문서** (`rules.md`): 테스트·lint·type 명령, 설계 브리프 추가 섹션, 리뷰 추가 점검 항목 등 도메인 지식은 모두 여기에 둔다. 스킬에 직접 넣지 않는다.

## harness-lab

`harness-lab`(원본: https://github.com/jikime/harness-lab)은 하네스를 설계·점검·개선하는 스킬이며 `.claude/skills/harness-lab/` 에 포함되어 있다. 원본에서 아래처럼 개정했다.

- 실행 하네스의 **기본 실행 모드를 Agent Team 에서 Subagent 순차로** 바꿨다. Agent Team(`TeamCreate`, `Task*`, `SendMessage`)은 사용자가 명시적으로 요청하고 도구가 실제로 보일 때만 쓰는 옵트인이다.
- Subagent 최소 실행 계약을 두었다: 호출 계약(실행 폴더·입력·출력·제약을 프롬프트로 전달, 10줄 이내 반환), `status.md`, 질문·승인 중계, 산출물 확인, 모드 선언(도구가 없다고 조용히 우회하지 않음), 읽기 전용 역할의 병렬 확장.
- 청사진 승인 게이트(파일 생성 전 청사진 제시)와 Phase 0~7 은 그대로 둔다.

## 포함하지 않은 것

프로젝트 지식 문서, 실행 산출물, 테스트 baseline (모두 `knowledge/` 지식 저장소), 회사 고유 규약.

## 알려진 한계

- 한 workplace 에서만 실전 검증했다.
- 새로 만든 에이전트·스킬은 세션을 새로 열어야 목록에 나타난다.
- 점검 스크립트는 커밋 시점에 돈다 (`--no-verify` 로 우회 가능). 편집 시점 강제는 하지 않는다 (todo 참고).
- `lessons.md` 는 이 하네스를 만들며 얻은 범용 규칙 목록이다. 새 환경의 사정에 맞게 취사선택한다.
