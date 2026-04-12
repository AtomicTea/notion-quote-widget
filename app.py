
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

            # --- Quote (title field) ---
            quote_list = props.get("Quote", {}).get("title", [])
            if not quote_list:
                continue
            quote = quote_list[0].get("plain_text", "").strip()

            if not quote:
                continue

            # --- Author (rich text field) ---
            author_list = props.get("Author", {}).get("rich_text", [])
            author = author_list[0].get("plain_text", "Unknown") if author_list else "Unknown"

            quotes.append(f'{quote} — {author}')

        return quotes

    from datetime import datetime

    @app.route("/", methods=["GET", "HEAD"])
    def quote_of_day():
        try:
            quotes = get_quotes()

            if not quotes:
                return "No quotes found."

            index = datetime.now().timetuple().tm_yday % len(quotes)
            quote = quotes[index]

            return f"""
            <div style="font-family: Georgia; padding:40px; text-align:center;">
                <p style="font-size:24px;">{quote}</p>
            </div>
            """

        except Exception as e:
            return f"ERROR: {str(e)}"


#@app.route("/", methods=["GET", "HEAD"])
#def quote_of_day():
    quotes = get_quotes()

    if not quotes:
        return "No quotes found."

    index = datetime.now().timetuple().tm_yday % len(quotes)
    quote = quotes[index]

    return f"""
    <div style="font-family: Georgia; padding:40px; text-align:center;">
        <p style="font-size:24px;">{quote}</p>
    </div>
    """
@app.route("/", methods=["GET", "HEAD"])
def quote_of_day():
    try:
        quotes = get_quotes()

        return f"DEBUG: got {len(quotes)} quotes"

    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    app.run()