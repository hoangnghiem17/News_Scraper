# News Scraper with Perplexity API

A Python tool that uses the Perplexity API to fetch and summarize daily news articles.

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Key

1. Get your Perplexity API key from [Perplexity API Portal](https://www.perplexity.ai/settings/api)
2. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
3. Add your API key to `.env`:
   ```
   PERPLEXITY_API_KEY=your_actual_api_key_here
   ```

### 3. Run the Scripts

**Simple Example:**
```bash
python perplexity_example.py
```

**Daily News Summarizer:**
```bash
python news_summarizer.py
```

## 📚 How It Works

### Perplexity API Overview

The Perplexity API provides two main capabilities:

1. **Search API** - Fetches real-time web search results (including news articles)
2. **Chat Completions API** - Generates AI-powered summaries and responses

### Architecture

```
┌─────────────────┐
│  News Summarizer│
└────────┬────────┘
         │
         ├───> Search API (fetch news articles)
         │
         └───> Chat Completions API (generate summaries)
```

### Key Components

#### 1. **Search API** (`client.search.create()`)

Fetches news articles from the web with various filtering options:

**Parameters:**
- `query` (string): Search query (e.g., "technology news today")
- `max_results` (int): Maximum number of results (default: 5)
- `search_after_date_filter` (string): Filter news after this date (format: "MM/DD/YYYY")
- `search_before_date_filter` (string): Filter news before this date (format: "MM/DD/YYYY")

**Returns:**
- List of article objects with:
  - `title`: Article title
  - `url`: Source URL
  - `snippet`: Article preview/snippet

#### 2. **Chat Completions API** (`client.chat.completions.create()`)

Generates AI summaries using Perplexity's language model:

**Parameters:**
- `model` (string): Model to use (e.g., "sonar-small", "sonar-medium", "sonar-large", "sonar-pro")
- `messages` (list): List of message objects with `role` and `content`
- `max_tokens` (int): Maximum length of the response (default: 150)

**Returns:**
- Response object with generated text in `choices[0].message.content`

## 🛠️ Available Options & Customizations

### Search API Options

```python
# Basic search
search = client.search.create(
    query="your search query",
    max_results=10
)

# Date-filtered search (for daily news)
search = client.search.create(
    query="technology news",
    max_results=5,
    search_after_date_filter="12/01/2024",   # News from Dec 1, 2024 onwards
    search_before_date_filter="12/02/2024"    # Up to Dec 2, 2024
)

# Topic-specific search
search = client.search.create(
    query="AI developments in healthcare",
    max_results=10
)
```

### Chat Completions API Options

```python
# Short summary
response = client.chat.completions.create(
    model="sonar-small",
    messages=[
        {"role": "user", "content": "Summarize: [article text]"}
    ],
    max_tokens=100
)
summary = response.choices[0].message.content

# Detailed summary
response = client.chat.completions.create(
    model="sonar-medium",
    messages=[
        {"role": "user", "content": "Provide a detailed summary: [article text]"}
    ],
    max_tokens=300
)

# Custom prompts
response = client.chat.completions.create(
    model="sonar-small",
    messages=[
        {"role": "user", "content": "Extract key facts from: [article text]"}
    ],
    max_tokens=200
)
```

### NewsSummarizer Class Methods

#### `fetch_news(topic, max_results, days_back)`
- Fetch news for a specific topic
- Filter by number of days back
- Returns list of article objects

#### `summarize_article(article, max_tokens)`
- Generate summary for a single article
- Customizable summary length

#### `create_daily_brief(topics, articles_per_topic)`
- Create a comprehensive daily brief
- Support multiple topics
- Returns organized dictionary

## 📝 Usage Examples

### Example 1: Fetch Today's Technology News

```python
from news_summarizer import NewsSummarizer

summarizer = NewsSummarizer()
articles = summarizer.fetch_news(
    topic="technology news",
    max_results=5,
    days_back=1
)

for article in articles:
    print(f"{article.title}: {article.url}")
```

### Example 2: Create Multi-Topic Daily Brief

```python
summarizer = NewsSummarizer()

brief = summarizer.create_daily_brief(
    topics=["technology", "politics", "sports"],
    articles_per_topic=3
)

summarizer.print_brief(brief)
```

### Example 3: Custom Summary Length

```python
article = articles[0]
summary = summarizer.summarize_article(
    article,
    max_tokens=500  # Longer, more detailed summary
)
```

## 🔧 Advanced Customization

### Custom Date Ranges

```python
from datetime import datetime, timedelta

# Get news from last week
week_ago = (datetime.now() - timedelta(days=7)).strftime("%m/%d/%Y")
today = datetime.now().strftime("%m/%d/%Y")

search = client.search.create(
    query="technology news",
    search_after_date_filter=week_ago,
    search_before_date_filter=today,
    max_results=20
)
```

### Filtering by Source

You can filter results by checking the `url` field:

```python
articles = summarizer.fetch_news("technology")
techcrunch_articles = [a for a in articles if "techcrunch" in a.url.lower()]
```

### Batch Processing

```python
# Process multiple topics in parallel
topics = ["AI", "cryptocurrency", "climate change"]
all_articles = {}

for topic in topics:
    all_articles[topic] = summarizer.fetch_news(topic, max_results=5)
```

## 📊 Output Formats

The tool can output in multiple formats:

1. **Console Output** - Formatted text display
2. **Text File** - Save to `.txt` file (interactive prompt)
3. **JSON** - Modify code to return JSON structure
4. **Email** - Integrate with email libraries to send daily briefs

## ⚙️ Configuration

### Environment Variables

- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)

### Rate Limits

Be aware of Perplexity API rate limits:
- Check your plan's limits at the [API Portal](https://www.perplexity.ai/settings/api)
- Consider adding delays between requests for large batches

## 🚨 Error Handling

The scripts include basic error handling:
- Missing API key detection
- Network error handling
- Invalid date format validation

## 🔮 Future Enhancements

Potential improvements:
- [ ] Schedule daily runs with cron/scheduler
- [ ] Email delivery of daily briefs
- [ ] Database storage for historical summaries
- [ ] Web dashboard for viewing summaries
- [ ] RSS feed generation
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Keyword extraction

## 📖 Resources

- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity API Portal](https://www.perplexity.ai/settings/api)
- [Python SDK Guide](https://docs.perplexity.ai/guides/perplexity-sdk)

## 📄 License

This project is open source and available for personal use.

