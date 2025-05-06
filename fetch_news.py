import feedparser

# RSS feed URL for technology news from India
rss_url = "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en"

# Parse the feed
feed = feedparser.parse(rss_url)

# Loop through fetched news
for entry in feed.entries:
    print("Title:", entry.title)
    print("Link:", entry.link)
    print("Published:", entry.published)
    print("Summary:", entry.summary)
    print("-" * 80)
