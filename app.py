
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

    for page in data.get("results", []):
        props = page.get("properties", {})

        # Safe quote
        title_data = props.get("Quote", {}).get("title", [])
        if not title_data:
            continue
        quote = title_data[0].get("plain_text", "")

        # Safe author
        author_data = props.get("Author", {}).get("rich_text", [])
        author = author_data[0].get("plain_text", "Unknown") if author_data else "Unknown"

        quotes.append(f'"{quote}" — {author}')

    return quotes


@app.route("/", methods=["GET", "HEAD"])
def quote_of_day():
    try:
        quotes = get_quotes()

        if not quotes:
            return "No quotes found. Check Notion setup."

        index = datetime.now().timetuple().tm_yday % len(quotes)
        quote = quotes[index]

        return f"""
           <div style="font-family: Georgia; padding:40px; text-align:center;">
               <p style="font-size:22px;">{quote}</p>
           </div>
           """

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    app.run()