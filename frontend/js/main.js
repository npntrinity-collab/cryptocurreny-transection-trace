document.getElementById("traceBtn").addEventListener("click", async () => {
  const data = await fetchTraceData();

  // CASE INFO
  document.getElementById("caseId").innerText = data.case.id;
  document.getElementById("caseInput").innerText = data.case.input;
  document.getElementById("caseStatus").innerText = data.case.status;

  // SUMMARY
  document.getElementById("totalVolume").innerText = data.summary.totalVolume;
  document.getElementById("walletCount").innerText = data.summary.wallets;
  document.getElementById("txCount").innerText = data.summary.transactions;
  document.getElementById("suspiciousCount").innerText =
    data.summary.suspicious;

  // MAIN DATA
  renderGraph(data.graph);
  renderRisk(data.risk);
  renderTimeline(data.timeline);
});
