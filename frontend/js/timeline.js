function renderTimeline(data) {
  const container = document.getElementById("timeline");
  container.innerHTML = "";

  data.forEach((item) => {
    const div = document.createElement("div");
    div.className = "timeline-card";
    div.innerHTML = `<b>${item.time}</b><br>${item.text}`;
    container.appendChild(div);
  });
}
