// Wage Saver — app.js
// ════════════════════════════

const STORAGE_KEY = 'anuhas-wage-saver-v1';
const GOAL_KEY    = 'anuhas-wage-goal-v1';

let transactions = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
let goal         = JSON.parse(localStorage.getItem(GOAL_KEY))    || null;
let currentType  = 'income';
let pendingDeleteId = null;
let chartInstance   = null;

const CAT_ICONS = {
  salary:'💼', freelance:'💻', bonus:'🎁', 'other-income':'💵',
  food:'🍚', transport:'🚗', utilities:'⚡', entertainment:'🎮',
  health:'🏥', 'other-exp':'📦'
};
const INCOME_CATS  = ['salary','freelance','bonus','other-income'];

// ── Init ──────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('entryDate').valueAsDate = new Date();
  bindEvents();
  populateMonthFilter();
  renderAll();
  initChart();
});

function bindEvents() {
  // Tabs
  document.getElementById('tabIncome').addEventListener('click',  () => switchTab('income'));
  document.getElementById('tabExpense').addEventListener('click', () => switchTab('expense'));

  // Form
  document.getElementById('entryForm').addEventListener('submit', addEntry);

  // Goal
  document.getElementById('setGoalBtn').addEventListener('click', () => {
    document.getElementById('goalForm').classList.toggle('hidden');
    document.getElementById('goalDisplay').classList.toggle('hidden');
  });
  document.getElementById('saveGoalBtn').addEventListener('click', saveGoal);
  document.getElementById('cancelGoalBtn').addEventListener('click', () => {
    document.getElementById('goalForm').classList.add('hidden');
    document.getElementById('goalDisplay').classList.remove('hidden');
  });

  // Delete modal
  document.getElementById('confirmDel').addEventListener('click', confirmDelete);
  document.getElementById('cancelDel').addEventListener('click', closeModal);
}

// ── Tab switch ────────────────────────────────────
window.switchTab = function(type) {
  currentType = type;
  document.getElementById('tabIncome').classList.toggle('active', type === 'income');
  document.getElementById('tabExpense').classList.toggle('active', type === 'expense');
  const cat = document.getElementById('entryCategory');
  const btn = document.getElementById('addBtn');
  if (type === 'income') {
    cat.innerHTML = `
      <option value="salary">💼 වැටුප</option>
      <option value="freelance">💻 Freelance</option>
      <option value="bonus">🎁 Bonus</option>
      <option value="other-income">💵 වෙනත් ආදායම</option>`;
    btn.textContent = '💼 ආදායම එකතු කරන්න';
  } else {
    cat.innerHTML = `
      <option value="food">🍚 ආහාර</option>
      <option value="transport">🚗 ගමන්</option>
      <option value="utilities">⚡ Bills</option>
      <option value="entertainment">🎮 විනෝද</option>
      <option value="health">🏥 සෞඛ්‍ය</option>
      <option value="other-exp">📦 වෙනත්</option>`;
    btn.textContent = '🛒 වියදම එකතු කරන්න';
  }
};

// ── Add Entry ─────────────────────────────────────
function addEntry(e) {
  e.preventDefault();
  const desc   = document.getElementById('entryDesc').value.trim();
  const amount = parseFloat(document.getElementById('entryAmount').value);
  const date   = document.getElementById('entryDate').value;
  const cat    = document.getElementById('entryCategory').value;
  const note   = document.getElementById('entryNote').value.trim();

  if (!desc || isNaN(amount) || amount <= 0) { showToast('⚠️ විස්තරය සහ වලංගු මුදලක් ඇතුළු කරන්න!', 'error'); return; }

  transactions.unshift({
    id: Date.now(),
    type: currentType,
    desc, amount, date, cat, note
  });
  save();
  document.getElementById('entryForm').reset();
  document.getElementById('entryDate').valueAsDate = new Date();
  populateMonthFilter();
  renderAll();
  showToast(currentType === 'income' ? '✅ ආදායම් ගනුදෙනුව එකතු විය!' : '✅ වියදම් ගනුදෙනුව එකතු විය!', 'success');
}

// ── Save Goal ─────────────────────────────────────
function saveGoal() {
  const name   = document.getElementById('goalName').value.trim();
  const amount = parseFloat(document.getElementById('goalAmount').value);
  if (!name || isNaN(amount) || amount <= 0) { showToast('⚠️ ඉලක්කයේ නම සහ මුදල ඇතුළු කරන්න!', 'error'); return; }
  goal = { name, amount };
  localStorage.setItem(GOAL_KEY, JSON.stringify(goal));
  document.getElementById('goalForm').classList.add('hidden');
  document.getElementById('goalDisplay').classList.remove('hidden');
  renderAll();
  showToast('🎯 ඉලක්කය සුරැකිණ!', 'success');
}

// ── Render All ────────────────────────────────────
function renderAll() {
  const totalIncome   = transactions.filter(t => t.type === 'income').reduce((s,t) => s + t.amount, 0);
  const totalExpenses = transactions.filter(t => t.type === 'expense').reduce((s,t) => s + t.amount, 0);
  const totalSavings  = totalIncome - totalExpenses;

  document.getElementById('totalIncome').textContent   = fmt(totalIncome);
  document.getElementById('totalExpenses').textContent = fmt(totalExpenses);
  document.getElementById('totalSavings').textContent  = fmt(totalSavings);
  document.getElementById('totalSavings').style.color  = totalSavings >= 0 ? '#10b981' : '#ef4444';

  // Goal
  if (goal) {
    const pct = Math.min(Math.round((totalSavings / goal.amount) * 100), 100);
    document.getElementById('goalProgress').textContent = pct + '%';
    document.getElementById('goalDisplay').innerHTML = `
      <div class="goal-progress-card">
        <div class="goal-info-row">
          <span class="goal-name">🎯 ${goal.name}</span>
          <span class="goal-amounts"><span>${fmt(Math.max(totalSavings,0))}</span> / ${fmt(goal.amount)}</span>
        </div>
        <div class="goal-track"><div class="goal-fill" style="width:${pct}%"></div></div>
        <div class="goal-pct">${pct}% සම්පූර්ණ ${pct >= 100 ? '🎉' : ''}</div>
      </div>`;
  } else {
    document.getElementById('goalProgress').textContent = '0%';
    document.getElementById('goalDisplay').innerHTML = '<p class="no-data">ඉලක්කයක් සකසා නොමැත.</p>';
  }

  // Savings rate
  const rate = totalIncome > 0 ? Math.max(0, Math.min(100, Math.round((totalSavings / totalIncome) * 100))) : 0;
  document.getElementById('rateFill').style.width = rate + '%';
  document.getElementById('rateText').textContent  = rate + '%';

  // Chart mini stats
  document.getElementById('chartIncome').textContent  = fmt(totalIncome);
  document.getElementById('chartExpense').textContent = fmt(totalExpenses);
  document.getElementById('chartSaving').textContent  = fmt(totalSavings);

  updateChart();
  renderTxns();
}

// ── Transactions ──────────────────────────────────
window.renderTxns = function() {
  const filterType  = document.getElementById('filterType').value;
  const filterMonth = document.getElementById('filterMonth').value;

  let list = transactions.filter(t => {
    if (filterType !== 'all' && t.type !== filterType) return false;
    if (filterMonth !== 'all' && !t.date.startsWith(filterMonth)) return false;
    return true;
  });

  const container = document.getElementById('txnList');
  if (list.length === 0) {
    container.innerHTML = '<p class="no-data">ගනුදෙනු නොමැත.</p>';
    return;
  }
  container.innerHTML = list.map(t => `
    <div class="txn-item" id="txn-${t.id}">
      <span class="txn-icon">${CAT_ICONS[t.cat] || (t.type==='income' ? '💼' : '🛒')}</span>
      <div class="txn-info">
        <div class="txn-desc">${t.desc}</div>
        <div class="txn-meta">${fmtDate(t.date)} · ${t.cat}</div>
        ${t.note ? `<div class="txn-note">${t.note}</div>` : ''}
      </div>
      <span class="txn-amount ${t.type}">${t.type==='income' ? '+' : '-'}${fmt(t.amount)}</span>
      <button class="txn-del" onclick="askDelete(${t.id})" title="මකන්න">🗑️</button>
    </div>`).join('');
};

window.askDelete = function(id) {
  pendingDeleteId = id;
  document.getElementById('modal').classList.remove('hidden');
};
function closeModal() {
  pendingDeleteId = null;
  document.getElementById('modal').classList.add('hidden');
}
function confirmDelete() {
  if (pendingDeleteId) {
    transactions = transactions.filter(t => t.id !== pendingDeleteId);
    save();
    renderAll();
    showToast('🗑️ ගනුදෙනුව මකා දැමිණ.', 'success');
  }
  closeModal();
}

// ── Chart ─────────────────────────────────────────
function initChart() {
  const ctx = document.getElementById('myChart').getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: { labels: [], datasets: [
      { label: 'ආදායම', data: [], backgroundColor: 'rgba(16,185,129,0.7)', borderRadius: 8 },
      { label: 'වියදම',  data: [], backgroundColor: 'rgba(239,68,68,0.7)',  borderRadius: 8 }
    ]},
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: '#94a3b8', font: { family: 'Outfit' }}}},
      scales: {
        x: { ticks: { color: '#64748b' }, grid: { color: 'rgba(255,255,255,0.05)' }},
        y: { ticks: { color: '#64748b', callback: v => 'රු.' + v.toLocaleString() }, grid: { color: 'rgba(255,255,255,0.05)' }}
      }
    }
  });
}

function updateChart() {
  if (!chartInstance) return;
  const months = {};
  transactions.forEach(t => {
    if (!t.date) return;
    const key = t.date.slice(0,7);
    if (!months[key]) months[key] = { income: 0, expense: 0 };
    months[key][t.type] += t.amount;
  });
  const sorted = Object.keys(months).sort().slice(-6);
  chartInstance.data.labels              = sorted.map(m => { const [y,mo] = m.split('-'); return `${mo}/${y.slice(2)}`; });
  chartInstance.data.datasets[0].data   = sorted.map(m => months[m].income);
  chartInstance.data.datasets[1].data   = sorted.map(m => months[m].expense);
  chartInstance.update();
}

// ── Helpers ───────────────────────────────────────
function fmt(n)     { return 'රු. ' + Math.abs(n).toLocaleString('si-LK', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function fmtDate(d) { if (!d) return ''; const [y,m,day] = d.split('-'); return `${day}/${m}/${y}`; }
function save()     { localStorage.setItem(STORAGE_KEY, JSON.stringify(transactions)); }

function populateMonthFilter() {
  const months = [...new Set(transactions.map(t => t.date ? t.date.slice(0,7) : '').filter(Boolean))].sort().reverse();
  const sel = document.getElementById('filterMonth');
  const cur = sel.value;
  sel.innerHTML = '<option value="all">සියලු මාස</option>' + months.map(m => {
    const [y, mo] = m.split('-');
    return `<option value="${m}" ${m===cur?'selected':''}>${mo}/${y}</option>`;
  }).join('');
}

function showToast(msg, type = '') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast ' + type + ' show';
  setTimeout(() => t.classList.remove('show'), 3000);
}

window.exportData = function() {
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ transactions, goal }));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", `anuhas-wage-saver-backup.json`);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
  showToast('📥 Data exported successfully!', 'success');
};

window.resetAllData = function() {
  if (confirm('ඔබේ සියලුම ගනුදෙනු සහ ඉලක්ක මකා දැමීමට අවශ්‍යද? (Are you sure you want to reset all data?)')) {
    transactions = [];
    goal = null;
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(GOAL_KEY);
    renderAll();
    showToast('🗑️ Data reset successfully.', 'success');
  }
};

