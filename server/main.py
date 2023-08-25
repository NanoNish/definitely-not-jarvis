import os
from typing import Any

from dotenv import load_dotenv
from slack_bolt import App, Ack, Say


load_dotenv()
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_mention")
def on_mention(ack: Ack, say: Say, payload: dict[str, Any]):
    ack()

    ts = payload.get("thread_ts", None) or payload.get("ts", None)

    say(text="Thanks for mentioning me!", thread_ts=ts)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
