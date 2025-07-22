class ConfigEditor {
  constructor() {
    this.apiUrl = ""
    this.config = null
    this.init()
  }

  init() {
    this.bindEvents()
    this.loadConfig()
  }

  bindEvents() {
    document.getElementById("loadBtn").addEventListener("click", () => this.loadConfig())
    document.getElementById("saveBtn").addEventListener("click", () => this.saveConfig())

    // Range input updates
    document.getElementById("dropout_rate").addEventListener("input", (e) => {
      document.getElementById("dropout_value").textContent = e.target.value
    })

    document.getElementById("test_size").addEventListener("input", (e) => {
      document.getElementById("test_size_value").textContent = e.target.value
    })
  }

  async loadConfig() {
    try {
      this.showLoading(true)
      const response = await fetch(`${this.apiUrl}/config`)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      this.config = await response.json()
      this.populateForm()
      this.showAlert("Configuration loaded successfully!", "success")
    } catch (error) {
      console.error("Error loading config:", error)
      this.showAlert("Failed to load configuration. Please check if the server is running.", "danger")
    } finally {
      this.showLoading(false)
    }
  }

  async saveConfig() {
    try {
      this.showLoading(true)
      const configData = this.getFormData()

      const response = await fetch(`${this.apiUrl}/config`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(configData),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      this.showAlert("Configuration saved successfully!", "success")
    } catch (error) {
      console.error("Error saving config:", error)
      this.showAlert("Failed to save configuration. Please try again.", "danger")
    } finally {
      this.showLoading(false)
    }
  }

  populateForm() {
    if (!this.config) return

    // Data configuration
    document.getElementById("augment").checked = this.config.data.augment
    document.getElementById("balance_classes").checked = this.config.data.balance_classes
    document.getElementById("task_type").value = this.config.data.task_type
    document.getElementById("min_samples").value = this.config.data.min_samples

    // Image data
    if (this.config.data.image_data) {
      document.getElementById("color_mode").value = this.config.data.image_data.color_mode
      document.getElementById("image_format").value = this.config.data.image_data.image_format
      document.getElementById("image_dir").value = this.config.data.image_data.image_dir
      document.getElementById("labels_file").value = this.config.data.image_data.labels_file

      if (this.config.data.image_data.resize_to) {
        document.getElementById("resize_width").value = this.config.data.image_data.resize_to[0]
        document.getElementById("resize_height").value = this.config.data.image_data.resize_to[1]
      }
    }

    // Text data
    if (this.config.data.text_data) {
      document.getElementById("raw_path").value = this.config.data.text_data.raw_path
      document.getElementById("processed_path").value = this.config.data.text_data.processed_path
    }

    // Model configuration
    document.getElementById("architecture").value = this.config.model.architecture
    document.getElementById("batch_size").value = this.config.model.batch_size
    document.getElementById("epochs").value = this.config.model.epochs
    document.getElementById("dropout_rate").value = this.config.model.dropout_rate
    document.getElementById("dropout_value").textContent = this.config.model.dropout_rate

    // LSTM settings
    if (this.config.model.lstm) {
      document.getElementById("embedding_dim").value = this.config.model.lstm.embedding_dim
      document.getElementById("hidden_units").value = this.config.model.lstm.hidden_units
      document.getElementById("lstm_activation").value = this.config.model.lstm.activation
      document.getElementById("bidirectional").checked = this.config.model.lstm.bidirectional
    }

    // CNN settings
    if (this.config.model.cnn) {
      document.getElementById("filters").value = this.config.model.cnn.filters
      document.getElementById("kernel_size").value = this.config.model.cnn.kernel_size
      document.getElementById("cnn_activation").value = this.config.model.cnn.activation
      document.getElementById("pooling").value = this.config.model.cnn.pooling
    }

    // Processing configuration
    document.getElementById("max_len").value = this.config.processing.max_len
    document.getElementById("max_words").value = this.config.processing.max_words
    document.getElementById("test_size").value = this.config.processing.test_size
    document.getElementById("test_size_value").textContent = this.config.processing.test_size
    document.getElementById("random_state").value = this.config.processing.random_state
    document.getElementById("normalize").checked = this.config.processing.normalize
    document.getElementById("stratify").checked = this.config.processing.stratify

    // Paths
    document.getElementById("base_dir").value = this.config.paths.base_dir
    document.getElementById("data_dir").value = this.config.paths.data_dir
    document.getElementById("artifacts_dir").value = this.config.paths.artifacts_dir
    document.getElementById("model_path").value = this.config.model.model_path
    document.getElementById("encoder_path").value = this.config.model.encoder_path
    document.getElementById("tokenizer_path").value = this.config.model.tokenizer_path
    document.getElementById("tflite_path").value = this.config.model.tflite_path
  }

  getFormData() {
    return {
      data: {
        augment: document.getElementById("augment").checked,
        balance_classes: document.getElementById("balance_classes").checked,
        task_type: document.getElementById("task_type").value,
        min_samples: Number.parseInt(document.getElementById("min_samples").value),
        image_data: {
          color_mode: document.getElementById("color_mode").value,
          image_format: document.getElementById("image_format").value,
          image_dir: document.getElementById("image_dir").value,
          labels_file: document.getElementById("labels_file").value,
          resize_to: [
            Number.parseInt(document.getElementById("resize_width").value),
            Number.parseInt(document.getElementById("resize_height").value),
          ],
        },
        text_data: {
          raw_path: document.getElementById("raw_path").value,
          processed_path: document.getElementById("processed_path").value,
          required_columns: ["text"],
          label_columns: ["label"],
        },
      },
      model: {
        architecture: document.getElementById("architecture").value,
        batch_size: Number.parseInt(document.getElementById("batch_size").value),
        epochs: Number.parseInt(document.getElementById("epochs").value),
        dropout_rate: Number.parseFloat(document.getElementById("dropout_rate").value),
        lstm: {
          embedding_dim: Number.parseInt(document.getElementById("embedding_dim").value),
          hidden_units: Number.parseInt(document.getElementById("hidden_units").value),
          activation: document.getElementById("lstm_activation").value,
          bidirectional: document.getElementById("bidirectional").checked,
        },
        cnn: {
          filters: Number.parseInt(document.getElementById("filters").value),
          kernel_size: Number.parseInt(document.getElementById("kernel_size").value),
          activation: document.getElementById("cnn_activation").value,
          pooling: document.getElementById("pooling").value,
        },
        model_path: document.getElementById("model_path").value,
        encoder_path: document.getElementById("encoder_path").value,
        tokenizer_path: document.getElementById("tokenizer_path").value,
        tflite_path: document.getElementById("tflite_path").value,
      },
      processing: {
        max_len: Number.parseInt(document.getElementById("max_len").value),
        max_words: Number.parseInt(document.getElementById("max_words").value),
        test_size: Number.parseFloat(document.getElementById("test_size").value),
        random_state: Number.parseInt(document.getElementById("random_state").value),
        normalize: document.getElementById("normalize").checked,
        stratify: document.getElementById("stratify").checked,
      },
      paths: {
        base_dir: document.getElementById("base_dir").value,
        data_dir: document.getElementById("data_dir").value,
        artifacts_dir: document.getElementById("artifacts_dir").value,
      },
    }
  }

  showLoading(show) {
    const spinner = document.getElementById("loadingSpinner")
    const form = document.getElementById("configForm")

    if (show) {
      spinner.style.display = "block"
      form.style.display = "none"
    } else {
      spinner.style.display = "none"
      form.style.display = "block"
    }
  }

  showAlert(message, type) {
    const alertContainer = document.getElementById("alertContainer")
    const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${type === "success" ? "check-circle" : "exclamation-triangle"} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `

    alertContainer.innerHTML = alertHtml

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      const alert = alertContainer.querySelector(".alert")
      if (alert) {
        alert.classList.add("fade")
        alert.style.display = "none"
      }
    }, 5000)
  }
}

// Initialize the application
document.addEventListener("DOMContentLoaded", () => {
  new ConfigEditor()
})
