let currentData = null;
let selectedModel = "finbert";
BASE_PATH = "http://127.0.0.1:8000/api";

// Model selection
document.querySelectorAll(".model-card").forEach((card) => {
  card.addEventListener("click", function () {
    document
      .querySelectorAll(".model-card")
      .forEach((c) => c.classList.remove("active"));
    this.classList.add("active");
    selectedModel = this.dataset.model;
  });
});

// Filter tabs
document.querySelectorAll(".filter-tab").forEach((tab) => {
  tab.addEventListener("click", function () {
    document
      .querySelectorAll(".filter-tab")
      .forEach((t) => t.classList.remove("active"));
    this.classList.add("active");
  });
});

async function analyzeNews() {
  console.log("Starting analysis...");

  try {
    const ticker = document.getElementById("ticker").value.trim();
    if (!ticker) {
      alert("Mohon masukkan ticker symbol");
      return;
    }

    // Show loading
    document.querySelector(".loading").classList.add("active");
    document.querySelector(".results-section").classList.remove("active");

    if (!selectedModel) {
      console.log("You haven't selected a model");
      return;
    }

    // Set model
    const res = await fetch(`${BASE_PATH}/set_model`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model_name: selectedModel,
      }),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    console.log("Set model response:", data);

    // Get predictions
    const res2 = await fetch(`${BASE_PATH}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        stock_symbol: ticker,
      }),
    });

    if (!res2.ok) {
      throw new Error(`HTTP error! status: ${res2.status}`);
    }

    const data2 = await res2.json();
    console.log("Prediction response:", data2);

    // Transform API response to match our display format
    const transformedData = {
      ticker: ticker,
      model: selectedModel,
      news: data2.data.map((item) => ({
        title: item.headline,
        sentiment: item.sentiment.toLowerCase(),
        importance:
          item.importance === "non-major"
            ? "minor"
            : item.importance.toLowerCase(),
        source: item.source,
      })),
    };

    // Calculate summary
    transformedData.summary = calculateSummary(transformedData.news);

    // Store current data
    currentData = transformedData;

    // Display results
    displayResults(transformedData);

    document.querySelector(".loading").classList.remove("active");
    document.querySelector(".results-section").classList.add("active");
  } catch (err) {
    console.error("Analyze news error:", err);
    document.querySelector(".loading").classList.remove("active");
    alert("Gagal menganalisis berita. Silakan coba lagi.");
  }
}

function calculateSummary(news) {
  const major = news.filter((n) => n.importance === "major").length;
  const positive = news.filter((n) => n.sentiment === "positive").length;
  const negative = news.filter((n) => n.sentiment === "negative").length;
  const neutral = news.filter((n) => n.sentiment === "neutral").length;

  const sentimentScore =
    news.length > 0 ? ((positive - negative) / news.length).toFixed(2) : "0.00";

  const dominant =
    positive > negative
      ? "Positive"
      : negative > positive
      ? "Negative"
      : "Neutral";

  return {
    total: news.length,
    major: major,
    sentimentScore: sentimentScore,
    dominant: dominant,
    positive: positive,
    negative: negative,
    neutral: neutral,
  };
}

function displayResults(data) {
  const summary = data.summary;

  // Update summary cards
  document.getElementById("totalNews").textContent = summary.total;
  document.getElementById("majorNews").textContent = summary.major;
  document.getElementById("sentimentScore").textContent =
    summary.sentimentScore;

  const sentimentEl = document.getElementById("dominantSentiment");
  sentimentEl.textContent = summary.dominant;
  sentimentEl.className = "value sentiment-" + summary.dominant.toLowerCase();

  // Display news list
  displayNewsList(data.news);
}

function getSourceDomain(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname.replace("www.", "");
  } catch (e) {
    return "Unknown Source";
  }
}

function displayNewsList(news, filter = "all") {
  const newsListEl = document.getElementById("newsList");

  let filteredNews = news;
  if (filter === "positive") {
    filteredNews = news.filter((n) => n.sentiment === "positive");
  } else if (filter === "negative") {
    filteredNews = news.filter((n) => n.sentiment === "negative");
  } else if (filter === "neutral") {
    filteredNews = news.filter((n) => n.sentiment === "neutral");
  }

  if (filteredNews.length === 0) {
    newsListEl.innerHTML =
      '<p style="text-align: center; color: #666; padding: 40px;">Tidak ada berita yang sesuai dengan filter.</p>';
    return;
  }

  newsListEl.innerHTML = filteredNews
    .map(
      (item) => `
        <div class="news-item">
            <div class="news-header">
                <div class="news-title">${item.title}</div>
                <a href="${
                  item.source
                }" target="_blank" rel="noopener noreferrer" class="news-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                </a>
            </div>
            <div class="news-source">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
                ${getSourceDomain(item.source)}
            </div>
            <div class="news-labels">
                <div class="label-item">
                    <span class="label-title">Sentiment:</span>
                    <span class="badge badge-${
                      item.sentiment
                    }">${item.sentiment.toUpperCase()}</span>
                </div>
                <div class="label-item">
                    <span class="label-title">Importance:</span>
                    <span class="badge badge-${
                      item.importance
                    }">${item.importance.toUpperCase()}</span>
                </div>
            </div>
        </div>
    `
    )
    .join("");
}

function filterNews(filter) {
  if (currentData) {
    displayNewsList(currentData.news, filter);
  }
}

function exportJSON() {
  if (!currentData) return;

  const dataStr = JSON.stringify(currentData, null, 2);
  const dataBlob = new Blob([dataStr], { type: "application/json" });
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `majormove-${currentData.ticker}-${
    new Date().toISOString().split("T")[0]
  }.json`;
  link.click();
}

function exportCSV() {
  if (!currentData) return;

  const headers = ["Title", "Source", "Sentiment", "Importance"];
  const rows = currentData.news.map((item) => [
    item.title,
    item.source,
    item.sentiment,
    item.importance,
  ]);

  let csvContent = headers.join(",") + "\n";
  rows.forEach((row) => {
    csvContent += row.map((cell) => `"${cell}"`).join(",") + "\n";
  });

  const blob = new Blob([csvContent], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `majormove-${currentData.ticker}-${
    new Date().toISOString().split("T")[0]
  }.csv`;
  link.click();
}
