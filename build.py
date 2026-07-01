#!/usr/bin/env python3
"""
build.py — 저장소 루트를 스캔해 index.html의 REPORTS 배열을 자동 갱신합니다.

사용법:
    python build.py

동작:
    1. 저장소 루트에서 'reports_'로 시작하는 모든 html 파일을 순회
       (reports/ 하위 폴더가 아니라 루트 직속 파일을 대상으로 한다)
    2. 각 파일 상단의 <script id="report-meta"> 블록에서 메타데이터 추출
    3. 파일명 규칙(reports_{cat}_{slug}_{seq}.html)에서 cat, slug, seq 파싱
       - seq는 기여자가 파일명에 직접 부여한 값을 그대로 읽어올 뿐,
         이 스크립트가 자동으로 번호를 매기지 않는다.
    4. index.html의 REPORTS 배열을 추출한 데이터로 교체
"""

import os
import re
import json

# 스크립트가 어느 경로에서 실행되든 build.py 위치를 기준으로 동작
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = "."
INDEX_FILE = "index.html"
FILENAME_PREFIX = "reports_"

CAT_ORDER = ["insights", "issues", "sectors"]
CAT_META = {
    "insights": {"label": "Insights", "sub": "개념·구조 해설"},
    "issues":   {"label": "Issues",   "sub": "시장·정책·딜 이슈"},
    "sectors":  {"label": "Sectors",  "sub": "자산군·산업군 정리"},
}


def extract_meta(filepath):
    """html 파일에서 report-meta JSON 블록을 추출합니다."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    match = re.search(
        r'<script[^>]+id=["\']report-meta["\'][^>]*>(.*?)</script>',
        content,
        re.DOTALL
    )
    if not match:
        print(f"  [경고] 메타데이터 없음: {filepath}")
        return None

    try:
        meta = json.loads(match.group(1).strip())
    except json.JSONDecodeError as e:
        print(f"  [오류] JSON 파싱 실패 ({filepath}): {e}")
        return None

    return meta


def parse_filename(filename):
    """
    파일명에서 cat, slug, seq를 파싱합니다.
    형식 1 (시리즈물): reports_{cat}_{slug}_{seq}.html
        예: reports_insights_kb-balhae_2.html → cat='insights', slug='kb-balhae', seq=2
    형식 2 (단일 리포트, seq 생략): reports_{cat}_{slug}.html
        예: reports_sectors_land-reclamation.html → cat='sectors', slug='land-reclamation', seq=1(내부 기본값)

    규칙: 접두어(reports_)를 뗀 뒤, 마지막 토큰이 숫자면 그것을 seq로 보고 나머지를 slug로 삼는다.
          마지막 토큰이 숫자가 아니면(=seq 생략) 전체를 slug로 보고 seq는 1로 취급한다.
          (단일 리포트는 시리즈가 아니므로 파일명에 번호를 붙이지 않는다.)
    """
    name = filename.replace(".html", "")
    if not name.startswith(FILENAME_PREFIX):
        return None
    name = name[len(FILENAME_PREFIX):]  # {cat}_{slug}[_{seq}]

    parts = name.split("_")
    if len(parts) < 2:
        print(f"  [경고] 파일명 형식 불일치(reports_{{cat}}_{{slug}}[_{{seq}}].html 아님), 건너뜀: {filename}")
        return None

    cat = parts[0]
    rest = parts[1:]

    if rest[-1].isdigit():
        seq = int(rest[-1])
        slug = "_".join(rest[:-1])
    else:
        seq = 1  # 단일 리포트: seq 생략, 내부적으로 1로 취급
        slug = "_".join(rest)

    if not slug:
        print(f"  [경고] slug가 비어 있음, 건너뜀: {filename}")
        return None

    if cat not in CAT_ORDER:
        print(f"  [경고] 알 수 없는 카테고리 '{cat}', 건너뜀: {filename}")
        return None

    return {
        "cat": cat,
        "slug": slug,
        "seq": seq,
    }


def collect_reports():
    """저장소 루트에서 reports_*.html 파일을 스캔해 메타데이터 목록을 반환합니다."""
    reports = []
    for filename in sorted(os.listdir(ROOT_DIR)):
        if not filename.startswith(FILENAME_PREFIX) or not filename.endswith(".html"):
            continue

        file_info = parse_filename(filename)
        if not file_info:
            continue

        meta = extract_meta(filename)
        if not meta:
            continue

        report = {
            "cat":       meta.get("cat", file_info["cat"]),
            "topic":     meta.get("topic", ""),
            "title":     meta.get("title", ""),
            "date":      meta.get("date", ""),
            "author":    meta.get("author", ""),
            "seq":       file_info["seq"],
            "href":      filename,  # 루트 직속이므로 경로 접두어 없이 파일명 그대로
            "published": meta.get("published", False),
            "upcoming":  meta.get("upcoming", False),
        }
        reports.append(report)
        print(f"  [수집] {filename} → {report['topic']} / {report['title']}")

    return reports


def build_reports_js(reports):
    """REPORTS 배열 JS 코드를 생성합니다."""
    lines = ["const REPORTS = ["]

    for cat in CAT_ORDER:
        cat_reports = [r for r in reports if r["cat"] == cat]
        if not cat_reports:
            continue

        lines.append(f"  // ── {cat.upper()} ──")
        for r in cat_reports:
            upcoming_str = ", upcoming: true" if r.get("upcoming") else ""
            published_str = ", published: true" if r.get("published") else ""
            lines.append(
                f'  {{ cat: \'{r["cat"]}\', topic: "{r["topic"]}", '
                f'title: "{r["title"]}", date: \'{r["date"]}\', '
                f'author: \'{r["author"]}\', n: {r["seq"]}, '
                f'href: \'{r["href"]}\'{published_str}{upcoming_str} }},'
            )

    lines.append("];")
    return "\n".join(lines)


def update_index(new_reports_js):
    """index.html의 REPORTS 배열을 교체합니다."""
    with open(INDEX_FILE, encoding="utf-8") as f:
        content = f.read()

    # const REPORTS = [ ... ]; 블록을 찾아 교체
    pattern = re.compile(
        r'(const REPORTS\s*=\s*\[).*?(\];)',
        re.DOTALL
    )
    if not pattern.search(content):
        print("[오류] index.html에서 REPORTS 배열을 찾을 수 없습니다.")
        return False

    new_content = pattern.sub(new_reports_js, content)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    print("=== build.py 시작 ===")
    print(f"[1] 저장소 루트에서 '{FILENAME_PREFIX}*.html' 스캔 중...")
    reports = collect_reports()

    if not reports:
        print("[완료] 수집된 리포트 없음. index.html 업데이트 생략.")
        return

    print(f"\n[2] REPORTS 배열 생성 중... ({len(reports)}개)")
    new_js = build_reports_js(reports)

    print(f"\n[3] {INDEX_FILE} 업데이트 중...")
    if update_index(new_js):
        print(f"[완료] {INDEX_FILE} 업데이트 성공 — 총 {len(reports)}개 리포트")
    else:
        print("[실패] index.html 업데이트 실패")


if __name__ == "__main__":
    main()
