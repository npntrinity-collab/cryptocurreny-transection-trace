function getCurrentPageName() {
  const pathname = (window.location.pathname || '').split('/').pop() || '';
  return pathname.toLowerCase();
}

function getGraphTheme(pageName) {
  if (pageName.includes('risk')) {
    return {
      nodeColor: '#ef4444',
      borderColor: '#7f1d1d',
      edgeColor: '#fbbf24',
      bgColor: '#fee2e2',
      layout: { name: 'breadthfirst', directed: true, padding: 40 },
      nodeShape: 'round-rectangle'
    };
  }
  if (pageName.includes('cases')) {
    return {
      nodeColor: '#10b981',
      borderColor: '#064e3b',
      edgeColor: '#22c55e',
      bgColor: '#ecfccb',
      layout: { name: 'concentric', fit: true, padding: 30 },
      nodeShape: 'ellipse'
    };
  }
  if (pageName.includes('dashboard')) {
    return {
      nodeColor: '#3b82f6',
      borderColor: '#1e40af',
      edgeColor: '#60a5fa',
      bgColor: '#dbeafe',
      layout: { name: 'cose', animate: true, fit: true, padding: 30 },
      nodeShape: 'ellipse'
    };
  }
  return {
    nodeColor: '#3b82f6',
    borderColor: '#1e293b',
    edgeColor: '#888',
    bgColor: '#f8fafc',
    layout: { name: 'cose', animate: true, fit: true, padding: 30 },
    nodeShape: 'ellipse'
  };
}

// Renders a Cytoscape graph. Accepts either an elements array or an object {nodes:[], edges:[]}
function renderGraph(graphData, options = {}) {
  const container = document.getElementById('graph');
  if (!container) {
    console.warn('[Graph] No graph container found, skipping render.');
    return;
  }

  // Normalize elements
  let elements = graphData;
  if (!elements) elements = [];
  if (elements.nodes || elements.edges) {
    elements = { nodes: elements.nodes || [], edges: elements.edges || [] };
  }

  const nodeCount = (elements.nodes && elements.nodes.length) || (Array.isArray(elements) ? elements.filter(e => e.data && e.data.id).length : 0);

  // If no nodes, bail (higher-level code should fallback to chart)
  if (!nodeCount) {
    console.warn('[Graph] Graph data empty — no nodes to render.');
    if (window.cy) {
      window.cy.destroy();
      window.cy = null;
    }
    return;
  }

  if (window.cy) {
    window.cy.destroy();
    window.cy = null;
  }

  const pageName = options.pageName || getCurrentPageName();
  const theme = getGraphTheme(pageName);

  window.cy = cytoscape({
    container,
    elements,
    style: [
      {
        selector: 'node',
        style: {
          'background-color': theme.nodeColor,
          'border-color': theme.borderColor,
          'border-width': 2,
          width: 42,
          height: 42,
          shape: theme.nodeShape,
          label: 'data(label)',
          color: 'white',
          'font-size': '12px',
          'text-valign': 'center',
          'text-halign': 'center',
          'text-outline-color': theme.borderColor,
          'text-outline-width': 2
        }
      },
      {
        selector: 'edge',
        style: {
          width: 3,
          'line-color': theme.edgeColor,
          'target-arrow-shape': 'triangle',
          'target-arrow-color': theme.edgeColor,
          'curve-style': 'bezier',
          label: 'data(label)',
          'font-size': '10px',
          color: '#374151'
        }
      },
      {
        selector: ':selected',
        style: {
          'background-color': '#f59e0b',
          'line-color': '#f59e0b',
          'target-arrow-color': '#f59e0b',
          'source-arrow-color': '#f59e0b'
        }
      }
    ],
    layout: theme.layout
  });
}

// Render fallback charts (Chart.js) when graph is not suitable or empty.
function renderChartFallback(payload) {
  const container = document.getElementById('graph');
  if (!container) return;

  // Clear any existing Cytoscape instance
  if (window.cy) {
    window.cy.destroy();
    window.cy = null;
  }

  // Remove any existing canvas
  container.innerHTML = '';

  // Create canvas for Chart.js
  const canvas = document.createElement('canvas');
  canvas.id = 'graphChart';
  container.appendChild(canvas);

  // Choose chart type and dataset based on page and payload
  const pathname = (window.location.pathname || '').split('/').pop() || '';
  const page = pathname.toLowerCase();

  let labels = [];
  let values = [];
  let chartType = 'bar';
  let bgColors = [];

  // Helper to generate colors
  const palette = (base, n) => {
    const cols = [];
    for (let i = 0; i < n; i++) cols.push(base);
    return cols;
  };

  if (payload && payload.summary && page.includes('dashboard')) {
    chartType = 'bar';
    labels = ['Wallets', 'Transactions', 'Suspicious'];
    values = [
      Number(payload.summary.wallets) || 0,
      Number(payload.summary.transactions) || 0,
      Number(payload.summary.suspicious) || 0,
    ];
    bgColors = ['#3b82f6', '#10b981', '#f97316'];

  } else if (payload && payload.risk && page.includes('risk')) {
    // Risk page: show doughnut of top flags or score buckets
    chartType = 'doughnut';
    if (Array.isArray(payload.risk.flags) && payload.risk.flags.length) {
      labels = payload.risk.flags.slice(0, 6);
      values = labels.map(() => 1);
    } else if (payload.risk.score !== undefined) {
      labels = ['Risk', 'Remaining'];
      const score = Number(payload.risk.score) || 0;
      values = [score, Math.max(0, 100 - score)];
    } else {
      labels = ['Unknown']; values = [1];
    }
    bgColors = ['#ef4444', '#f59e0b', '#f97316', '#fca5a5', '#fcd34d', '#fb923c'];

  } else if (payload && payload.timeline && Array.isArray(payload.timeline) && page.includes('cases')) {
    // Cases: timeline -> line chart
    chartType = 'line';
    labels = payload.timeline.map(t => t.time || t.date || '').slice(-20);
    values = payload.timeline.map(t => t.count || 1).slice(-20);
    bgColors = palette('#6366f1', values.length);

  } else if (payload && payload.summary) {
    // Generic summary fallback
    chartType = 'bar';
    labels = Object.keys(payload.summary).slice(0, 6);
    values = labels.map(k => Number(payload.summary[k]) || 0);
    bgColors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#f97316', '#ef4444'].slice(0, labels.length);

  } else if (payload && payload.risk && Array.isArray(payload.risk.flags)) {
    chartType = 'horizontalBar' in Chart ? 'bar' : 'bar';
    labels = payload.risk.flags.slice(0, 6);
    values = labels.map(() => 1);
    bgColors = ['#f97316', '#f59e0b', '#fca5a5', '#fb923c', '#fcd34d', '#ef4444'].slice(0, labels.length);

  } else {
    labels = ['No Data'];
    values = [0];
    bgColors = ['#94a3b8'];
  }

  // Clean up previous chart
  if (window.__graphChart) {
    try { window.__graphChart.destroy(); } catch (e) {}
    window.__graphChart = null;
  }

  if (typeof Chart === 'undefined') {
    console.warn('[Graph] Chart.js not loaded — cannot render fallback chart.');
    container.innerHTML = '<div style="padding:16px;color:#94a3b8;">No visual available</div>';
    return;
  }

  // Ensure canvas has a visible height
  canvas.style.width = '100%';
  canvas.style.height = '260px';

  const ctx = canvas.getContext('2d');
  window.__graphChart = new Chart(ctx, {
    type: chartType,
    data: {
      labels,
      datasets: [{
        label: 'Snapshot',
        data: values,
        backgroundColor: bgColors.length ? bgColors : '#3b82f6'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: chartType !== 'bar' } },
      scales: chartType === 'line' ? undefined : { y: { beginAtZero: true } }
    }
  });
}

// High-level helper: accept full payload and render graph or fallback chart
function renderVisual(payload) {
  if (!payload) {
    console.warn('[Graph] No payload provided to renderVisual');
    return;
  }

  const pageName = getCurrentPageName();
  const graph = payload.graph || null;
  const hasNodes = graph && ((Array.isArray(graph.nodes) && graph.nodes.length) || (Array.isArray(graph) && graph.length));

  if (hasNodes) {
    renderGraph(graph, { pageName });
  } else {
    renderChartFallback(payload);
  }
}
