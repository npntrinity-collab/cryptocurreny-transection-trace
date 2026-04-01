async function fetchTraceData(wallet) {
  const res = await fetch(`http://127.0.0.1:5000/api/trace?wallet=${wallet}`);
  return await res.json();
}
