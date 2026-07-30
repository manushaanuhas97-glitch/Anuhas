/* app.js — Particles + Spotlights + Live Users Ticker + Admin Config Sync */

// ════════════════════════════════════════
// 1. BACKGROUND PARTICLE CANVAS ENGINE
// ════════════════════════════════════════
(function initParticles() {
  const canvas = document.getElementById('bgCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  const particleCount = 45;

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 2 + 1,
      dx: (Math.random() - 0.5) * 0.4,
      dy: (Math.random() - 0.5) * 0.4,
      alpha: Math.random() * 0.5 + 0.2
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach((p) => {
      p.x += p.dx;
      p.y += p.dy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(167, 139, 250, ${p.alpha})`;
      ctx.shadowBlur = 8;
      ctx.shadowColor = '#a78bfa';
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  draw();
})();

// ════════════════════════════════════════
// 2. REAL LIVE VISITORS COUNTER (CounterAPI)
// ════════════════════════════════════════
(function liveUsersTicker() {
  const NAMESPACE = 'anuhas_tools_v1';
  
  function updateRealVisits() {
    // Ping pageview count
    fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/live_visitors/up`)
      .then(res => res.json())
      .then(data => {
        const count = data.count || 1;
        const tickerEl = document.getElementById('liveUsersCount');
        const heroEl   = document.getElementById('heroLiveUsers');

        if (tickerEl) tickerEl.textContent = `🟢 ${count} Real Visitors`;
        if (heroEl)   heroEl.textContent   = `${count}`;
      })
      .catch(e => {
        // Fallback gracefully
        const tickerEl = document.getElementById('liveUsersCount');
        if (tickerEl) tickerEl.textContent = `🟢 1 Real Visitor`;
      });
  }

  updateRealVisits();
  setInterval(updateRealVisits, 15000);
})();

// ════════════════════════════════════════
// 3. CARD MOUSE SPOTLIGHT EFFECT
// ════════════════════════════════════════
document.addEventListener('mousemove', (e) => {
  document.querySelectorAll('.tool-card').forEach((card) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  });
});

// ════════════════════════════════════════
// 4. ADMIN CONFIG SYNC & MAINTENANCE MODES
// ════════════════════════════════════════
const CONFIG_KEY = 'anuhas_admin_config_v1';

function applyAdminConfig() {
  const config = JSON.parse(localStorage.getItem(CONFIG_KEY)) || {};

  // Check tools status
  document.querySelectorAll('.tool-card').forEach((card) => {
    const key = card.getAttribute('data-tool-key');
    if (!key) return;

    const isEnabled = config[key] !== false;
    const badge = document.getElementById(`badge-${key}`);

    if (!isEnabled) {
      card.classList.add('coming-soon');
      if (badge) {
        badge.textContent = 'OFF / MAINTENANCE';
        badge.className = 'tool-status-badge upcoming';
      }
    }
  });

  // Notice banner
  const banner = document.getElementById('globalNoticeBanner');
  if (banner && config.notice) {
    banner.textContent = `📢 ${config.notice}`;
    banner.classList.remove('hidden');
  }
}

function checkAndOpenTool(key, url) {
  const config = JSON.parse(localStorage.getItem(CONFIG_KEY)) || {};
  if (config[key] === false) {
    alert('🛑 මෙම Tool එක හිමිකරු (Manusha) විසින් නඩත්තු කටයුතු (Maintenance) සදහා තාවකාලිකව නවතා ඇත. (Temporarily Disabled by Owner)');
    return;
  }
  window.location.href = url;
}

// ════════════════════════════════════════
// 5. LOADING SEQUENCE
// ════════════════════════════════════════
function runLoadingSequence() {
  applyAdminConfig();

  const bag         = document.getElementById('bag');
  const brandReveal = document.getElementById('brandReveal');
  const burstItems  = document.querySelectorAll('.burst-item');
  const loadScreen  = document.getElementById('loadingScreen');
  const mainSite    = document.getElementById('mainSite');

  setTimeout(() => { if (bag) bag.classList.add('opening'); }, 800);

  setTimeout(() => {
    burstItems.forEach((el, i) => {
      setTimeout(() => el.classList.add('fly'), i * 80);
    });
  }, 1400);

  setTimeout(() => {
    if (brandReveal) brandReveal.classList.add('show');
  }, 1900);

  setTimeout(() => {
    if (loadScreen) loadScreen.classList.add('fade-out');
    setTimeout(() => {
      if (loadScreen) loadScreen.style.display = 'none';
      if (mainSite)   mainSite.classList.remove('hidden');
      document.body.style.overflow = 'auto';
    }, 800);
  }, 3600);
}

document.fonts.ready.then(runLoadingSequence);

// ════════════════════════════════════════
// 6. SEARCH & CATEGORY FILTERING
// ════════════════════════════════════════
function filterTools() {
  const query = document.getElementById('toolSearchInput').value.toLowerCase().trim();
  const cards = document.querySelectorAll('.tool-card');

  cards.forEach((card) => {
    const name = card.getAttribute('data-name') || '';
    if (name.includes(query)) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

function filterCategory(cat, btn) {
  document.querySelectorAll('.filter-pill').forEach((p) => p.classList.remove('active'));
  btn.classList.add('active');

  const cards = document.querySelectorAll('.tool-card');
  cards.forEach((card) => {
    const cardCat = card.getAttribute('data-category');
    if (cat === 'all' || cardCat === cat) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

function openTool(url) {
  window.location.href = url;
}
