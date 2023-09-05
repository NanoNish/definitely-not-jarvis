import os
from typing import Any

from dotenv import load_dotenv
from slack_bolt import App, Ack, Say

from clarifai import ClarifaiService
from blocks import make_blocks
from strapi import get_all_faq, get_all_knowledge

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
faqs: list = get_all_faq()
knowledge: list = get_all_knowledge()

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

@app.action("contact_human")
def contact_human(ack: Ack, say: Say, body: Any):
    # contact human code comes here
    ack()

    print("clicked contact human")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
