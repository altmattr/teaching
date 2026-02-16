let graphData = { nodes: [], edges: [] };

const svg = document.getElementById("graph");
const questionTitle = document.getElementById("question-node-title");
const questionText = document.getElementById("question-text");
const questionForm = document.getElementById("question-form");
const submitButton = document.getElementById("submit-answer");
const feedback = document.getElementById("feedback");

const nodeById = new Map();
const answers = new Map();
let selectedNodeId = null;

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Failed to load ${path}: ${response.status}`);
  }
  return response.json();
}

function buildGraphData(graph, questions) {
  if (!Array.isArray(graph.nodes) || !Array.isArray(graph.edges)) {
    throw new Error("graph.json must contain nodes[] and edges[]");
  }
  if (!questions || typeof questions.questions !== "object") {
    throw new Error("questions.json must contain a questions object keyed by node id");
  }

  const mergedNodes = graph.nodes.map((node) => {
    const q = questions.questions[node.id];
    if (!q) {
      throw new Error(`Missing question data for node ${node.id}`);
    }
    if (!Array.isArray(q.options) || typeof q.correct !== "number") {
      throw new Error(`Invalid question format for node ${node.id}`);
    }
    return {
      id: node.id,
      label: node.label || node.id,
      question: q.question,
      options: q.options,
      correct: q.correct,
    };
  });

  return { nodes: mergedNodes, edges: graph.edges };
}

function setGraphData(data) {
  graphData = data;
  nodeById.clear();
  graphData.nodes.forEach((node) => {
    nodeById.set(node.id, node);
  });
}

function renderSelectionState() {
  const groups = svg.querySelectorAll(".node");
  groups.forEach((group) => {
    const id = group.getAttribute("data-node-id");
    group.classList.toggle("active", id === selectedNodeId);
    group.classList.toggle("answered", answers.has(id));
  });
}

function selectNode(nodeId) {
  selectedNodeId = nodeId;
  renderSelectionState();
  renderQuestion();
}

function renderQuestion() {
  if (!selectedNodeId) {
    return;
  }

  const node = nodeById.get(selectedNodeId);
  if (!node) return;
  questionTitle.textContent = `Node ${node.label}`;
  questionText.textContent = node.question;
  feedback.textContent = "";
  feedback.className = "feedback";

  const previous = answers.get(node.id);
  questionForm.innerHTML = "";
  node.options.forEach((option, index) => {
    const id = `choice-${node.id}-${index}`;
    const label = document.createElement("label");
    label.className = "choice";
    label.setAttribute("for", id);

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "answer";
    radio.value = String(index);
    radio.id = id;
    if (previous && previous.selected === index) {
      radio.checked = true;
    }

    const text = document.createElement("span");
    text.textContent = option;

    label.appendChild(radio);
    label.appendChild(text);
    questionForm.appendChild(label);
  });

  submitButton.disabled = false;
}

function submitAnswer() {
  if (!selectedNodeId) return;

  const choice = questionForm.querySelector("input[name='answer']:checked");
  if (!choice) {
    feedback.textContent = "Please choose an option first.";
    feedback.className = "feedback bad";
    return;
  }

  const node = nodeById.get(selectedNodeId);
  if (!node) return;
  const selected = Number(choice.value);
  const isCorrect = selected === node.correct;
  answers.set(selectedNodeId, { selected, isCorrect });
  renderSelectionState();

  feedback.textContent = isCorrect ? "Correct answer." : "Not quite. Try again.";
  feedback.className = `feedback ${isCorrect ? "good" : "bad"}`;
}

function computeDepths(nodes, links) {
  const incomingCount = new Map(nodes.map((node) => [node.id, 0]));
  const outgoing = new Map(nodes.map((node) => [node.id, []]));

  links.forEach((link) => {
    incomingCount.set(link.target, (incomingCount.get(link.target) || 0) + 1);
    outgoing.get(link.source).push(link.target);
  });

  const queue = [];
  const depth = new Map(nodes.map((node) => [node.id, 0]));
  incomingCount.forEach((count, id) => {
    if (count === 0) queue.push(id);
  });

  while (queue.length > 0) {
    const id = queue.shift();
    const currentDepth = depth.get(id) || 0;
    const nextIds = outgoing.get(id) || [];
    nextIds.forEach((nextId) => {
      depth.set(nextId, Math.max(depth.get(nextId) || 0, currentDepth + 1));
      incomingCount.set(nextId, incomingCount.get(nextId) - 1);
      if (incomingCount.get(nextId) === 0) queue.push(nextId);
    });
  }

  return depth;
}

function drawGraphWithD3() {
  if (!window.d3) {
    questionText.textContent = "D3 failed to load, so the graph cannot be rendered.";
    return;
  }

  const width = 760;
  const height = 440;
  const nodeRadius = 25;
  const nodes = graphData.nodes.map((node) => ({ id: node.id, label: node.label }));
  const links = graphData.edges.map(([source, target]) => ({ source, target }));
  const depths = computeDepths(nodes, links);

  const d3svg = d3.select(svg);
  d3svg.selectAll("*").remove();

  d3svg
    .append("defs")
    .append("marker")
    .attr("id", "arrowhead")
    .attr("viewBox", "0 0 10 10")
    .attr("refX", 9)
    .attr("refY", 5)
    .attr("markerWidth", 7)
    .attr("markerHeight", 7)
    .attr("orient", "auto-start-reverse")
    .append("path")
    .attr("d", "M 0 0 L 10 5 L 0 10 z")
    .attr("fill", "#5b5b5b");

  const linkEls = d3svg
    .append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("class", "edge");

  const nodeEls = d3svg
    .append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .attr("class", "node")
    .attr("data-node-id", (d) => d.id)
    .attr("tabindex", 0)
    .attr("role", "button")
    .attr("aria-label", (d) => `Select node ${d.label}`)
    .on("click", (_, d) => selectNode(d.id))
    .on("keydown", (event, d) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectNode(d.id);
      }
    });

  nodeEls.append("circle").attr("r", nodeRadius);
  nodeEls
    .append("text")
    .attr("text-anchor", "middle")
    .attr("y", 5)
    .text((d) => d.label);

  const maxDepth = Math.max(...depths.values(), 1);
  const xScale = d3.scaleLinear().domain([0, maxDepth]).range([95, width - 95]);

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(130)
        .strength(0.5),
    )
    .force("charge", d3.forceManyBody().strength(-650))
    .force("collide", d3.forceCollide(nodeRadius + 12))
    .force(
      "x",
      d3
        .forceX((d) => xScale(depths.get(d.id) || 0))
        .strength(0.7),
    )
    .force("y", d3.forceY(height / 2).strength(0.06))
    .force("center", d3.forceCenter(width / 2, height / 2));

  simulation.on("tick", () => {
    nodes.forEach((node) => {
      node.x = Math.max(nodeRadius + 10, Math.min(width - nodeRadius - 10, node.x));
      node.y = Math.max(nodeRadius + 10, Math.min(height - nodeRadius - 10, node.y));
    });

    linkEls
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const len = Math.hypot(dx, dy) || 1;
        return d.target.x - (dx / len) * (nodeRadius + 2);
      })
      .attr("y2", (d) => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const len = Math.hypot(dx, dy) || 1;
        return d.target.y - (dy / len) * (nodeRadius + 2);
      });

    nodeEls.attr("transform", (d) => `translate(${d.x},${d.y})`);
  });

  renderSelectionState();
}

submitButton.addEventListener("click", submitAnswer);

async function init() {
  try {
    const [graph, questions] = await Promise.all([fetchJson("graph.json"), fetchJson("questions.json")]);
    setGraphData(buildGraphData(graph, questions));
    drawGraphWithD3();
  } catch (error) {
    questionTitle.textContent = "Data loading error";
    if (window.location.protocol === "file:") {
      questionText.textContent =
        "This page was opened from file:// and the browser blocks JSON fetches. Run ./serve-local.sh and open http://localhost:8000";
    } else {
      questionText.textContent = error.message;
    }
    submitButton.disabled = true;
  }
}

init();
