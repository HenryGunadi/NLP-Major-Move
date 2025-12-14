let currentData = null;
let selectedModel = 'finbert';
let realDataset = [];

// Load real dataset from Excel file
async function loadDataset() {
    try {
        const response = await fetch('complete_labeled_dataset.xlsx');
        const arrayBuffer = await response.arrayBuffer();
        const workbook = XLSX.read(arrayBuffer, {type: 'array'});
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        realDataset = XLSX.utils.sheet_to_json(firstSheet);
        console.log('Dataset loaded:', realDataset.length, 'articles');
    } catch (error) {
        console.error('Error loading dataset:', error);
        // Fallback to embedded dataset if file not found
        realDataset = getEmbeddedDataset();
    }
}

// Embedded dataset as fallback
function getEmbeddedDataset() {
    return [
        {
            "Headline": "Apple Inc. Reports Record Q4 Earnings, Exceeding Wall Street Expectations",
            "Sentiment": "positive",
            "Importance": "major"
        },
        {
            "Headline": "Tesla Announces Major Price Cuts Across All Models in Response to Competition",
            "Sentiment": "neutral",
            "Importance": "major"
        },
        {
            "Headline": "Google Parent Alphabet Faces Antitrust Lawsuit from DOJ Over Search Monopoly",
            "Sentiment": "negative",
            "Importance": "major"
        },
        {
            "Headline": "Microsoft Azure Cloud Services Show Strong Growth in Latest Quarter",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Amazon Prime Day Sales Break Previous Records with $12 Billion Revenue",
            "Sentiment": "positive",
            "Importance": "major"
        },
        {
            "Headline": "Meta Platforms Announces Layoffs Affecting 10,000 Employees Globally",
            "Sentiment": "negative",
            "Importance": "major"
        },
        {
            "Headline": "NVIDIA Stock Surges as AI Chip Demand Continues to Soar",
            "Sentiment": "positive",
            "Importance": "major"
        },
        {
            "Headline": "Intel Delays Next-Gen Chip Launch Due to Manufacturing Challenges",
            "Sentiment": "negative",
            "Importance": "minor"
        },
        {
            "Headline": "Berkshire Hathaway Increases Stake in Apple by 5%",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "JPMorgan Chase Reports Stable Q3 Results Meeting Analyst Forecasts",
            "Sentiment": "neutral",
            "Importance": "minor"
        },
        {
            "Headline": "Boeing Faces New Safety Concerns After Recent Incident",
            "Sentiment": "negative",
            "Importance": "major"
        },
        {
            "Headline": "Coca-Cola Expands Product Line with New Health-Focused Beverages",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Goldman Sachs Upgrades Tech Sector Outlook for 2024",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Toyota Accelerates Electric Vehicle Production Plans",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Walmart Raises Minimum Wage for Store Associates",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Netflix Subscriber Growth Slows in Competitive Streaming Market",
            "Sentiment": "negative",
            "Importance": "minor"
        },
        {
            "Headline": "Pfizer Vaccine Sales Decline as Pandemic Concerns Ease",
            "Sentiment": "negative",
            "Importance": "minor"
        },
        {
            "Headline": "Adobe Completes Acquisition of Figma for $20 Billion",
            "Sentiment": "neutral",
            "Importance": "major"
        },
        {
            "Headline": "ExxonMobil Reports Strong Profits Amid High Oil Prices",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Starbucks Opens 1000th Store in China Market",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Ford Recalls 500,000 Vehicles Due to Safety Issue",
            "Sentiment": "negative",
            "Importance": "major"
        },
        {
            "Headline": "Qualcomm Wins Patent Case Against Apple",
            "Sentiment": "positive",
            "Importance": "minor"
        },
        {
            "Headline": "Twitter (X) User Engagement Drops Following Platform Changes",
            "Sentiment": "negative",
            "Importance": "minor"
        },
        {
            "Headline": "Bank of America Maintains Steady Performance in Q4",
            "Sentiment": "neutral",
            "Importance": "neutral"
        },
        {
            "Headline": "Disney+ Announces Price Increase for Streaming Service",
            "Sentiment": "neutral",
            "Importance": "minor"
        }
    ];
}

// Initialize on page load
loadDataset();

// Model selection
document.querySelectorAll('.model-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.model-card').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        selectedModel = this.dataset.model;
    });
});

// Filter tabs
document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
    });
});

function analyzeNews() {
    const ticker = document.getElementById('ticker').value.trim();
    if (!ticker) {
        alert('Mohon masukkan ticker symbol');
        return;
    }

    // Show loading
    document.querySelector('.loading').classList.add('active');
    document.querySelector('.results-section').classList.remove('active');

    // Use real dataset
    setTimeout(() => {
        currentData = generateDataFromRealDataset(ticker);
        displayResults(currentData);
        document.querySelector('.loading').classList.remove('active');
        document.querySelector('.results-section').classList.add('active');
    }, 2000);
}

function generateDataFromRealDataset(ticker) {
    const tickers = ticker.split(',').map(t => t.trim().toUpperCase());
    
    // Use real dataset if available, otherwise use embedded
    const dataset = realDataset.length > 0 ? realDataset : getEmbeddedDataset();
    
    // Randomly select articles from dataset
    const numArticles = Math.min(30, dataset.length);
    const selectedIndices = new Set();
    
    while (selectedIndices.size < numArticles) {
        selectedIndices.add(Math.floor(Math.random() * dataset.length));
    }
    
    const news = Array.from(selectedIndices).map(idx => {
        const article = dataset[idx];
        const selectedTicker = tickers[Math.floor(Math.random() * tickers.length)];
        
        // Map column names (handle different possible column names)
        const headline = article.Headline || article.headline || article.title || article.Title || 'No headline';
        const sentiment = (article.Sentiment || article.sentiment || 'neutral').toLowerCase();
        const importance = (article.Importance || article.importance || 'neutral').toLowerCase();
        
        return {
            title: `${selectedTicker}: ${headline}`,
            importance: importance,
            sentiment: sentiment,
            source: generateSource()
        };
    });

    return {
        ticker: ticker,
        model: selectedModel,
        news: news,
        summary: calculateSummary(news)
    };
}

function generateSource() {
    const sources = [
        'Reuters', 'Bloomberg', 'CNBC', 'Yahoo Finance', 'MarketWatch',
        'Financial Times', 'Wall Street Journal', 'The Economist',
        'Seeking Alpha', 'Barron\'s', 'Forbes', 'Business Insider'
    ];
    return sources[Math.floor(Math.random() * sources.length)];
}

function calculateSummary(news) {
    const major = news.filter(n => n.importance === 'major').length;
    const positive = news.filter(n => n.sentiment === 'positive').length;
    const negative = news.filter(n => n.sentiment === 'negative').length;
    const neutral = news.filter(n => n.sentiment === 'neutral').length;

    const sentimentScore = ((positive - negative) / news.length).toFixed(2);
    const dominant = positive > negative ? 'Positive' : negative > positive ? 'Negative' : 'Neutral';

    return {
        total: news.length,
        major: major,
        sentimentScore: sentimentScore,
        dominant: dominant,
        positive: positive,
        negative: negative,
        neutral: neutral
    };
}

function displayResults(data) {
    const summary = data.summary;

    // Update summary cards
    document.getElementById('totalNews').textContent = summary.total;
    document.getElementById('majorNews').textContent = summary.major;
    document.getElementById('sentimentScore').textContent = summary.sentimentScore;
    
    const sentimentEl = document.getElementById('dominantSentiment');
    sentimentEl.textContent = summary.dominant;
    sentimentEl.className = 'value sentiment-' + summary.dominant.toLowerCase();

    // Display news list
    displayNewsList(data.news);
}

function displayNewsList(news, filter = 'all') {
    const newsListEl = document.getElementById('newsList');
    
    let filteredNews = news;
    if (filter === 'positive') {
        filteredNews = news.filter(n => n.sentiment === 'positive');
    } else if (filter === 'negative') {
        filteredNews = news.filter(n => n.sentiment === 'negative');
    } else if (filter === 'neutral') {
        filteredNews = news.filter(n => n.sentiment === 'neutral');
    }

    if (filteredNews.length === 0) {
        newsListEl.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">Tidak ada berita yang sesuai dengan filter.</p>';
        return;
    }

    newsListEl.innerHTML = filteredNews.map(item => `
        <div class="news-item">
            <div class="news-title">${item.title}</div>
            <div class="news-source">📰 ${item.source}</div>
            <div class="news-labels">
                <div class="label-item">
                    <span class="label-title">Sentiment:</span>
                    <span class="badge badge-${item.sentiment}">${item.sentiment.toUpperCase()}</span>
                </div>
                <div class="label-item">
                    <span class="label-title">Importance:</span>
                    <span class="badge badge-${item.importance}">${item.importance.toUpperCase()}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function filterNews(filter) {
    if (currentData) {
        displayNewsList(currentData.news, filter);
    }
}

function exportJSON() {
    if (!currentData) return;
    
    const dataStr = JSON.stringify(currentData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `majormove-${currentData.ticker}-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
}

function exportCSV() {
    if (!currentData) return;

    const headers = ['Title', 'Source', 'Sentiment', 'Importance'];
    const rows = currentData.news.map(item => [
        item.title,
        item.source,
        item.sentiment,
        item.importance
    ]);

    let csvContent = headers.join(',') + '\n';
    rows.forEach(row => {
        csvContent += row.map(cell => `"${cell}"`).join(',') + '\n';
    });

    const blob = new Blob([csvContent], {type: 'text/csv'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `majormove-${currentData.ticker}-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
}