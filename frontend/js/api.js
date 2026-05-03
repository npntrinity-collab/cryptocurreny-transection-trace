let API_BASE_URL =
  window.location.origin &&
  window.location.origin !== "null" &&
  window.location.protocol !== "file:"
    ? window.location.origin
    : "http://localhost:5000";

async function fetchTraceData(wallet) {
  const res = await fetch(
    `${API_BASE_URL}/api/trace?wallet=${encodeURIComponent(wallet)}`,
  );
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  }
  return await res.json();
}
