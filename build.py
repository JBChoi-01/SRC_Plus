#!/usr/bin/env python3
"""
build.py — reports/ 폴더를 스캔해 index.html의 REPORTS 배열을 자동 갱신합니다.

사용법:
    python build.py

동작:
    1. reports/ 폴더의 모든 html 파일을 순회
    2. 각 파일 상단의 <script id="report-meta"> 블록에서 메타데이터 추출
    3. 파일명 규칙({cat}_{slug}_{YYMMDD}_{author}.html)에서 추가 정보 파싱
    4. index.html의 REPORTS 배열을 추출한 데이터로 교체
"""

import os
import re
import json

# 스크립트가 어느 경로에서 실행되든 build.py 위치를 기준으로 동작
os.chdir(os.path.dirname(os.path.abspath(__file__)))

REPORTS_DIR = "reports"
INDEX_FILE = "index.html"

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
    파일명에서 cat, slug, date, author를 파싱합니다.
    형식: {cat}_{slug}_{YYMMDD}_{author}.html
    예: sectors_land-reclamation_250624_jbchoi.html
    """
    name = filename.replace(".html", "")
    parts = name.split("_")
    if len(parts) < 4:
        return None
    return {
        "cat": parts[0],
        "slug": "_".join(parts[1:-2]),  # 슬러그에 _ 포함 가능
        "date": parts[-2],
        "author": parts[-1],
    }


def date_to_display(yymmdd):
    """250624 → 2025-06"""
    if len(yymmdd) == 6:
        yy, mm = yymmdd[:2], yymmdd[2:4]
        return f"20{yy}-{mm}"
    return yymmdd


def collect_reports():
    """reports/ 폴더를 스캔해 메타데이터 목록을 반환합니다."""
    if not os.path.isdir(REPORTS_DIR):
        print(f"[오류] '{REPORTS_DIR}' 폴더를 찾을 수 없습니다.")
        return []

    reports = []
    for filename in sorted(os.listdir(REPORTS_DIR)):
        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(REPORTS_DIR, filename)
        file_info = parse_filename(filename)
        if not file_info:
            print(f"  [경고] 파일명 규칙 불일치, 건너뜀: {filename}")
            continue

        meta = extract_meta(filepath)
        if not meta:
            continue

        # 메타 블록 우선, 파일명은 보조
        report = {
            "cat":       meta.get("cat",    file_info["cat"]),
            "topic":     meta.get("topic",  ""),
            "title":     meta.get("title",  ""),
            "date":      date_to_display(meta.get("date", file_info["date"])),
            "author":    meta.get("author", file_info["author"]),
            "href":      f"reports/{filename}",
            "published": meta.get("published", False),
            "upcoming":  meta.get("upcoming",  False),
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
        for n, r in enumerate(cat_reports, start=1):
            upcoming_str = ", upcoming: true" if r.get("upcoming") else ""
            published_str = ", published: true" if r.get("published") else ""
            lines.append(
                f'  {{ cat: \'{r["cat"]}\', topic: "{r["topic"]}", '
                f'title: "{r["title"]}", date: \'{r["date"]}\', '
                f'author: \'{r["author"]}\', n: {n}, '
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
    print(f"[1] {REPORTS_DIR}/ 폴더 스캔 중...")
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
