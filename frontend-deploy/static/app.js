const conversions = window.CONVERSIONS || [];

const comboInput = document.querySelector("#conversionSearch");
const comboList = document.querySelector("#conversionListbox");
const comboBox = document.querySelector("#conversionCombobox");
const sortToggle = document.querySelector("#sortToggle");
const hintText = document.querySelector("#hintText");
const inputValue = document.querySelector("#inputValue");
const outputValue = document.querySelector("#outputValue");
const statusText = document.querySelector("#statusText");
const historyList = document.querySelector("#historyList");
const convertButton = document.querySelector("#convertButton");
const exampleButton = document.querySelector("#exampleButton");
const clearButton = document.querySelector("#clearButton");
const copyButton = document.querySelector("#copyButton");
const clearHistoryButton = document.querySelector("#clearHistoryButton");
const themeToggle = document.querySelector("#themeToggle");

const historyKey = "encoding-explorer-history";
const themeKey = "encoding-explorer-theme";
const sortKey = "encoding-explorer-sort";

let historyItems = loadHistory();
let selectedConversion = conversions[0];
let sortDirection = localStorage.getItem(sortKey) === "desc" ? "desc" : "asc";
let filterText = "";
let activeIndex = -1;

function currentConversion() {
  return selectedConversion || conversions[0];
}

function setStatus(message, type = "success") {
  statusText.textContent = message;
  statusText.classList.toggle("is-error", type === "error");
  statusText.classList.toggle("is-success", type !== "error");
}

// --- Searchable / sortable conversion picker --------------------------------

function getVisibleConversions() {
  let list = [...conversions].sort((a, b) => a.label.localeCompare(b.label));
  if (sortDirection === "desc") list.reverse();

  const query = filterText.trim().toLowerCase();
  if (query) {
    list = list.filter(
      (conversion) =>
        conversion.label.toLowerCase().includes(query) || conversion.key === query
    );
  }
  return list;
}

function renderComboList() {
  const list = getVisibleConversions();
  comboList.innerHTML = "";

  if (list.length === 0) {
    const empty = document.createElement("li");
    empty.className = "combobox-empty";
    empty.textContent = "No matching conversions.";
    comboList.append(empty);
    activeIndex = -1;
    return;
  }

  if (activeIndex >= list.length) activeIndex = list.length - 1;

  list.forEach((conversion, index) => {
    const option = document.createElement("li");
    option.className = "combobox-option";
    option.setAttribute("role", "option");
    option.id = `combo-option-${conversion.key}`;
    option.dataset.key = conversion.key;
    if (index === activeIndex) option.classList.add("is-active");
    if (selectedConversion && conversion.key === selectedConversion.key) {
      option.classList.add("is-selected");
      option.setAttribute("aria-selected", "true");
    }
    option.innerHTML = `<span class="option-key">#${conversion.key}</span><span class="option-label">${escapeHtml(conversion.label)}</span>`;
    option.addEventListener("mousedown", (event) => {
      event.preventDefault();
      selectConversion(conversion);
    });
    comboList.append(option);
  });
}

function openList() {
  comboList.hidden = false;
  comboInput.setAttribute("aria-expanded", "true");
  renderComboList();
}

function closeList() {
  comboList.hidden = true;
  comboInput.setAttribute("aria-expanded", "false");
  activeIndex = -1;
}

function selectConversion(conversion) {
  selectedConversion = conversion;
  comboInput.value = conversion.label;
  filterText = "";
  closeList();
  updateHint();
}

function applySortDirection(direction) {
  sortDirection = direction;
  localStorage.setItem(sortKey, direction);
  sortToggle.setAttribute("aria-label", direction === "asc" ? "Sorted A to Z. Click for Z to A." : "Sorted Z to A. Click for A to Z.");
  sortToggle.title = sortToggle.getAttribute("aria-label");
  sortToggle.querySelector("span").textContent = direction === "asc" ? "A→Z" : "Z→A";
  if (!comboList.hidden) renderComboList();
}

comboInput.addEventListener("focus", () => {
  filterText = "";
  activeIndex = -1;
  openList();
  comboInput.select();
});

comboInput.addEventListener("input", () => {
  filterText = comboInput.value;
  activeIndex = 0;
  openList();
});

comboInput.addEventListener("keydown", (event) => {
  if (event.key === "ArrowDown") {
    event.preventDefault();
    if (comboList.hidden) {
      openList();
      return;
    }
    const list = getVisibleConversions();
    activeIndex = Math.min(activeIndex + 1, list.length - 1);
    renderComboList();
    return;
  }

  if (event.key === "ArrowUp") {
    event.preventDefault();
    const list = getVisibleConversions();
    activeIndex = Math.max(activeIndex - 1, 0);
    renderComboList();
    return;
  }

  if (event.key === "Enter") {
    event.preventDefault();
    event.stopPropagation();
    const list = getVisibleConversions();
    if (list[activeIndex]) {
      selectConversion(list[activeIndex]);
    } else if (list.length === 1) {
      selectConversion(list[0]);
    }
    return;
  }

  if (event.key === "Escape") {
    event.preventDefault();
    event.stopPropagation();
    filterText = "";
    comboInput.value = currentConversion().label;
    closeList();
  }
});

sortToggle.addEventListener("click", () => {
  applySortDirection(sortDirection === "asc" ? "desc" : "asc");
});

document.addEventListener("click", (event) => {
  if (!comboBox.contains(event.target)) {
    closeList();
    comboInput.value = currentConversion().label;
  }
});

// --- Core conversion logic ----------------------------------------------------

function updateHint() {
  const conversion = currentConversion();
  hintText.textContent = conversion.hint;
  outputValue.value = "";
  setStatus("Ready.");
}

function loadExample() {
  const conversion = currentConversion();
  inputValue.value = conversion.example;
  outputValue.value = "";
  setStatus("Example loaded.");
  inputValue.focus();
}

async function convert() {
  const conversion = currentConversion();
  const value = inputValue.value.trim();

  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ choice: conversion.key, value }),
    });
    const payload = await response.json();

    if (!response.ok || !payload.ok) {
      throw new Error(payload.error || "Conversion failed.");
    }

    outputValue.value = payload.result;
    setStatus(`${payload.conversion.outputLabel} ready.`);
    addHistory({
      label: payload.conversion.label,
      choice: payload.conversion.key,
      input: value,
      output: payload.result,
    });
  } catch (error) {
    outputValue.value = "";
    setStatus(`Error: ${error.message}`, "error");
  }
}

function clearCurrent() {
  inputValue.value = "";
  outputValue.value = "";
  updateHint();
  inputValue.focus();
}

async function copyOutput() {
  if (!outputValue.value.trim()) {
    setStatus("Nothing to copy yet.", "error");
    return;
  }

  await navigator.clipboard.writeText(outputValue.value);
  setStatus("Output copied.");
}

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(historyKey)) || [];
  } catch {
    return [];
  }
}

function saveHistory() {
  localStorage.setItem(historyKey, JSON.stringify(historyItems.slice(0, 30)));
}

function addHistory(item) {
  historyItems = [item, ...historyItems].slice(0, 30);
  saveHistory();
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = "";

  if (historyItems.length === 0) {
    const empty = document.createElement("div");
    empty.className = "history-empty";
    empty.textContent = "No conversions yet.";
    historyList.append(empty);
    return;
  }

  for (const item of historyItems) {
    const button = document.createElement("button");
    button.className = "history-item";
    button.type = "button";
    button.innerHTML = `<strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.input)} -> ${escapeHtml(item.output)}</span>`;
    button.addEventListener("click", () => {
      const conversion = conversions.find((c) => c.key === item.choice);
      if (conversion) {
        selectedConversion = conversion;
        comboInput.value = conversion.label;
      }
      inputValue.value = item.input;
      outputValue.value = item.output;
      updateHint();
      setStatus("History item loaded.");
    });
    historyList.append(button);
  }
}

function clearHistory() {
  historyItems = [];
  saveHistory();
  renderHistory();
  setStatus("History cleared.");
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem(themeKey, theme);
}

function toggleTheme() {
  const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(nextTheme);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

convertButton.addEventListener("click", convert);
exampleButton.addEventListener("click", loadExample);
clearButton.addEventListener("click", clearCurrent);
copyButton.addEventListener("click", copyOutput);
clearHistoryButton.addEventListener("click", clearHistory);
themeToggle.addEventListener("click", toggleTheme);

// Enter converts (Shift+Enter still inserts a newline, same convention as
// chat apps). Scoped to the input textarea only.
inputValue.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    convert();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.ctrlKey && event.key === "Enter") {
    convert();
  }
  if (event.key === "Escape" && document.activeElement !== comboInput) {
    clearCurrent();
  }
});

applyTheme(localStorage.getItem(themeKey) || "light");
applySortDirection(sortDirection);
comboInput.value = selectedConversion.label;
closeList();
updateHint();
loadExample();
renderHistory();