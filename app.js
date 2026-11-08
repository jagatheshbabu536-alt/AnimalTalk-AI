const audioInput = document.getElementById("audioFile");
const dropzone = document.getElementById("dropzone");
const fileRow = document.getElementById("fileRow");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const resultContent = document.getElementById("resultContent");
const resultText = document.getElementById("resultText");
const errorBox = document.getElementById("errorBox");
const stateLabel = document.getElementById("stateLabel");
const cautionText = document.getElementById("cautionText");

let selectedFile = null;
let latestTamilText = "";

document.querySelectorAll(".animal-option").forEach(option => {
  option.addEventListener("click", () => {
    document.querySelectorAll(".animal-option").forEach(x => x.classList.remove("selected"));
    option.classList.add("selected");
    option.querySelector("input").checked = true;
  });
});

function setFile(file) {
  if (!file) return;
  selectedFile = file;
  fileName.textContent = `${file.name} · ${(file.size / (1024 * 1024)).toFixed(2)} MB`;
  fileRow.hidden = false;
  errorBox.hidden = true;
}
audioInput.addEventListener("change", e => setFile(e.target.files[0]));
document.getElementById("removeFile").addEventListener("click", () => {
  selectedFile = null; audioInput.value = ""; fileRow.hidden = true;
});
["dragenter", "dragover"].forEach(name => dropzone.addEventListener(name, e => {
  e.preventDefault(); dropzone.classList.add("dragover");
}));
["dragleave", "drop"].forEach(name => dropzone.addEventListener(name, e => {
  e.preventDefault(); dropzone.classList.remove("dragover");
}));
dropzone.addEventListener("drop", e => setFile(e.dataTransfer.files[0]));

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    errorBox.textContent = "முதலில் ஒரு audio file upload செய்யவும்.";
    errorBox.hidden = false; return;
  }
  const animal = document.querySelector('input[name="animal"]:checked').value;
  const form = new FormData();
  form.append("animal", animal);
  form.append("audio", selectedFile);

  errorBox.hidden = true; resultContent.hidden = true;
  emptyState.hidden = true; loadingState.hidden = false;
  stateLabel.textContent = "ANALYZING";
  analyzeBtn.disabled = true;
  try {
    const response = await fetch("/analyze", { method: "POST", body: form });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed");
    latestTamilText = data.result;
    resultText.textContent = data.result;
    cautionText.textContent = data.note || "";
    resultContent.hidden = false;
    stateLabel.textContent = "COMPLETED";
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.hidden = false;
    emptyState.hidden = false;
    stateLabel.textContent = "ERROR";
  } finally {
    loadingState.hidden = true;
    analyzeBtn.disabled = false;
  }
});

document.getElementById("speakBtn").addEventListener("click", () => {
  if (!latestTamilText) return;
  if (!("speechSynthesis" in window)) {
    alert("இந்த browser-ல் Text-to-Speech support இல்லை.");
    return;
  }
  speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(latestTamilText);
  utterance.lang = "ta-IN";
  utterance.rate = 0.88;
  utterance.pitch = 1;
  const voices = speechSynthesis.getVoices();
  const tamilVoice = voices.find(v => v.lang.toLowerCase().startsWith("ta"));
  if (tamilVoice) utterance.voice = tamilVoice;
  speechSynthesis.speak(utterance);
});
document.getElementById("stopBtn").addEventListener("click", () => {
  if ("speechSynthesis" in window) speechSynthesis.cancel();
});
document.getElementById("copyBtn").addEventListener("click", async () => {
  if (!latestTamilText) return;
  await navigator.clipboard.writeText(latestTamilText);
  document.getElementById("copyBtn").textContent = "✓ Copied";
  setTimeout(() => document.getElementById("copyBtn").textContent = "⧉ Copy", 1400);
});
