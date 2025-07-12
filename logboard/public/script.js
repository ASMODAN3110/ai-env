const socket = io();

socket.on("connect", () => {
    console.log("Connecté au serveur WebSocket");
});

socket.on("performance", (data) => {
    document.getElementById("cpu").textContent = data.cpu_percent.toFixed(1);
    document.getElementById("ram").textContent = data.ram_percent.toFixed(1);
    document.getElementById("gpu").textContent = data.gpu_percent ? data.gpu_percent.toFixed(1) : "N/A";
    document.getElementById("gpu-memory").textContent = data.gpu_memory_percent ? data.gpu_memory_percent.toFixed(1) : "N/A";
});

async function fetchLogs(level = "") {
    const response = await fetch(level ? `/logs?level=${level}` : "/logs");
    const logs = await response.json();
    const logList = document.getElementById("log-list");
    logList.innerHTML = "";
    logs.forEach(log => {
        const li = document.createElement("li");
        li.textContent = `[${log.timestamp}] ${log.level} | ${log.module} | ${log.message} | Contexte: ${JSON.stringify(log.context)}`;
        logList.appendChild(li);
    });
}

async function clearLogs() {
    await fetch("/logs/clear", { method: "POST" });
    fetchLogs();
}

document.getElementById("level-filter").addEventListener("change", (e) => {
    fetchLogs(e.target.value);
});

// Charger les journaux au démarrage
fetchLogs();