# Project 5 — Sample Crawler

Sample Crawler is an ethical, topic-focused web spider with a local web UI. It can:

- Take either **URLs** or just **keywords**
- Use DuckDuckGo to bootstrap URLs from keywords
- Crawl with either a standard or **Turbo (async)** mode
- Respect `robots.txt`, rate limit per domain, and identify with a custom User-Agent
- Score pages based on keyword relevance + a simple NLP-style density measure
- Show results in a table and export to CSV

## Run locally

```bash
cd projects/05-insights-crawler/app
pip install -r requirements.txt

# Windows PowerShell
$env:FLASK_APP = "web.app"
flask run
