# News Summarizer with Perplexity API

Automatically fetches, summarizes, and emails daily news briefs using Perplexity API.

## 🎯 Features

- Real-time web search for multiple topics
- AI-powered article summarization
- HTML-formatted email delivery
- Automatic scheduling (Windows Task Scheduler or Python)
- Local file archive

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file:

```
PERPLEXITY_API_KEY=your_perplexity_api_key
GMAIL_APP_PASSWORD=your_gmail_app_password
```

**Get keys:**
- Perplexity API: https://www.perplexity.ai/settings/api
- Gmail App Password: https://myaccount.google.com/apppasswords (enable 2-Step Verification first)

### 3. Configure Topics ⚠️ **Critical: Use Specific Keywords**

**Topics must be detailed and specific** - generic keywords return poor results. Include relevant terms, context, and focus areas.

**✅ Good Examples (from actual config):**
```json
{
  "topics": [
    "Venture capital emerging startup ecosystems innovation hubs",
    "Vietnamese economic development infrastructure investment trade agreements"
  ]
}
```

**❌ Bad Examples (too generic):**
```json
{
  "topics": [
    "technology",
    "venture capital",
    "vietnam"
  ]
}
```

**Why it matters:** Specific keywords help Perplexity find relevant, recent articles. Generic terms return outdated or irrelevant results.

### 4. Configure Email

Edit `config.json`:

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

### 5. Test

```bash
python news_summarizer.py
```

### 6. Schedule (Optional)

**Windows Task Scheduler:**
1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task → Daily, Recur every 3 days, Time: `08:00`
3. Action: Start program → `run_scheduled.bat`
4. Start in: Your project path

**Or use Python scheduler:**
```bash
python scheduler.py
```

## ⚙️ Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `topics` | **Specific, detailed topic queries** | Required |
| `articles_per_topic` | Articles per topic | `5` |
| `days_back` | Days to look back | `1` |
| `max_tokens` | Summary length (100-500) | `200` |
| `model` | Perplexity model | `"sonar"` |
| `auto_save` | Auto-save to file | `false` |
| `email.enabled` | Enable email | `false` |

## 🔧 Troubleshooting

**No email?** Check `email.enabled`, verify `.env` password, check spam folder.

**Few articles?** Use more specific keywords, increase `days_back`, adjust `articles_per_topic`.

**Scheduler not running?** Verify task is enabled, check task history, verify `run_scheduled.bat` path.

## 📖 Resources

- [Perplexity API Docs](https://docs.perplexity.ai/)
- [Perplexity API Portal](https://www.perplexity.ai/settings/api)
