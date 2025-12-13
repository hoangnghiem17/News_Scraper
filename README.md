# News Summarizer with Perplexity API

A Python tool that automatically fetches, summarizes, and emails daily news briefs using Perplexity's AI-powered search and summarization.

## 🎯 What It Does

- **Fetches news** from multiple topics using Perplexity's real-time web search
- **Summarizes articles** using AI to extract key facts and main points
- **Sends formatted emails** with HTML-styled briefs
- **Runs automatically** every 3 days via Windows Task Scheduler
- **Saves briefs** to local files for archive

## 📚 How It Works

1. **Search API** - Perplexity searches the web in real-time for your topics
2. **Date Filtering** - Only gets articles from the specified date range
3. **AI Summarization** - Uses Perplexity's language model to create concise summaries
4. **Email Delivery** - Sends formatted HTML email via Gmail SMTP
5. **File Archive** - Saves briefs locally for reference

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```
PERPLEXITY_API_KEY=your_perplexity_api_key
GMAIL_APP_PASSWORD=your_gmail_app_password
```

**Get your keys:**
- Perplexity API: https://www.perplexity.ai/settings/api
- Gmail App Password: https://myaccount.google.com/apppasswords
  - Enable 2-Step Verification first
  - Generate password for "Mail" → "Windows Computer"

### 3. Configure Topics

Edit `config.json` to set your news topics:

```json
{
  "topics": [
    "technology companies announce",
    "venture capital",
    "vietnam technology"
  ],
  "articles_per_topic": 3,
  "days_back": 3
}
```

### 4. Set Up Email

Edit `config.json` email section:

```json
{
  "email": {
    "enabled": true,
    "sender_email": "your-email@gmail.com",
    "sender_password": "",
    "recipient_email": "your-email@gmail.com"
  },
  "auto_save": true
}
```

Leave `sender_password` empty - it uses `GMAIL_APP_PASSWORD` from `.env`.

### 5. Test It

```bash
python news_summarizer.py
```

You should receive an email with your news brief!

### 6. Schedule Automatic Runs

**Windows Task Scheduler:**

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task:
   - **Name:** `News Summarizer`
   - **Trigger:** Daily, Recur every **3 days**, Time: `08:00`
   - **Action:** Start program → Browse to `run_scheduled.bat`
   - **Start in:** `D:\Coding\News_Scraper` (your project path)
3. Test: Right-click task → **Run**

**Alternative - Python Scheduler:**

```bash
python scheduler.py
```

Runs every 3 days at 8:00 AM (keeps running in background).

## ⚙️ Configuration Options

Edit `config.json` to customize:

| Option | Description | Default |
|--------|-------------|---------|
| `topics` | List of news topics to track | `["general news"]` |
| `articles_per_topic` | Number of articles per topic | `5` |
| `days_back` | Days to look back for news | `1` |
| `max_tokens` | Summary length (100-500) | `200` |
| `model` | Perplexity model (`sonar`, `sonar-medium`, etc.) | `"sonar"` |
| `auto_save` | Auto-save briefs to file | `false` |
| `email.enabled` | Enable email sending | `false` |

## 📧 Email Features

- **HTML formatted** with styled layout
- **Clickable article links**
- **Organized by topic**
- **Plain text fallback** for email clients
- **Automatic sending** when enabled

## 📁 Output

- **Console:** Formatted brief display
- **Email:** HTML-styled email sent to your inbox
- **Files:** Saved to `briefs/` folder as `news_brief_YYYYMMDD.txt`

## 🔧 Troubleshooting

**No email received?**
- Check `email.enabled` is `true` in config
- Verify Gmail app password in `.env`
- Check spam folder
- Test manually: `python news_summarizer.py`

**Scheduler not running?**
- Verify Task Scheduler task is enabled
- Check task history for errors
- Verify `run_scheduled.bat` path is correct

**Few articles per topic?**
- Increase `days_back` (e.g., `3` for last 3 days)
- Adjust `articles_per_topic` based on topic popularity
- Some topics naturally have fewer daily articles

## 🛠️ Advanced Usage

### Custom Topics

Use specific, action-oriented queries for better results:

```json
{
  "topics": [
    "technology companies announce",
    "venture capital funding",
    "startup acquisitions",
    "vietnam technology"
  ]
}
```

### Adjust Summary Length

```json
{
  "max_tokens": 300  // Longer summaries (default: 200)
}
```

### Change Schedule Frequency

Edit `scheduler.py`:
```python
schedule.every(2).days.at("09:00").do(run_news_summarizer)  // Every 2 days at 9 AM
```

## 📖 Resources

- [Perplexity API Docs](https://docs.perplexity.ai/)
- [Perplexity API Portal](https://www.perplexity.ai/settings/api)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)

## 📄 License

Open source for personal use.
