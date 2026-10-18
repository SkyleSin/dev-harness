# 하네스 TODO

앞으로 할 일. 이미 정한 것·답이 필요한 질문은 `decisions.md`, 한 일은 `changelog.md` 에 둔다.
항목을 끝내면 지우지 않고 `[x]` 로 바꾼 뒤 `changelog.md` 에 한 줄을 남긴다.

## 가까운 일

- [ ] `knowledge/boundary.txt` 의 `[doc-groups]` 와 `[harness-forbidden]` 을 실제 프로젝트에 맞게 채우기 (환경마다)
- [ ] 첫 대상 하나를 `project-onboarding` 으로 편입 (`overview.md`, `rules.md` 작성)
- [ ] 새 세션(workplace 에서 시작)에서 테스트 프롬프트 실행: 정상 / 대상 미지정 / 테스트 실패 / 지식 문서 없음 / 도구 없음 / "리뷰만 다시"
- [ ] 첫 실전: 소규모 기능 하나를 `work-orchestrator` 로 완주하고 막힌 지점을 `changelog.md` 에 기록

## 보류 · 추후

- [ ] 개발 실행 중 하네스 파일(`.claude/agents|skills|rules`) 수정 차단 hook (PreToolUse, 정비할 때만 환경변수로 해제). 개발 실행이 하네스를 오염시키는 사고가 생기면 도입
- [ ] 읽기 전용 검증자(`work-ruler`)를 구현과 병렬로 `Agent` 백그라운드 호출. 기계 판정 규칙은 hook, 판단이 필요한 규칙만 ruler
- [ ] 무인 장시간 실행 설계 (`-p` + 권한 모드 + allow/deny, 종료 조건, 진행 기록)
- [ ] Task / Agent Team 도구 실험 (필요해지면 비용이 낮은 병렬 `Agent` 호출부터)
- [ ] 개발 실행의 `knowledge/docs` 쓰기를 permissions `ask` 로 승인 강제하는 방안 (자동화와 충돌 여부 확인 후)
