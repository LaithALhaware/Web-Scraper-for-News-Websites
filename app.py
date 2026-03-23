from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from urllib.parse import urljoin

app = Flask(__name__)

# Function to scrape headlines
def scrape_news_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all(['h2', 'h3', 'h4'])

        news_data = []
        for idx, headline in enumerate(headlines, 1):
            text = headline.get_text(strip=True)
            link = headline.find('a')['href'] if headline.find('a') else None
            if text:
                if link and link.startswith('/'):
                    link = urljoin(url, link)
                news_data.append({
                    "id": idx,
                    "title": text,
                    "url": link
                })

        # Optional: save to JSON file
        now = datetime.now()
        folder = "news_headlines"
        os.makedirs(folder, exist_ok=True)
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            import json
            json.dump(news_data, f, ensure_ascii=False, indent=2)

        return news_data if news_data else [{"message": "No headlines found"}]

    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]


# Flask route for API
@app.route("/headlines", methods=["GET"])
def get_headlines():
    news_url = "https://www.bbc.com/news"  # Change to any news site
    data = scrape_news_api(news_url)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
