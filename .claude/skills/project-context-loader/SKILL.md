---
name: project-context-loader
description: 대상 폴더(예 apps/service-a)의 프로젝트 지식 문서, 프로젝트 규칙 문서(rules.md), 해당 폴더의 CLAUDE.md, 관련 코드를 로드한다. work-architect 가 설계 시작 전에 사용한다. 지식 문서가 없으면 중단하고 project-onboarding 을 안내한다.
---

# project-context-loader

## Overview

대상 폴더의 컨텍스트를 확보해 설계자가 근거 있는 브리프를 만들게 한다. 문서가 없거나 대상이 불명확하면 임의로 진행하지 않고 확인 필요로 반환한다.

## 경로 규약

- `TARGET`: workplace 기준 대상 폴더 (예 `apps/service-a`). `TARGET_SLUG`: `/` 를 `-` 로 바꾼 값 (예 `apps-service-a`).
- 그룹: `TARGET` 의 첫 경로 (예 `apps`).
- 프로젝트 지식: `knowledge/docs/{TARGET}/overview.md` (필수)
- 프로젝트 규칙: `knowledge/docs/{TARGET}/rules.md`, 없으면 `knowledge/docs/{그룹}/common/rules.md`
- 공통 문서: `knowledge/docs/{그룹}/common/*.md`
- 대상 폴더와 상위 폴더의 `CLAUDE.md` (있으면)
- 문서 계약(구조, 꼬리표, 고정 제목)은 `.claude/docs/README.md`. `reference/` 폴더는 읽지 않는다 (온보딩 전용 원본 자료).

## Workflow

1. 프롬프트로 받은 `TARGET` 이 실제 폴더인지 확인한다.
2. `knowledge/docs/{TARGET}/overview.md` 존재를 확인한다. 없으면 즉시 중단하고 "프로젝트 지식 부재 — project-onboarding 필요" 를 반환한다. 코드를 보고 문서를 추측하지 않는다.
3. 아래 순서로 읽는다: 대상 폴더와 상위 폴더의 `CLAUDE.md` → `overview.md` → `rules.md` → 공통 문서 중 요청과 관련된 것.
4. 요청과 관련된 코드를 Grep/Glob 으로 식별한다. 관련성 있는 파일만 고른다 (전체 나열 금지).
5. 프로젝트 규칙 문서에 '명령'(테스트·lint·type) 항목이 있는지 확인한다. 없으면 "확인 필요" 로 반환한다.

## 반환 형식

```md
## 대상
- {TARGET} (slug: {TARGET_SLUG})

## 로드한 컨텍스트
- {읽은 문서 경로 목록}

## 프로젝트 규칙 요지
- 명령: 테스트 / lint / type
- 설계 브리프 추가 섹션:
- 리뷰 추가 점검 항목:
- 구현 금지·주의:
- 배포 노트 항목:
- 회귀 위험 신호:

## 관련 코드 영역
- `{path}`: {한 줄 요지}

## 확인 필요
- {문서 부재, 명령 부재, 대상 불명확 등}
```

## 품질 기준

- 문서와 코드의 존재 여부를 실제로 확인한 것만 적는다.
- 요청이 여러 대상에 걸치면 임의로 고르지 않고 대상별로 별도 실행하도록 안내한다.
