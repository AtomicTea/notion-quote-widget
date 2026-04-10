
from flask import Flask
import requests
import random
from datetime import datetime
import os

app = Flask(__name__)

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("DATABASE_ID")

def get_quotes():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    quotes = []

    for page in data["results"]:
        props = page["properties"]

        try:
            quote = props["Quote"]["title"][0]["plain_text"]
        except:
            continue

        author = "Unknown"
        if props["Author"]["rich_text"]:
            author = props["Author"]["rich_text"][0]["plain_text"]

        quotes.append(f'"{quote}" — {author}')

    return quotes


@app.route("/")
def quote_of_day():
    quotes = get_quotes()

    if not quotes:
        return "No quotes found."

    # Deterministic daily quote
    index = datetime.now().timetuple().tm_yday % len(quotes)
    quote = quotes[index]

    return f"""
    <div style="font-family: Georgia; padding:40px; text-align:center;">
        <p style="font-size:22px;">{quote}</p>
    </div>
    """


if __name__ == "__main__":
    app.run()