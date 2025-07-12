/**
 * Professional System Monitor Dashboard JavaScript
 *
 * This script handles real-time system monitoring, WebSocket connections,
 * chart rendering, theme switching, and log management for the dashboard.
 *
 * Features:
 * - Real-time performance monitoring with Chart.js
 * - WebSocket connection management
 * - Light/Dark theme switching
 * - Advanced log filtering and display
 * - Responsive chart updates
 * - Professional UI interactions
 *
 * @author System Monitor Dashboard
 * @version 1.1.0
 * @license MIT
 */

// ===== GLOBAL VARIABLES AND CONFIGURATION =====
let socket;
const charts = {};
const performanceData = {
  cpu: [],
  ram: [],
  gpu: [],
  gpuMemory: [],
  timestamps: [],
};
let currentTheme = localStorage.getItem("theme") || "light";
let logsData = [];
let filteredLogs = [];
let currentLogLevel = "";

// Chart configuration constants
const CHART_CONFIG = {
  maxDataPoints: 20,
  updateInterval: 1000,
  colors: {
    light: {
      primary: "#8b5cf6",
      secondary: "#a78bfa",
      success: "#10b981",
      warning: "#f59e0b",
      error: "#ef4444",
      info: "#3b82f6",
    },
    dark: {
      primary: "#fb923c",
      secondary: "#fdba74",
      success: "#34d399",
      warning: "#fbbf24",
      error: "#f87171",
      info: "#60a5fa",
    },
  },
};

// ===== INITIALIZATION =====
/**
 * Initialize the dashboard when DOM is loaded
 */
document.addEventListener("DOMContentLoaded", () => {
  initializeTheme();
  initializeWebSocket();
  initializeCharts();
  initializeEventListeners();
  loadInitialLogs();
  showLoadingOverlay(false);
});

// ===== THEME MANAGEMENT =====
/**
 * Initialize theme based on user preference or system preference
 */
function initializeTheme() {
  // Check for saved theme preference or default to system preference
  if (!currentTheme) {
    currentTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  applyTheme(currentTheme);
  updateThemeToggleIcon();
}

/**
 * Apply the specified theme to the document
 * @param {string} theme - Theme name ('light' or 'dark')
 */
function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
  currentTheme = theme;

  // Update charts with new theme colors
  if (Object.keys(charts).length > 0) {
    updateChartsTheme();
  }
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
  const newTheme = currentTheme === "light" ? "dark" : "light";
  applyTheme(newTheme);
  updateThemeToggleIcon();
}

/**
 * Update the theme toggle button icon
 */
function updateThemeToggleIcon() {
  const themeToggle = document.getElementById("theme-toggle");
  const icon = themeToggle.querySelector("i");

  if (currentTheme === "dark") {
    icon.className = "fas fa-sun";
    themeToggle.setAttribute("aria-label", "Passer au thème clair");
  } else {
    icon.className = "fas fa-moon";
    themeToggle.setAttribute("aria-label", "Passer au thème sombre");
  }
}

// ===== WEBSOCKET CONNECTION MANAGEMENT =====
/**
 * Initialize WebSocket connection with error handling and reconnection logic
 */
function initializeWebSocket() {
  try {
    // Use the global io function from Socket.IO CDN
    socket = io();

    socket.on("connect", handleSocketConnect);
    socket.on("disconnect", handleSocketDisconnect);
    socket.on("performance", handlePerformanceData);
    socket.on("connect_error", handleSocketError);
  } catch (error) {
    console.error("Failed to initialize WebSocket:", error);
    updateConnectionStatus(false);
  }
}

/**
 * Handle successful WebSocket connection
 */
function handleSocketConnect() {
  console.log("Connected to WebSocket server");
  updateConnectionStatus(true);
  showRefreshIndicator();
}

/**
 * Handle WebSocket disconnection
 */
function handleSocketDisconnect() {
  console.log("Disconnected from WebSocket server");
  updateConnectionStatus(false);
}

/**
 * Handle WebSocket connection errors
 * @param {Error} error - Connection error object
 */
function handleSocketError(error) {
  console.error("WebSocket connection error:", error);
  updateConnectionStatus(false);
}

/**
 * Update connection status indicator in the UI
 * @param {boolean} isConnected - Connection status
 */
function updateConnectionStatus(isConnected) {
  const statusElement = document.getElementById("connection-status");
  const statusText = statusElement.querySelector("span");

  if (isConnected) {
    statusElement.className = "connection-status connected";
    statusText.textContent = "Connecté";
  } else {
    statusElement.className = "connection-status disconnected";
    statusText.textContent = "Déconnecté";
  }
}

// ===== PERFORMANCE DATA HANDLING =====
/**
 * Handle incoming performance data from WebSocket
 * @param {Object} data - Performance data object
 */
function handlePerformanceData(data) {
  try {
    // Update performance data arrays
    updatePerformanceArrays(data);

    // Update metric cards
    updateMetricCards(data);

    // Update charts
    updatePerformanceCharts();

    // Show refresh indicator
    showRefreshIndicator();
  } catch (error) {
    console.error("Error handling performance data:", error);
  }
}

/**
 * Update performance data arrays with new data point
 * @param {Object} data - Performance data object
 */
function updatePerformanceArrays(data) {
  const timestamp = new Date().toLocaleTimeString();

  // Add new data points
  performanceData.cpu.push(data.cpu_percent || 0);
  performanceData.ram.push(data.ram_percent || 0);
  performanceData.gpu.push(data.gpu_percent || 0);
  performanceData.gpuMemory.push(data.gpu_memory_percent || 0);
  performanceData.timestamps.push(timestamp);

  // Maintain maximum data points
  if (performanceData.cpu.length > CHART_CONFIG.maxDataPoints) {
    performanceData.cpu.shift();
    performanceData.ram.shift();
    performanceData.gpu.shift();
    performanceData.gpuMemory.shift();
    performanceData.timestamps.shift();
  }
}

/**
 * Update metric cards with current values
 * @param {Object} data - Performance data object
 */
function updateMetricCards(data) {
  // Update CPU
  updateMetricCard("cpu", data.cpu_percent);

  // Update RAM
  updateMetricCard("ram", data.ram_percent);

  // Update GPU
  updateMetricCard("gpu", data.gpu_percent);

  // Update GPU Memory
  updateMetricCard("gpu-memory", data.gpu_memory_percent);
}

/**
 * Update individual metric card
 * @param {string} metric - Metric name
 * @param {number} value - Metric value
 */
function updateMetricCard(metric, value) {
  const valueElement = document.getElementById(metric + "-value");
  const statusElement = document.getElementById(metric + "-status");

  if (value !== null && value !== undefined) {
    valueElement.textContent = value.toFixed(1) + "%";

    // Update status based on value
    let status = "normal";
    let statusText = "Normal";

    if (value > 80) {
      status = "critical";
      statusText = "Critique";
    } else if (value > 60) {
      status = "warning";
      statusText = "Attention";
    }

    statusElement.className = "metric-status " + status;
    statusElement.textContent = statusText;
  } else {
    valueElement.textContent = "N/A";
    statusElement.className = "metric-status";
    statusElement.textContent = "N/A";
  }
}

/**
 * Show refresh indicator animation
 */
function showRefreshIndicator() {
  const indicator = document.getElementById("refresh-indicator");
  indicator.classList.add("spinning");

  setTimeout(() => {
    indicator.classList.remove("spinning");
  }, 1000);
}

// ===== CHART MANAGEMENT =====
/**
 * Initialize all charts
 */
function initializeCharts() {
  initializeMetricCharts();
  initializeOverviewChart();
}

/**
 * Initialize individual metric charts
 */
function initializeMetricCharts() {
  const metrics = ["cpu", "ram", "gpu", "gpu-memory"];
  const colors = CHART_CONFIG.colors[currentTheme];

  metrics.forEach((metric) => {
    const canvas = document.getElementById(metric + "-chart");
    if (canvas) {
      charts[metric] = createMiniChart(canvas, colors.primary);
    }
  });
}

/**
 * Initialize overview chart
 */
function initializeOverviewChart() {
  const canvas = document.getElementById("overview-chart");
  if (canvas) {
    charts.overview = createOverviewChart(canvas);
  }
}

/**
 * Create a mini chart for metric cards
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @param {string} color - Chart color
 * @returns {Chart} Chart.js instance
 */
function createMiniChart(canvas, color) {
  return new Chart(canvas, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          data: [],
          borderColor: color,
          backgroundColor: `${color}20`,
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: { display: false },
        y: {
          display: false,
          min: 0,
          max: 100,
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
      animation: {
        duration: 0 // Disable animations for better performance
      }
    },
  });
}

/**
 * Create overview chart showing all metrics
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @returns {Chart} Chart.js instance
 */
function createOverviewChart(canvas) {
  const colors = CHART_CONFIG.colors[currentTheme];

  return new Chart(canvas, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "CPU (%)",
          data: [],
          borderColor: colors.primary,
          backgroundColor: `${colors.primary}20`,
          borderWidth: 2,
          fill: false,
          tension: 0.4,
        },
        {
          label: "RAM (%)",
          data: [],
          borderColor: colors.success,
          backgroundColor: `${colors.success}20`,
          borderWidth: 2,
          fill: false,
          tension: 0.4,
        },
        {
          label: "GPU (%)",
          data: [],
          borderColor: colors.warning,
          backgroundColor: `${colors.warning}20`,
          borderWidth: 2,
          fill: false,
          tension: 0.4,
        },
        {
          label: "GPU Memory (%)",
          data: [],
          borderColor: colors.error,
          backgroundColor: `${colors.error}20`,
          borderWidth: 2,
          fill: false,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: {
            usePointStyle: true,
            padding: 20,
          },
        },
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: "Temps",
          },
          ticks: {
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 10
          }
        },
        y: {
          display: true,
          min: 0,
          max: 100,
          title: {
            display: true,
            text: "Utilisation (%)",
          },
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
      animation: {
        duration: 0 // Disable animations for better performance
      }
    },
  });
}

/**
 * Update all performance charts with latest data
 */
function updatePerformanceCharts() {
  // Update mini charts
  updateMiniChart("cpu", performanceData.cpu);
  updateMiniChart("ram", performanceData.ram);
  updateMiniChart("gpu", performanceData.gpu);
  updateMiniChart("gpu-memory", performanceData.gpuMemory);

  // Update overview chart
  updateOverviewChart();
}

/**
 * Update individual mini chart
 * @param {string} metric - Metric name
 * @param {Array} data - Data array
 */
function updateMiniChart(metric, data) {
  const chart = charts[metric];
  if (chart) {
    chart.data.labels = performanceData.timestamps;
    chart.data.datasets[0].data = data;
    chart.update('none'); // Update without animation
  }
}

/**
 * Update overview chart with all metrics
 */
function updateOverviewChart() {
  const chart = charts.overview;
  if (chart) {
    chart.data.labels = performanceData.timestamps;
    chart.data.datasets[0].data = performanceData.cpu;
    chart.data.datasets[1].data = performanceData.ram;
    chart.data.datasets[2].data = performanceData.gpu;
    chart.data.datasets[3].data = performanceData.gpuMemory;
    chart.update('none'); // Update without animation
  }
}

/**
 * Update charts theme colors
 */
function updateChartsTheme() {
  const colors = CHART_CONFIG.colors[currentTheme];

  // Update mini charts
  Object.keys(charts).forEach((key) => {
    if (key !== "overview") {
      const chart = charts[key];
      if (chart) {
        chart.data.datasets[0].borderColor = colors.primary;
        chart.data.datasets[0].backgroundColor = `${colors.primary}20`;
        chart.update('none');
      }
    }
  });

  // Update overview chart
  if (charts.overview) {
    const datasets = charts.overview.data.datasets;
    datasets[0].borderColor = colors.primary;
    datasets[1].borderColor = colors.success;
    datasets[2].borderColor = colors.warning;
    datasets[3].borderColor = colors.error;
    charts.overview.update('none');
  }
}

// ===== LOG MANAGEMENT =====
/**
 * Load initial logs from server
 */
function loadInitialLogs() {
  showLoadingOverlay(true);
  fetchLogs()
    .then(() => {
      showLoadingOverlay(false);
    })
    .catch((error) => {
      console.error("Error loading initial logs:", error);
      showLoadingOverlay(false);
    });
}

/**
 * Fetch logs from server with optional level filter
 * @param {string} level - Log level filter
 */
function fetchLogs(level) {
  level = level || "";

  const url = level ? "/logs?level=" + level : "/logs";

  return fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error("HTTP error! status: " + response.status);
      }
      return response.json();
    })
    .then((data) => {
      logsData = data;
      currentLogLevel = level;
      filterAndDisplayLogs();
      updateLogsStatistics();
    })
    .catch((error) => {
      console.error("Error fetching logs:", error);
      displayErrorMessage("Erreur lors du chargement des journaux");
    });
}

/**
 * Filter and display logs based on current filter
 */
function filterAndDisplayLogs() {
  filteredLogs = currentLogLevel ? logsData.filter((log) => log.level === currentLogLevel) : logsData;

  displayLogs(filteredLogs);
}

/**
 * Display logs in the UI
 * @param {Array} logs - Array of log objects
 */
function displayLogs(logs) {
  const logsList = document.getElementById("logs-list");

  if (logs.length === 0) {
    logsList.innerHTML =
      '<div class="no-logs">' + '<i class="fas fa-inbox"></i>' + "<p>Aucun journal disponible</p>" + "</div>";
    return;
  }

  logsList.innerHTML = logs
    .map(
      (log) =>
        '<div class="log-entry">' +
        '<div class="log-timestamp">' +
        formatTimestamp(log.timestamp) +
        "</div>" +
        '<div class="log-level ' +
        log.level +
        '">' +
        log.level +
        "</div>" +
        '<div class="log-module">' +
        (log.module || "System") +
        "</div>" +
        '<div class="log-message">' +
        escapeHtml(log.message) +
        "</div>" +
        '<div class="log-context">' +
        escapeHtml(formatContext(log.context)) +
        "</div>" +
        "</div>"
    )
    .join("");
}

/**
 * Update logs statistics
 */
function updateLogsStatistics() {
  const totalLogs = logsData.length;
  const errorLogs = logsData.filter((log) => log.level === "ERROR" || log.level === "CRITICAL").length;
  const warningLogs = logsData.filter((log) => log.level === "WARNING").length;

  document.getElementById("total-logs").textContent = totalLogs;
  document.getElementById("error-logs").textContent = errorLogs;
  document.getElementById("warning-logs").textContent = warningLogs;
}

/**
 * Clear all logs
 */
function clearLogs() {
  showLoadingOverlay(true);

  fetch("/logs/clear", { method: "POST" })
    .then((response) => {
      if (!response.ok) {
        throw new Error("HTTP error! status: " + response.status);
      }
      return fetchLogs(currentLogLevel);
    })
    .then(() => {
      showLoadingOverlay(false);
    })
    .catch((error) => {
      console.error("Error clearing logs:", error);
      displayErrorMessage("Erreur lors de la suppression des journaux");
      showLoadingOverlay(false);
    });
}

// ===== UTILITY FUNCTIONS =====
/**
 * Format timestamp for display
 * @param {string} timestamp - ISO timestamp string
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp) {
  try {
    return new Date(timestamp).toLocaleString("fr-FR");
  } catch (error) {
    return timestamp;
  }
}

/**
 * Format context object for display
 * @param {Object} context - Context object
 * @returns {string} Formatted context string
 */
function formatContext(context) {
  if (!context) return "";

  try {
    return typeof context === "string" ? context : JSON.stringify(context, null, 2);
  } catch (error) {
    return String(context);
  }
}

/**
 * Escape HTML characters to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Show or hide loading overlay
 * @param {boolean} show - Whether to show the overlay
 */
function showLoadingOverlay(show) {
  const overlay = document.getElementById("loading-overlay");
  if (show) {
    overlay.classList.add("show");
  } else {
    overlay.classList.remove("show");
  }
}

/**
 * Display error message to user
 * @param {string} message - Error message
 */
function displayErrorMessage(message) {
  const errorContainer = document.getElementById("error-container");
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.style.display = "block";

    setTimeout(() => {
      errorContainer.style.display = "none";
    }, 5000);
  }
}

// ===== EVENT LISTENERS =====
/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
  // Theme toggle
  document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

  // Log level filter
  document.getElementById("level-filter").addEventListener("change", (e) => {
    fetchLogs(e.target.value);
  });

  // Clear logs button
  document.getElementById("clear-logs-btn").addEventListener("click", clearLogs);

  // Refresh logs button
  document.getElementById("refresh-logs-btn").addEventListener("click", () => {
    fetchLogs(currentLogLevel);
  });

  // Chart timeframe controls
  const chartControlBtns = document.querySelectorAll(".chart-control-btn");
  chartControlBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      // Remove active class from all buttons
      chartControlBtns.forEach((b) => {
        b.classList.remove("active");
      });
      // Add active class to clicked button
      e.target.classList.add("active");

      // Here you could implement different timeframe logic
      const timeframe = e.target.dataset.timeframe;
      console.log("Timeframe changed to: " + timeframe);
    });
  });

  // Keyboard shortcuts
  document.addEventListener("keydown", (e) => {
    // Ctrl/Cmd + D to toggle theme
    if ((e.ctrlKey || e.metaKey) && e.key === "d") {
      e.preventDefault();
      toggleTheme();
    }

    // Ctrl/Cmd + R to refresh logs
    if ((e.ctrlKey || e.metaKey) && e.key === "r") {
      e.preventDefault();
      fetchLogs(currentLogLevel);
    }
  });

  // Handle system theme changes
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (!localStorage.getItem("theme")) {
      applyTheme(e.matches ? "dark" : "light");
      updateThemeToggleIcon();
    }
  });
}

// ===== ERROR HANDLING =====
/**
 * Global error handler
 */
window.addEventListener("error", (e) => {
  console.error("Global error:", e.error);
});

/**
 * Unhandled promise rejection handler
 */
window.addEventListener("unhandledrejection", (e) => {
  console.error("Unhandled promise rejection:", e.reason);
});
