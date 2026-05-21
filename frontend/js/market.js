// Fetch market data from backend and render a small market-cap chart
(async function(){
  if (typeof window.API_BASE_URL === 'undefined') {
    window.API_BASE_URL = (window.location.origin && window.location.origin !== 'null' && window.location.protocol !== 'file:') ? window.location.origin : 'http://localhost:5000';
  }
})();

async function fetchMarket(top = 8) {
  const res = await fetch(`${window.API_BASE_URL}/api/market?top=${top}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

function renderMarketChart(items, containerId = 'marketWidget'){
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';
  const canvas = document.createElement('canvas');
  canvas.id = containerId + '-chart';
  canvas.style.width = '100%';
  canvas.style.height = '220px';
  container.appendChild(canvas);

  if (window.__marketChart) {
    try { window.__marketChart.destroy(); } catch(e){}
    window.__marketChart = null;
  }

  if (typeof Chart === 'undefined') {
    container.innerHTML = '<div style="padding:12px;color:#94a3b8">Chart.js not loaded</div>';
    return;
  }

  const labels = items.map(i => `${i.symbol}`);
  const values = items.map(i => Number(i.market_cap) || 0);
  const colors = items.map((_, idx) => ['#3b82f6','#10b981','#f97316','#ef4444','#6366f1','#06b6d4','#f59e0b','#8b5cf6'][idx%8]);

  const ctx = canvas.getContext('2d');
  window.__marketChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: 'Market Cap', data: values, backgroundColor: colors }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: function(ctx){ return 'Market Cap: $' + Number(ctx.parsed.y).toLocaleString(); }}}},
      scales: { y: { beginAtZero: true, ticks: { callback: v => v >= 1 ? '$' + Number(v).toLocaleString() : v } } }
    }
  });
}

async function loadMarketWidget(top = 6, containerId = 'marketWidget'){
  try{
    const data = await fetchMarket(top);
    renderMarketChart(data, containerId);
  } catch (err) {
    const c = document.getElementById(containerId);
    if (c) c.innerHTML = `<div style="padding:12px;color:#f97316">Unable to load market data</div>`;
    console.warn('[Market] Error loading market data:', err.message);
  }
}

window.loadMarketWidget = loadMarketWidget;
