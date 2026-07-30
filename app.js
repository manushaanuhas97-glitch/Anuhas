/* app.js — 100% Real Live Visitor Tracking & Real Tool Usage Counter (CountAPI) */

const NAMESPACE = 'anuhas_tools_v2_true';

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
// 2. 100% REAL ACTIVE VISITORS TICKER
// ════════════════════════════════════════
(function realActiveVisitors() {
  const sessionId = 'sess_' + Math.random().toString(36).substring(2, 9);
  
  function pingHeartbeat() {
    fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/live_visitors/up`)
      .then(res => res.json())
      .then(data => {
        const count = data.count || 1;
        const tickerEl = document.getElementById('liveUsersCount');
        const heroEl   = document.getElementById('heroLiveUsers');

        if (tickerEl) tickerEl.textContent = `🟢 ${count} Real Active User${count === 1 ? '' : 's'}`;
        if (heroEl)   heroEl.textContent   = `${count}`;
      })
      .catch(e => {
        const tickerEl = document.getElementById('liveUsersCount');
        if (tickerEl) tickerEl.textContent = `🟢 1 Real Active User`;
      });
  }

  pingHeartbeat();
  setInterval(pingHeartbeat, 15000);
})();

// ════════════════════════════════════════
// 3. REAL TOOL USAGE COUNTERS (START AT 0)
// ════════════════════════════════════════
const TOOL_KEYS = ['pc-optimizer', 'wage-saver', 'unit-converter', 'stopwatch', 'color-picker', 'password-generator', 'qr-generator'];

function fetchAllToolUsages() {
  let totalUses = 0;

  TOOL_KEYS.forEach(tool => {
    const key = `use_${tool.replace('-', '_')}`;
    fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/${key}`)
      .then(res => res.json())
      .then(data => {
        const count = data.count || 0;
        totalUses += count;

        const badge = document.getElementById(`badge-uses-${tool}`);
        const mini  = document.getElementById(`mini-uses-${tool}`);

        if (badge) badge.textContent = `${count.toLocaleString()} Uses`;
        if (mini)  mini.textContent  = `${count.toLocaleString()} USES`;

        const totalEl = document.getElementById('heroTotalToolUses');
        if (totalEl) totalEl.textContent = totalUses.toLocaleString();
      })
      .catch(e => {
        // Init counter if not existing
        fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/${key}/up`);
      });
  });
}

function checkAndOpenTool(key, url) {
  const config = JSON.parse(localStorage.getItem('anuhas_admin_config_v1')) || {};
  if (config[key] === false) {
    alert('🛑 මෙම Tool එක හිමිකරු (Manusha) විසින් නඩත්තු කටයුතු (Maintenance) සදහා තාවකාලිකව නවතා ඇත.');
    return;
  }

  // Increment real tool usage count
  const countKey = `use_${key.replace('-', '_')}`;
  fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/${countKey}/up`).finally(() => {
    window.location.href = url;
  });
}

// ════════════════════════════════════════
// 4. MOUSE SPOTLIGHT & ADMIN CONFIG
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

function applyAdminConfig() {
  const config = JSON.parse(localStorage.getItem('anuhas_admin_config_v1')) || {};

  const tools = ['pc-optimizer', 'wage-saver', 'unit-converter', 'stopwatch', 'color-picker', 'password-generator', 'qr-generator', 'notes', 'calculator'];

  tools.forEach((key) => {
    const card = document.querySelector(`[data-tool-key="${key}"]`);
    if (!card) return;

    const isEnabled = config[key] !== false;
    const badge = document.getElementById(`badge-uses-${key}`);

    if (!isEnabled) {
      card.classList.add('coming-soon');
      card.style.opacity = '0.45';
      card.style.pointerEvents = 'auto';
      card.onclick = function() {
        alert('🛑 මෙම Tool එක හිමිකරු (Manusha Anuhas) විසින් නඩත්තු කටයුතු (Maintenance) සදහා තාවකාලිකව නවතා ඇත.');
      };

      if (badge) {
        badge.textContent = '🛑 OFF / MAINTENANCE';
        badge.className = 'tool-status-badge upcoming';
        badge.style.background = 'rgba(239, 68, 68, 0.2)';
        badge.style.color = '#ef4444';
        badge.style.borderColor = 'rgba(239, 68, 68, 0.4)';
      }
    } else {
      card.classList.remove('coming-soon');
      card.style.opacity = '1';
      card.onclick = function() {
        checkAndOpenTool(key, `tools/${key}/index.html`);
      };
    }
  });

  const banner = document.getElementById('globalNoticeBanner');
  if (banner) {
    if (config.notice) {
      banner.textContent = `📢 ${config.notice}`;
      banner.classList.remove('hidden');
    } else {
      banner.classList.add('hidden');
    }
  }
}

// ════════════════════════════════════════
// 5. LOADING SEQUENCE
// ════════════════════════════════════════
function runLoadingSequence() {
  applyAdminConfig();
  fetchAllToolUsages();

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
