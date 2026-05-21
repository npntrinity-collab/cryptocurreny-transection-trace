function renderTimeline(data) {
  const container = document.getElementById("timeline");
  if (!container) {
    console.warn('[Timeline] container not found');
    return;
  }
  container.innerHTML = "";

  if (!Array.isArray(data) || data.length === 0) {
    container.innerHTML = '<div class="timeline-event"><h3>No timeline data available</h3></div>';
    return;
  }

  data.forEach((item) => {
    const div = document.createElement("div");
    div.className = "timeline-card";
    div.innerHTML = `<b>${item.time}</b><br>${item.text}`;
    container.appendChild(div);
  });
}
