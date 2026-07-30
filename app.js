/* app.js — Loading animation + main logic */

// ════════════════════════════════════════
// STARS
// ════════════════════════════════════════
(function createStars() {
  const container = document.getElementById('stars');
  if (!container) return;
  for (let i = 0; i < 120; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 3 + 1;
    s.style.cssText = `
      width: ${size}px; height: ${size}px;
      top: ${Math.random() * 100}%;
      left: ${Math.random() * 100}%;
      --dur: ${(Math.random() * 4 + 2).toFixed(1)}s;
      animation-delay: ${(Math.random() * 4).toFixed(1)}s;
    `;
    container.appendChild(s);
  }
})();

// ════════════════════════════════════════
// LOADING SEQUENCE
// ════════════════════════════════════════
function runLoadingSequence() {
  const bag         = document.getElementById('bag');
  const toolBurst   = document.getElementById('toolBurst');
  const brandReveal = document.getElementById('brandReveal');
  const burstItems  = document.querySelectorAll('.burst-item');
  const loadScreen  = document.getElementById('loadingScreen');
  const mainSite    = document.getElementById('mainSite');

  // Phase 1 — 800ms: walk & wiggle (already animating via CSS)

  // Phase 2 — open bag zipper
  setTimeout(() => {
    if (bag) bag.classList.add('opening');
  }, 900);

  // Phase 3 — tools burst out
  setTimeout(() => {
    burstItems.forEach((el, i) => {
      setTimeout(() => el.classList.add('fly'), i * 80);
    });
  }, 1600);

  // Phase 4 — brand reveal
  setTimeout(() => {
    if (brandReveal) brandReveal.classList.add('show');
  }, 2000);

  // Phase 5 — loading bar finishes, then transition to main site
  setTimeout(() => {
    if (loadScreen) loadScreen.classList.add('fade-out');
    setTimeout(() => {
      if (loadScreen) loadScreen.style.display = 'none';
      if (mainSite)   mainSite.classList.remove('hidden');
      document.body.style.overflow = 'auto';
    }, 800);
  }, 3800);
}

// Wait for fonts
document.fonts.ready.then(runLoadingSequence);

// ════════════════════════════════════════
// OPEN TOOL
// ════════════════════════════════════════
function openTool(url) {
  window.location.href = url;
}

// ════════════════════════════════════════
// SMOOTH SCROLL for nav links
// ════════════════════════════════════════
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
