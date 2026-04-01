function renderGraph(graphData) {
  const cy = cytoscape({
    container: document.getElementById("graph"),

    elements: graphData,

    style: [
      {
        selector: "node",
        style: {
          "background-color": "blue",
          label: "data(label)",
          color: "white",
          "font-size": "12px",
          "text-valign": "center",
          "text-halign": "center",
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": "#888",
          "target-arrow-shape": "triangle",
          "target-arrow-color": "#888",
          "curve-style": "bezier",
          label: "data(label)",
          "font-size": "10px",
          color: "#ccc",
        },
      },
    ],

    layout: {
      name: "cose",
      animate: true,
      fit: true,
      padding: 30,
    },
  });
}
