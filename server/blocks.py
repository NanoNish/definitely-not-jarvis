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
