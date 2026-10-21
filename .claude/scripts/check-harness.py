"""하네스 경계·형식 점검. 위반이 있으면 종료 코드 1.

실행: python3 -I .claude/scripts/check-harness.py
규칙의 원문: .claude/docs/README.md (문서 계약), .claude/docs/harness/boundary.txt (하네스 식별자),
knowledge/boundary.txt (환경별 문서 그룹·도메인 용어)
하네스 저장소와 knowledge/ 저장소의 pre-commit 이 함께 쓴다. knowledge/ 가 없으면 지식 쪽 점검은 건너뛴다.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / ".claude"
DOCS = CLAUDE / "docs"
HARNESS_BOUNDARY = DOCS / "harness" / "boundary.txt"
DOCS_ALLOWED = {"README.md", "runs.md"}
KNOW = ROOT / "knowledge"
KDOCS = KNOW / "docs"
KINDEX = KNOW / "README.md"
KBOUNDARY = KNOW / "boundary.txt"

KINDS = {"overview", "rules", "todo", "design", "guide", "reference"}
STATUSES = {"raw", "curated"}
FRONTMATTER_KEYS = ("kind", "target", "status", "updated")
RULES_HEADINGS = (
    "명령",
    "설계 브리프 추가 섹션",
    "리뷰 추가 점검 항목",
    "구현 금지 · 주의",
    "배포 노트 항목",
    "회귀 위험 신호",
)

errors: list[str] = []
warnings: list[str] = []


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out: dict[str, str] = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def load_boundary(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    cur = None
    if not path.exists():
        errors.append(f"{rel(path)}: 경계 사전이 없다")
        return sections
    for raw in read(path).split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            cur = line[1:-1]
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    return sections


def scan_terms(files: list[Path], terms: list[str], label: str) -> None:
    for f in files:
        for n, line in enumerate(read(f).split("\n"), 1):
            for t in terms:
                if t in line:
                    errors.append(f"{rel(f)}:{n}: {label} 용어 '{t}'")


# ---------- 하네스 쪽 docs: 계약과 설계 기록만 ----------
def check_harness_docs() -> None:
    for path in sorted(DOCS.rglob("*")):
        if not path.is_file():
            continue
        parts = path.relative_to(DOCS).parts
        if parts[0] == "harness" or (len(parts) == 1 and parts[0] in DOCS_ALLOWED):
            continue
        errors.append(f"{rel(path)}: .claude/docs 에는 {sorted(DOCS_ALLOWED)} 와 harness/ 만 둔다 (프로젝트 문서는 knowledge/docs/)")


# ---------- 문서 계약 (knowledge/docs) ----------
def check_docs(groups: set[str]) -> None:
    if not KDOCS.exists():
        errors.append(f"{rel(KDOCS)} 가 없다")
        return
    index_text = read(KINDEX) if KINDEX.exists() else ""
    if not KINDEX.exists():
        errors.append(f"{rel(KINDEX)} 가 없다 (대상 인덱스)")

    targets: set[str] = set()
    for path in sorted(KDOCS.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        parts = path.relative_to(KDOCS).parts
        if len(parts) < 3 or parts[0] not in groups:
            errors.append(f"{rel(path)}: 위치가 맞지 않다 (knowledge/docs/{{그룹}}/{{대상|common}}/파일, 그룹은 knowledge/boundary.txt 의 [doc-groups])")
            continue
        group, target_dir = parts[0], parts[1]
        target = f"{group}/{target_dir}"
        sub = parts[2:]
        name = sub[-1]

        if sub[0] == "reference":
            continue  # 원본 복사본. SOURCES.md 대조는 아래에서 한다.

        if path.suffix != ".md":
            errors.append(f"{rel(path)}: 문서는 .md 만 둔다 (비정형 자료는 reference/)")
            continue

        text = read(path)
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel(path)}: 꼬리표(frontmatter)가 없다")
            continue
        for k in FRONTMATTER_KEYS:
            if k not in fm:
                errors.append(f"{rel(path)}: 꼬리표에 '{k}' 가 없다")
        if fm.get("kind") not in KINDS:
            errors.append(f"{rel(path)}: kind '{fm.get('kind')}' 는 {sorted(KINDS)} 중 하나여야 한다")
        if fm.get("status") not in STATUSES:
            errors.append(f"{rel(path)}: status '{fm.get('status')}' 는 {sorted(STATUSES)} 중 하나여야 한다")
        if fm.get("target") != target:
            errors.append(f"{rel(path)}: target '{fm.get('target')}' 가 경로의 '{target}' 와 다르다")

        # 이름·위치와 kind 의 일치
        expected = None
        if len(sub) == 1 and name == "overview.md":
            expected = "overview"
        elif len(sub) == 1 and name == "rules.md":
            expected = "rules"
        elif len(sub) == 1 and name == "todo.md":
            expected = "todo"
        elif sub[0] == "design" and len(sub) == 2:
            expected = "design"
        elif target_dir == "common" and len(sub) == 1:
            expected = "guide"
        if expected is None:
            errors.append(
                f"{rel(path)}: 허용되지 않는 이름·위치 (overview.md, rules.md, todo.md, design/*.md, common/*.md, reference/ 만)"
            )
        elif fm.get("kind") != expected:
            errors.append(f"{rel(path)}: 이 위치의 kind 는 '{expected}' 여야 한다 (현재 '{fm.get('kind')}')")

        if name == "overview.md" and len(sub) == 1:
            targets.add(target)

        if name == "rules.md" and len(sub) == 1:
            for h in RULES_HEADINGS:
                if not re.search(rf"^## {re.escape(h)}\s*$", text, re.M):
                    errors.append(f"{rel(path)}: 필수 제목 '## {h}' 가 없다")
            body = re.sub(r"```.*?```", "", text, flags=re.S)
            for h in re.findall(r"^## (.+?)\s*$", body, re.M):
                if h not in RULES_HEADINGS:
                    warnings.append(f"{rel(path)}: 고정 목록에 없는 제목 '## {h}' (하네스가 읽지 않는다)")

    # reference/ 출처 대조
    for ref in sorted(KDOCS.glob("*/*/reference")):
        sources = ref / "SOURCES.md"
        if not sources.exists():
            errors.append(f"{rel(ref)}: SOURCES.md 가 없다 (파일 | 원본 경로 | 복사일)")
            continue
        src_text = read(sources)
        for f in sorted(p for p in ref.rglob("*") if p.is_file() and p != sources):
            rel_name = str(f.relative_to(ref))
            if rel_name not in src_text:
                errors.append(f"{rel(f)}: SOURCES.md 에 출처가 기록되지 않았다")

    # 대상 인덱스
    for t in sorted(targets):
        if f"`{t}`" not in index_text:
            errors.append(f"{rel(KINDEX)}: 대상 인덱스에 `{t}` 가 없다")


# ---------- 하네스 구조 ----------
def check_harness_files() -> list[Path]:
    files: list[Path] = []
    skill_dirs = sorted(p for p in (CLAUDE / "skills").glob("*") if p.is_dir())
    skills = {p.name for p in skill_dirs}
    for f in sorted((CLAUDE / "agents").glob("*.md")):
        files.append(f)
        t = read(f)
        m = re.match(r"---\nname: (.+)\n", t)
        if not m or m.group(1) != f.stem:
            errors.append(f"{rel(f)}: frontmatter name 이 파일명과 다르다")
        for s in re.findall(r"^  - (.+)$", t.split("---")[1] if t.startswith("---") else "", re.M):
            if s not in skills:
                errors.append(f"{rel(f)}: 참조한 스킬 '{s}' 가 없다")
    for d in skill_dirs:
        f = d / "SKILL.md"
        if not f.exists():
            errors.append(f"{rel(d)}: SKILL.md 가 없다")
            continue
        if d.name != "harness-lab":
            files.append(f)
        m = re.match(r"---\nname: (.+)\n", read(f))
        if not m or m.group(1) != d.name:
            errors.append(f"{rel(f)}: frontmatter name 이 폴더명과 다르다")
    files += sorted((CLAUDE / "rules").glob("*.md"))
    if (ROOT / "CLAUDE.md").exists():
        files.append(ROOT / "CLAUDE.md")
    return files


# ---------- 실행 산출물 ----------
RUN_FILE_LIMITS = {"design.md": 100, "00-input.md": 60}


def check_runs() -> None:
    for run in sorted((KNOW / "runs").glob("*/")):
        for name, limit in RUN_FILE_LIMITS.items():
            f = run / name
            if f.exists():
                n = len(read(f).splitlines())
                if n > limit:
                    warnings.append(f"{rel(f)}: {n}줄 (기준 {limit}줄 이하)")


def main() -> int:
    hb = load_boundary(HARNESS_BOUNDARY)
    check_harness_docs()
    harness_files = check_harness_files()

    if not KNOW.exists():
        warnings.append(
            "knowledge/ 가 없다: 지식 문서·도메인 용어 점검을 건너뛴다 "
            "(지식 저장소를 clone 하거나 cp -r .claude/knowledge-template knowledge)"
        )
    else:
        kb = load_boundary(KBOUNDARY)
        groups = set(kb.get("doc-groups", []))
        if not groups:
            warnings.append(f"{rel(KBOUNDARY)}: [doc-groups] 가 비어 있다 (첫 대상을 편입하기 전에 채운다)")
        check_docs(groups)
        check_runs()
        scan_terms(harness_files, kb.get("harness-forbidden", []), "하네스에 도메인")
        doc_files = [p for p in sorted(KDOCS.rglob("*.md")) if "reference" not in p.relative_to(KDOCS).parts]
        scan_terms(doc_files, hb.get("docs-forbidden", []), "프로젝트 문서에 하네스")

    for w in warnings:
        print(f"경고  {w}")
    for e in errors:
        print(f"오류  {e}")
    print(f"\n오류 {len(errors)}건, 경고 {len(warnings)}건")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
