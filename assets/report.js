/* report.js — 본문 공용 동작
   1) 상단 읽기 진행바
   2) 목차 현재 섹션 하이라이트 */
(function () {
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

  // 목차 active 표시
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
