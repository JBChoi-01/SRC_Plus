# 리포트 변환 작업 지시서 (코딩 에이전트용)

이 파일은 자동으로 로드되지 않는다. 참여자가 코딩 에이전트에게 "prompt-for-agent.md를 읽고 이 지시에 따라 작업해줘"라고 명시적으로 요청했을 때만 읽힌다. 이 저장소(SRC_Plus)에 연결된 상태에서, 참여자가 제공하는 원본 자료를 표준 리포트 HTML로 변환하는 것이 목적이다.

## 0단계 — 시작 전 필수 확인

아래 정보 없이는 작업을 시작하지 않는다. 추측하지 말고 반드시 참여자에게 먼저 물어본다.

- **author ID** (예: jbchoi, jhahn, sjahn)
- **cat** — insights / issues / sectors 중 하나
- **시리즈물 여부** — 2편 이상 이어지는 시리즈물이면 seq 번호(1, 2, 3...)를 몇 번째 글인지 물어본다. 한 편으로 끝나는 단일 리포트면 seq 없이 진행한다.
- **원본 자료** — 파일 경로, 붙여넣은 텍스트, 링크 등 참여자가 준 형태 그대로 확인한다. 원본 자료가 Word(.docx), PowerPoint(.pptx), Excel(.xlsx) 등 오피스 포맷이라 직접 읽을 수 없는 경우, 참여자에게 PDF로 변환해서 다시 달라고 요청한다. PDF나 텍스트 계열 파일(md, txt, csv 등)은 바로 읽는다.

## 1단계 — 참조 파일 확인

저장소에 이미 있는 아래 파일을 직접 읽는다. 참여자에게 별도로 첨부해달라고 요청하지 않는다.

- `assets_report.css` — 디자인 시스템 CSS
- `assets_report.js` — 공용 스크립트
- 저장소 루트의 `reports_*.html` 파일 중 아무거나 하나 — HTML 구조·말투·포맷 참조용

## 2단계 — 파일명 규칙 (최종본 기준)

```
reports_{cat}_{slug}_{seq}.html   (2편 이상 이어지는 시리즈물)
reports_{cat}_{slug}.html         (한 편으로 끝나는 단일 리포트 — seq 생략)
```

- `cat`: insights / issues / sectors 중 하나
- `slug`: 주제를 영어로 요약, 단어는 하이픈(-)으로 연결. 시리즈 번호는 넣지 않는다.
- `seq`: 시리즈물일 때만 붙인다. 0단계에서 확인한 번호를 사용한다.

## 3단계 — report-meta 블록

아래 6개 필드는 모두 필수이며 하나도 빠짐없이 포함한다. `published`는 항상 `true`로 고정하고 임의로 생략하거나 다른 값으로 바꾸지 않는다. 파일 최상단 `<!DOCTYPE html>` 바로 뒤에 아래 형식으로 작성한다.

```html
<script type="application/json" id="report-meta">
{
  "title": "리포트 제목 (한국어, 문장형)",
  "topic": "주제어 (짧게, 예: 공유수면매립사업)",
  "cat": "insights / issues / sectors 중 하나",
  "date": "최초 작성일 YYMMDD (신규 작성이면 오늘 날짜, 기존 리포트 수정이면 처음 게시했던 날짜 그대로 유지 — 수정일로 바꾸지 않음)",
  "author": "0단계에서 확인한 author ID",
  "published": true
}
</script>
```

## 4단계 — HTML 구조

1단계에서 확인한 레퍼런스 리포트의 HTML 구조를 그대로 따른다. `topbar`, `article.article`, `footer.article-foot` 구조를 유지한다. `article-head` 안에는 반드시 아래 두 줄을 비워둔다 (`assets_report.js`가 자동 주입한다):

```html
<p class="a-topic"></p>
<h1 class="a-title"></h1>
```

`a-meta`에는 날짜만 표시하고, author(작성자)는 화면에 표시하지 않는다. 작성자 정보는 `report-meta` JSON의 `author` 필드에만 남긴다.

CSS/JS 경로는 6단계(미리보기)와 8단계(최종본)에서 서로 다르게 처리한다 — 아래 해당 단계를 참고한다.

## 5단계 — 분량 / 말투 / 구성

- **분량**: 본문 텍스트 기준 공백 제외 2,500~5,000자. 짧으면 살을 붙이고, 길면 자연스러운 지점에서 분할해 파일을 2개로 나눈다.
- **말투**: "~이다", "~한다", "~있다" 형태의 건조한 단문 서술체. "~요", "~습니다" 등 구어체 금지. 감상·평가 표현 없이 사실과 구조 중심으로 서술한다.
- **구성**: 섹션 수, 목차 구조, callout·formula·table 사용 여부는 내용에 맞게 자유롭게 결정한다. lead 문단(`p.lead`)으로 시작하는 것을 권장한다.

## 6단계 — 미리보기(_PREVIEW) 버전 먼저 출력

- 파일명 끝에 `_PREVIEW`를 붙인다 (예: `reports_sectors_xxx_1_PREVIEW.html`).
- CSS/JS 참조 경로를 아래 절대경로로 바꿔서 넣는다:
  ```html
  <link rel="stylesheet" href="https://srcplus.vercel.app/assets_report.css">
  <script src="https://srcplus.vercel.app/assets_report.js"></script>
  ```
- 화면(또는 파일 상단)에 "PREVIEW — 업로드 금지"라는 표시를 눈에 띄게 넣는다.
- 참여자가 이 파일을 다운로드해서 로컬 아무 폴더에나 두고 더블클릭으로 열어 확인할 것이다. 인터넷 연결만 있으면 폴더 위치 상관없이 실제 서비스와 동일하게 보인다. 파일 경로를 참여자에게 안내한다.

## 7단계 — 자연어 수정

참여자가 "3번 섹션 표로 바꿔줘" 같은 방식으로 수정을 요청하면, 수정된 새 `_PREVIEW` 파일을 다시 만든다. 수정을 마칠 때마다 매번 응답 끝에 이렇게 리마인드한다: "확인 후 만족스러우면, 업로드 전에 반드시 '최종본 줘'라고 요청하세요. 지금 이 _PREVIEW 파일은 업로드하면 안 됩니다."

## 8단계 — 최종본 요청 시

참여자가 "최종본 줘" 또는 이와 유사한 표현으로 요청하면:

1. 파일명에서 `_PREVIEW`를 뗀다 → `reports_{cat}_{slug}_{seq}.html` (시리즈물) 또는 `reports_{cat}_{slug}.html` (단일 리포트)
2. CSS/JS 경로를 절대경로에서 상대경로로 되돌린다:
   ```html
   href="assets_report.css"
   src="assets_report.js"
   ```
3. "PREVIEW — 업로드 금지" 표시를 제거한다.
4. 완성된 최종 파일명을 참여자에게 명확히 알려준다.

이 최종본 파일이 GitHub에 실제로 올라갈 파일이다.

## 9단계 — 커밋 및 업로드

참여자가 확정을 요청하면:

1. 저장소 루트에 파일이 최종 파일명으로 저장되어 있는지 확인한다.
2. 아래 규칙에 맞는 커밋 메시지로 `main` 브랜치에 직접 커밋한다 (참여자가 다른 방식을 요청하지 않는 한 push까지 진행하기 전에 반드시 참여자에게 확인받는다):

| 메시지 | 사용 시점 | 예시 |
|---|---|---|
| `add:` | 신규 리포트 추가 | `add: reports_issues_asset-lite_1.html` |
| `update:` | 기존 리포트 수정 후 재업로드 | `update: reports_issues_asset-lite_1.html` |
| `remove:` | 리포트 삭제 | `remove: reports_issues_asset-lite_1.html` |

기존 리포트를 수정하는 경우 같은 파일명으로 덮어쓴다. seq 번호를 새로 매기지 않고, `report-meta`의 `date`도 최초 업로드일 그대로 유지한다 (수정일로 바꾸지 않는다).

## 그 외

이 지시서에 없는 예외 상황(카드뉴스 제작, 배포 구조, 파일 구조 전반 등)은 `member-guide.html`을 직접 읽어 확인한다.
