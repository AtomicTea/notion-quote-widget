from flask import Flask
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Environment variables (set these in Render)
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

        # Get quote (title field)
        quote_list = props.get("Quote", {}).get("title", [])
        if not quote_list:
            continue

        quote = quote_list[0].get("plain_text", "").strip()
        if not quote:
            continue

        # Get author
        author_list = props.get("Author", {}).get("rich_text", [])
        author = author_list[0].get("plain_text", "Unknown") if author_list else "Unknown"

        quotes.append(f"{quote} — {author}")

    return quotes


@app.route("/", methods=["GET", "HEAD"])
def quote_of_day():
    try:
        quotes = get_quotes()

        if not quotes:
            return "No quotes found."

        # Daily rotating quote
        index = datetime.now().timetuple().tm_yday % len(quotes)
        quote = quotes[index]

        return f"""
        <div style="
            font-family: 'Georgia', serif;
            padding: 28px;
            text-align: left;
            background: #f4efe6;
            color: #2b2b2b;
            border-radius: 16px;
            max-width: 520px;
            margin: auto;
            position: relative;
            overflow: hidden;
        ">

            <!-- Accent shapes -->
            <div style="
                position: absolute;
                top: -40px;
                right: -40px;
                width: 140px;
                height: 140px;
                background: #d96c3d;
                border-radius: 50%;
                opacity: 0.9;
            "></div>

            <div style="
                position: absolute;
                bottom: -30px;
                left: -30px;
                width: 120px;
                height: 120px;
                background: #3f6f73;
                border-radius: 20px;
                transform: rotate(25deg);
                opacity: 0.85;
            "></div>

            <!-- Header -->
            <div style="
                font-size: 12px;
                letter-spacing: 2px;
                margin-bottom: 12px;
                opacity: 0.6;
            ">
                ATOMIC TEA WORKS
            </div>

            <!-- Quote -->
            <div style="
                font-size: 22px;
                line-height: 1.5;
                margin-bottom: 18px;
                position: relative;
                z-index: 2;
            ">
                {quote}
            </div>

            <!-- Divider -->
            <div style="
                width: 40px;
                height: 3px;
                background: #d96c3d;
                margin-bottom: 12px;
            "></div>

            <!-- Footer -->
            <div style="
                font-size: 11px;
                letter-spacing: 1.5px;
                opacity: 0.6;
            ">
                DAILY EDITION
            </div>

            <!-- Refresh button -->
            <button onclick="location.reload()" style="
                margin-top: 16px;
                padding: 6px 12px;
                background: transparent;
                border: 1px solid #2b2b2b;
                border-radius: 8px;
                font-size: 11px;
                letter-spacing: 1px;
                cursor: pointer;
            ">
                NEW QUOTE
            </button>

        </div>
        """

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    app.run()