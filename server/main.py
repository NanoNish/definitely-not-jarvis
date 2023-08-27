import os
from typing import Any

from dotenv import load_dotenv
from slack_bolt import App, Ack, Say

from clarifai import ClarifaiService
from blocks import make_blocks

load_dotenv()


# region init
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

service = ClarifaiService(
    api_key=os.environ.get("CLARIFAI_API_KEY", ""),
    user_id=os.environ.get("CLARIFAI_USER_ID", ""),
    app_id=os.environ.get("CLARIFAI_APP_ID", ""),
    workflow_id=os.environ.get("CLARIFAI_WORKFLOW_ID", ""),
)

BOT_ID = os.environ.get("SLACK_BOT_ID")
# endregion

# FAQs and Knowledge
faqs: list = [("Who is BURG3R5?", "BURG3R5 is a so-called developer who loves to 'code' in HTML and CSS")]
knowledge: list = ["Anand is a final-year student at IIT Roorkee. He has a strong passion" + \
        "for using technology to solve real-world problems, and he is constantly" + \
        "seeking new challenges to further improve his skills." ]

# Mentions
@app.event("app_mention")
def on_mention(ack: Ack, say: Say, payload: dict[str, Any]):
    ack()

    ts = payload.get("thread_ts", None) or payload.get("ts", None)
    
    user_input = payload.get("text", "").replace(f"<@{BOT_ID}>", "").strip()
    
    response_text = service.predict(
        faqs=faqs,
        knowledge=knowledge,
        user_input=user_input,
    )
    
    blocks = make_blocks(response_text, user_input)
    
    say(blocks=blocks, text=response_text, thread_ts=ts)

@app.action("try_again")
def try_again(ack: Ack, say: Say, body: Any):
    ack()
    
    ts = body.get("container", None).get("thread_ts", None)
    
    user_input = body.get("message", None).get("blocks", None)[1].get("elements", None)[0].get("value", None)
    
    response_text = service.predict(
        faqs=faqs,
        knowledge=knowledge,
        user_input=user_input,
    )
    
    blocks = make_blocks(response_text, user_input)
    
    say(blocks=blocks, text=response_text, thread_ts=ts)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
