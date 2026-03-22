function renderGraph(graphData) {
  document.getElementById("graph").innerHTML = "";

  cytoscape({
    container: document.getElementById("graph"),

    elements: [...graphData.nodes, ...graphData.edges],

    style: [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "background-color": "#3b82f6",
          color: "#fff",
          "text-valign": "center",
        },
      },
      {
        selector: 'node[type="exchange"]',
        style: { "background-color": "#22c55e" },
      },
      {
        selector: 'node[type="darknet"]',
        style: { "background-color": "#ef4444" },
      },
      {
        selector: 'node[type="mixer"]',
        style: { "background-color": "#f59e0b" },
      },
      {
        selector: "edge",
        style: {
          label: "data(label)",
          "line-color": "#64748b",
          "target-arrow-shape": "triangle",
          "target-arrow-color": "#64748b",
        },
      },
    ],

    layout: { name: "cose", animate: true },
  });
}
