const conversions = window.CONVERSIONS || [];

const conversionSelect = document.querySelector("#conversionSelect");
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

let historyItems = loadHistory();

function currentConversion() {
  return conversions.find((conversion) => conversion.key === conversionSelect.value) || conversions[0];
}

function setStatus(message, type = "success") {
  statusText.textContent = message;
  statusText.classList.toggle("is-error", type === "error");
  statusText.classList.toggle("is-success", type !== "error");
}

function renderConversions() {
  conversionSelect.innerHTML = "";
  for (const conversion of conversions) {
    const option = document.createElement("option");
    option.value = conversion.key;
    option.textContent = conversion.label;
    conversionSelect.append(option);
  }
}

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
      conversionSelect.value = item.choice;
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

conversionSelect.addEventListener("change", updateHint);
convertButton.addEventListener("click", convert);
exampleButton.addEventListener("click", loadExample);
clearButton.addEventListener("click", clearCurrent);
copyButton.addEventListener("click", copyOutput);
clearHistoryButton.addEventListener("click", clearHistory);
themeToggle.addEventListener("click", toggleTheme);

document.addEventListener("keydown", (event) => {
  if (event.ctrlKey && event.key === "Enter") {
    convert();
  }
  if (event.key === "Escape") {
    clearCurrent();
  }
});

applyTheme(localStorage.getItem(themeKey) || "light");
renderConversions();
updateHint();
loadExample();
renderHistory();
