"""
Scheduler script to run news summarizer every 3 days.
This script can run as a background service or be scheduled via Windows Task Scheduler.
"""

import schedule
import time
import sys
from datetime import datetime
from news_summarizer import main

def run_news_summarizer():
    """Run the news summarizer and handle any errors."""
    print(f"\n{'='*80}")
    print(f"🕐 Scheduled run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    try:
        main()
        print(f"\n✅ Scheduled run completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"\n❌ Error in scheduled run: {e}")
        # Don't exit - keep the scheduler running
    finally:
        print(f"\n{'='*80}\n")


def run_immediately():
    """Run immediately for testing."""
    print("🚀 Running news summarizer immediately (test mode)...")
    run_news_summarizer()


if __name__ == "__main__":
    # Schedule to run every 3 days at 8:00 AM
    schedule.every(3).days.at("08:00").do(run_news_summarizer)
    
    # Alternative: Run at specific time every 3 days
    # schedule.every().monday.at("08:00").do(run_news_summarizer)  # Every Monday
    # schedule.every().wednesday.at("08:00").do(run_news_summarizer)  # Every Wednesday
    # schedule.every().friday.at("08:00").do(run_news_summarizer)  # Every Friday
    
    print("📅 News Summarizer Scheduler Started")
    print(f"⏰ Will run every 3 days at 08:00 AM")
    print(f"🕐 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏳ Next run: {schedule.next_run()}")
    print("\nPress Ctrl+C to stop the scheduler\n")
    
    # Check for command line argument to run immediately
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        run_immediately()
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n🛑 Scheduler stopped by user")

