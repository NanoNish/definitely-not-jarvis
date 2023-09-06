def make_blocks(response, user_input):
    blocks = []
    response_block = {
        "type": "section",
			"text": {
				"type": "plain_text",
				"text": f"{response}",
			}
    }
    buttons_block = {"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Try again",
					},
					"value": f"{user_input}",
					"action_id": "try_again"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Contact a human",
					},
					"value": "contact_human",
					"action_id": "contact_human"
				}
            ]}
    
    blocks.append(response_block)
    blocks.append(buttons_block)
    return blocks

def make_forward_blocks(prompt, prompt_type, user):
    blocks = []
    prompt_type_block = {
        "type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"We recieved a query of type *{prompt_type}* from <@{user}>",
			}, 
	}
    prompt_block = {
        "type": "section",
			"text": {
				"type": "plain_text",
				"text": f"{prompt}",
			}, 
	}
    blocks.append(prompt_type_block)
    blocks.append(prompt_block)
    return blocks
