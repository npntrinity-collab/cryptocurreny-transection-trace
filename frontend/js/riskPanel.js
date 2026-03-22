function renderRisk(riskData) {
  document.getElementById("riskScore").innerText = riskData.score;

  const level = document.getElementById("riskLevel");
  level.innerText = riskData.level + " RISK";
  level.className = "risk-level " + riskData.level.toLowerCase();

  const list = document.getElementById("riskFlags");
  list.innerHTML = "";

  riskData.flags.forEach((flag) => {
    const li = document.createElement("li");
    li.innerText = flag;
    list.appendChild(li);
  });
}
