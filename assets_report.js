/* report.js — 본문 공용 동작
   1) report-meta → 본문 제목/부제/페이지 타이틀 자동 주입
   2) 상단 읽기 진행바
   3) 목차 현재 섹션 하이라이트 */
(function () {

  // ── 1. report-meta 주입 ──
  var metaEl = document.getElementById('report-meta');
  if (metaEl) {
    try {
      var meta = JSON.parse(metaEl.textContent.trim());

      // <title> 태그 (브라우저 탭 — topic: title 형식)
      if (meta.title) {
        document.title = (meta.topic ? meta.topic + ': ' : '') + meta.title + ' — RE & Infra Report Archive';
      }

      // .a-topic (작은 라벨)
      var topicEl = document.querySelector('.a-topic');
      if (topicEl && meta.topic) topicEl.textContent = meta.topic;

      // .a-title (h1 — 큰 제목)
      var titleEl = document.querySelector('.a-title');
      if (titleEl && meta.title) titleEl.textContent = meta.title;

      // .a-standfirst (부제 — 필요시)
      var subEl = document.querySelector('.a-standfirst');
      if (subEl) subEl.textContent = '';

    } catch (e) {
      console.warn('report-meta 파싱 실패:', e);
    }
  }

  // ── 2. 읽기 진행바 ──
  var progress = document.querySelector('.progress');
  var doc = document.documentElement;

  function onScroll() {
    if (!progress) return;
    var max = doc.scrollHeight - doc.clientHeight;
    var p = max > 0 ? (doc.scrollTop / max) * 100 : 0;
    progress.style.width = Math.min(100, Math.max(0, p)) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  // ── 3. 목차 active 표시 ──
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
  if (links.length) {
    var map = links.map(function (a) {
      return { a: a, el: document.getElementById(a.getAttribute('href').slice(1)) };
    }).filter(function (m) { return m.el; });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          map.forEach(function (m) { m.a.classList.toggle('active', m.el === e.target); });
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

    map.forEach(function (m) { io.observe(m.el); });
  }
})();
