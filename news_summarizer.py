"""
Daily News Summarizer using Perplexity API
This tool fetches and summarizes daily news articles.
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from perplexity import Perplexity

# Load environment variables
load_dotenv()


def load_config(config_path="config.json"):
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to the config file
    
    Returns:
        Dictionary with configuration values
    """
    default_config = {
        "topics": ["general news"],
        "articles_per_topic": 5,
        "model": "sonar",
        "max_tokens": 200,
        "days_back": 1,
        "max_results": 10,
        "summary_prompt": "Summarize the following news article in 2-3 concise sentences. Focus on the key facts and main points:",
        "auto_save": False,
        "output_directory": "briefs",
        "date_format": "%B %d, %Y",
        "query_suffix": "today"
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with defaults (user config overrides defaults)
                default_config.update(user_config)
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Invalid JSON in {config_path}. Using defaults. Error: {e}")
        except Exception as e:
            print(f"⚠️  Warning: Error reading {config_path}. Using defaults. Error: {e}")
    else:
        print(f"ℹ️  No config file found at {config_path}. Using defaults.")
    
    return default_config


class NewsSummarizer:
    """A class to handle news fetching and summarization using Perplexity API."""
    
    # Check https://docs.perplexity.ai/getting-started/models for the latest models
    
    def __init__(self, api_key=None, model=None, config=None):
        """
        Initialize the News Summarizer with API key and configuration.
        
        Args:
            api_key: Perplexity API key (if None, reads from PERPLEXITY_API_KEY env var)
            model: Model to use for summarization (if None, uses config or default "sonar")
            config: Configuration dictionary (if None, loads from config.json)
        """
        if api_key is None:
            api_key = os.getenv("PERPLEXITY_API_KEY")
        
        if not api_key:
            raise ValueError(
                "PERPLEXITY_API_KEY is required. Set it in .env file or pass as argument."
            )
        
        # Load config if not provided
        if config is None:
            config = load_config()
        
        self.config = config
        self.client = Perplexity(api_key=api_key)
        self.model = model or config.get("model", "sonar")
        self.max_tokens = config.get("max_tokens", 200)
        self.summary_prompt = config.get("summary_prompt", "Summarize the following news article in 2-3 concise sentences. Focus on the key facts and main points:")
        self.query_suffix = config.get("query_suffix", "today")
        self.date_format = config.get("date_format", "%B %d, %Y")
    
    def fetch_news(self, topic="general news", max_results=None, days_back=None):
        """
        Fetch news articles for a specific topic.
        
        Args:
            topic: News topic to search for (e.g., "technology", "politics", "sports")
            max_results: Maximum number of articles to fetch (uses config if None)
            days_back: Number of days to look back for news (uses config if None)
        
        Returns:
            List of news article results
        """
        # Use config values if not provided
        max_results = max_results or self.config.get("max_results", 10)
        days_back = days_back or self.config.get("days_back", 1)
        
        # Calculate date range
        today = datetime.now()
        before_date = today.strftime("%m/%d/%Y")
        after_date = (today - timedelta(days=days_back)).strftime("%m/%d/%Y")
        
        print(f"🔍 Searching for {topic} from {after_date} to {before_date}...")
        
        # Build query with configurable suffix
        query = f"{topic} {self.query_suffix}" if self.query_suffix else topic
        
        search = self.client.search.create(
            query=query,
            max_results=max_results,
            search_after_date_filter=after_date,
            search_before_date_filter=before_date
        )
        
        return search.results
    
    def summarize_article(self, article, max_tokens=None):
        """
        Generate a summary for a single article.
        
        Args:
            article: Article object from search results
            max_tokens: Maximum tokens for summary (uses config if None)
        
        Returns:
            Summary string
        """
        max_tokens = max_tokens or self.max_tokens
        
        prompt = f"""{self.summary_prompt}

Title: {article.title}
Content: {article.snippet}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()
    
    def create_daily_brief(self, topics=None, articles_per_topic=5):
        """
        Create a daily news brief covering multiple topics.
        
        Args:
            topics: List of topics to cover (default: general news)
            articles_per_topic: Number of articles per topic
        
        Returns:
            Dictionary with topics and their summaries
        """
        if topics is None:
            topics = ["general news"]
        
        brief = {}
        
        for topic in topics:
            print(f"\n📰 Processing {topic}...")
            articles = self.fetch_news(topic, max_results=articles_per_topic)
            
            # Handle case where fewer articles are returned than requested
            if len(articles) == 0:
                print(f"   ⚠️  No articles found for {topic}")
                brief[topic] = []
                continue
            
            if len(articles) < articles_per_topic:
                print(f"   ℹ️  Found {len(articles)} articles (requested {articles_per_topic})")
            
            # Remove duplicates based on URL
            seen_urls = set()
            unique_articles = []
            for article in articles:
                if article.url not in seen_urls:
                    seen_urls.add(article.url)
                    unique_articles.append(article)
            
            if len(unique_articles) < len(articles):
                print(f"   ℹ️  Removed {len(articles) - len(unique_articles)} duplicate article(s)")
            
            topic_summaries = []
            for article in unique_articles:
                try:
                    summary = self.summarize_article(article)
                    topic_summaries.append({
                        "title": article.title,
                        "summary": summary,
                        "url": article.url,
                        "snippet": article.snippet
                    })
                except Exception as e:
                    print(f"   ⚠️  Error summarizing article '{article.title}': {e}")
                    continue
            
            brief[topic] = topic_summaries
            print(f"   ✅ Processed {len(topic_summaries)} article(s) for {topic}")
        
        return brief
    
    def print_brief(self, brief):
        """Print the daily brief in a formatted way."""
        print("\n" + "=" * 80)
        print("📰 DAILY NEWS BRIEF")
        print("=" * 80)
        print(f"Date: {datetime.now().strftime(self.date_format)}\n")
        
        for topic, articles in brief.items():
            if not articles:
                continue  # Skip empty topics
            
            print(f"\n{'=' * 80}")
            print(f"📌 {topic.upper()}")
            print(f"{'=' * 80}\n")
            
            for i, article in enumerate(articles, 1):
                print(f"{i}. {article['title']}")
                print(f"   {article['summary']}")
                print(f"   🔗 {article['url']}\n")
        
        print("=" * 80)


def save_brief_to_file(brief, config):
    """Save the brief to a file."""
    # Create output directory if it doesn't exist
    output_dir = config.get("output_directory", "briefs")
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename
    date_format = config.get("date_format", "%B %d, %Y")
    filename = f"news_brief_{datetime.now().strftime('%Y%m%d')}.txt"
    filepath = os.path.join(output_dir, filename) if output_dir else filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Daily News Brief - {datetime.now().strftime(date_format)}\n")
        f.write("=" * 80 + "\n\n")
        
        for topic, articles in brief.items():
            f.write(f"\n{topic.upper()}\n")
            f.write("-" * 80 + "\n\n")
            
            for i, article in enumerate(articles, 1):
                f.write(f"{i}. {article['title']}\n")
                f.write(f"   {article['summary']}\n")
                f.write(f"   {article['url']}\n\n")
    
    return filepath


def main():
    """Main function to run the daily news summarizer."""
    try:
        # Load configuration
        config = load_config()
        
        # Initialize summarizer with config
        summarizer = NewsSummarizer(config=config)
        
        # Get topics from config
        topics = config.get("topics", ["general news"])
        articles_per_topic = config.get("articles_per_topic", 5)
        
        # Create daily brief
        brief = summarizer.create_daily_brief(
            topics=topics,
            articles_per_topic=articles_per_topic
        )
        
        # Print the brief
        summarizer.print_brief(brief)
        
        # Handle saving to file
        auto_save = config.get("auto_save", False)
        
        if auto_save:
            filepath = save_brief_to_file(brief, config)
            print(f"\n✅ Brief automatically saved to {filepath}")
        else:
            save_to_file = input("\n💾 Save brief to file? (y/n): ").lower() == 'y'
            if save_to_file:
                filepath = save_brief_to_file(brief, config)
                print(f"✅ Brief saved to {filepath}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set PERPLEXITY_API_KEY in your .env file")
        print("2. Installed required packages: pip install -r requirements.txt")


if __name__ == "__main__":
    main()

