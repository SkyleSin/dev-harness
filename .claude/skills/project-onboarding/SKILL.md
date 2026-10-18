---
name: project-onboarding
description: 코드가 이미 있는 대상 폴더(예 apps/service-c)를 개발 하네스에 편입한다. 소스를 스캔해 knowledge/docs/{대상}/overview.md 와 rules.md 초안을 만들고 승인 후 저장·등록한다. 자연어 예) "service-c 를 하네스에 추가해줘", "이 폴더 온보딩", "새 프로젝트 개발 문서 만들어줘". 골격 생성이나 도메인 구현은 하지 않는다.
---

# project-onboarding

## Overview

`work-orchestrator` 가 대상 폴더를 다룰 수 있도록 프로젝트 지식 문서를 만든다. 실제 파일에서 확인한 사실만 채우고 추측한 항목은 `확인 필요` 로 남긴다. 빈 저장소에 골격을 만드는 일은 이 스킬의 범위가 아니다.

## 만드는 문서

| 문서 | 위치 | 내용 |
| --- | --- | --- |
| 프로젝트 지식 | `knowledge/docs/{TARGET}/overview.md` | 목적, 구조, 계층, 실행 방법, 인프라, 포트, 이미지 경로 |
| 프로젝트 규칙 | `knowledge/docs/{TARGET}/rules.md` (공통이면 `knowledge/docs/{그룹}/common/rules.md` 재사용) | 고정 제목 여섯 개: 명령(테스트·lint·type), 설계 브리프 추가 섹션, 리뷰 추가 점검 항목, 구현 금지 · 주의, 배포 노트 항목, 회귀 위험 신호 |

`rules.md` 는 하네스가 도메인 지식을 읽는 유일한 접점이다. 이 문서에 없는 규약은 하네스가 요구하지 않는다. 문서 구조·꼬리표·고정 제목의 계약은 `.claude/docs/README.md` 를 따른다. 원본 자료가 흩어져 있으면 먼저 `reference/` 에 그대로 복사(`SOURCES.md` 에 출처 기록)하고 그것을 근거로 문서를 만든다.

## Workflow

1. `knowledge/` 가 있는지 확인한다. 없으면 workplace `README.md` 의 셋업 절차(지식 저장소 clone 또는 `knowledge-template/` 복사)를 안내하고 중단한다. `TARGET` 이 실제 폴더이고 `.git` 외 파일이 있는지 확인한다. 비어 있으면 "골격이 없는 폴더는 이 스킬의 범위가 아님" 을 안내하고 중단한다.
2. 다음을 스캔한다: 의존성 파일(`pyproject.toml`, `requirements*`, `package.json` 등), `Dockerfile`·`docker-compose*`·`entrypoint*`, CI 설정, `README*`, 마이그레이션 폴더, `tests/` 구조와 conftest, 주요 패키지 폴더(실제 존재하는 것만).
3. 파일 근거로만 추론한다: 프레임워크, 사용 인프라, 계층 구조, 실행 포트, 이미지 경로, 실행·테스트·lint·type 명령.
4. 같은 그룹의 기존 문서(`knowledge/docs/{그룹}/{다른 대상}/overview.md`)를 참조 양식으로 삼되, 존재하지 않는 계층과 섹션은 통째로 생략한다.
5. 초안 + 요약 + 확인 필요 항목을 사용자에게 보여주고 **명시적 승인** 을 기다린다. 승인 없이 저장하지 않는다.
6. 승인 후 저장한다. 이미 문서가 있으면 덮어쓰지 않고 차이를 보여주고 승인을 따로 받는다.
7. 문서마다 꼬리표(`kind`, `target`, `source`, `status`, `updated`)를 달고, `knowledge/README.md` 의 대상 인덱스에 한 줄을 추가(이미 있으면 갱신)한다. 편입 기록은 `knowledge/` 저장소에만 남기고 하네스의 `changelog.md` 에는 쓰지 않는다. `python3 -I .claude/scripts/check-harness.py` 로 계약 위반이 없는지 확인한다.
8. 남은 gap 을 리포트에 명시한다.

## 품질 기준

- 사실과 추정을 구분한다 (추정은 `확인 필요`).
- 명령은 실제 파일(CI 설정, README, pyproject 등)에서 확인된 것만 적는다.

## 예외와 금지 행동

- 코드를 수정하지 않는다 (문서만 만든다).
- 승인 전에 파일을 저장하지 않는다.
- 기존 문서를 말없이 덮어쓰지 않는다.
