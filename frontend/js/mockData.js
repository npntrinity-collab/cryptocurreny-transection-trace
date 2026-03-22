const mockData = {
  risk: {
    score: 89,
    level: "HIGH",
    flags: [
      "Darknet Market Transfer",
      "Large Transaction",
      "Mixer Usage Detected",
    ],
  },

  graph: {
    nodes: [
      { data: { id: "A", label: "Wallet A" } },
      { data: { id: "B", label: "Wallet B" } },
      { data: { id: "MX", label: "Mixer", type: "mixer" } },
      { data: { id: "DN", label: "Darknet", type: "darknet" } },
      { data: { id: "EX", label: "Exchange", type: "exchange" } },
    ],

    edges: [
      { data: { source: "A", target: "B", label: "5 BTC" } },
      { data: { source: "B", target: "MX", label: "10 BTC" } },
      { data: { source: "MX", target: "DN", label: "8 BTC" } },
      { data: { source: "DN", target: "EX", label: "7 BTC" } },
    ],
  },

  timeline: [
    { time: "10:25 AM", text: "Wallet A → Wallet B" },
    { time: "11:10 AM", text: "Wallet B → Mixer" },
    { time: "12:30 PM", text: "Mixer → Darknet" },
    { time: "01:15 PM", text: "Darknet → Exchange" },
  ],
};
