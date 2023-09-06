import os
from typing import Any

from dotenv import load_dotenv
from slack_bolt import App, Ack, Say

load_dotenv()

from clarifai import ClarifaiService
from blocks import make_blocks, make_forward_blocks
from strapi import get_all_faq, get_all_knowledge, get_subscribers


# region init
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

assistant = ClarifaiService(
    api_key=os.environ.get("CLARIFAI_API_KEY", ""),
    user_id=os.environ.get("CLARIFAI_USER_ID", ""),
    app_id=os.environ.get("CLARIFAI_APP_ID", ""),
    workflow_id=os.environ.get("CLARIFAI_ASSISTANT_WORKFLOW_ID", ""),
)

classifier = ClarifaiService(
    api_key=os.environ.get("CLARIFAI_API_KEY", ""),
    user_id=os.environ.get("CLARIFAI_USER_ID", ""),
    app_id=os.environ.get("CLARIFAI_APP_ID", ""),
    workflow_id=os.environ.get("CLARIFAI_CLASSIFIER_WORKFLOW_ID", ""),
)

BOT_ID = os.environ.get("SLACK_BOT_ID")
# endregion

# FAQs and Knowledge
# TODO: cache this and call periodically
faqs: list = get_all_faq()
knowledge: list = get_all_knowledge()

@app.event("app_mention")
def on_mention(ack: Ack, say: Say, payload: dict[str, Any]):
    ack()

    ts = payload.get("thread_ts", None) or payload.get("ts", None)

    user_input = payload.get("text", "").replace(f"<@{BOT_ID}>", "").strip()

    response_text = assistant.answer(
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

    user_input = body.get("message", None).get("blocks", None)[
        1].get("elements", None)[0].get("value", None)

    response_text = assistant.answer(
        faqs=faqs,
        knowledge=knowledge,
        user_input=user_input,
    )

    blocks = make_blocks(response_text, user_input)

    say(blocks=blocks, text=response_text, thread_ts=ts)


@app.action("contact_human")
def contact_human(ack: Ack, say: Say, body: Any):
    ack()

    ts = body.get("container", None).get("thread_ts", None)

    user_input = body.get("message", None).get("blocks", None)[
        1].get("elements", None)[0].get("value", None)

    input_type, project = classifier.classify(
        knowledge=knowledge,
        user_input=user_input,
    )
    user = body.get("user", None).get("id", None)


    forward_channels = get_subscribers(project=project.lower()).get("channels", None)
    forward_blocks = make_forward_blocks(user_input, input_type, user)
    for channel in forward_channels:
        say(blocks=forward_blocks, text="forwarded query", channel=channel)

    say(text="We have forwarded your query to the relevant people", thread_ts=ts)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
