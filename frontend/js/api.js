// Ensure a single global API base URL without redeclaring identifiers
if (typeof window.API_BASE_URL === 'undefined') {
  window.API_BASE_URL =
    (window.location.origin && window.location.origin !== 'null' && window.location.protocol !== 'file:')
      ? window.location.origin
      : 'http://localhost:5000';
}

async function fetchTraceData(wallet) {
  const query = wallet ? `?wallet=${encodeURIComponent(wallet)}` : '';
  const res = await fetch(`${window.API_BASE_URL}/api/trace${query}`);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  }
  return await res.json();
}

// expose helper on window for pages that expect it
window.fetchTraceData = fetchTraceData;
