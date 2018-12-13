from flask import Flask, request
from pymessenger import Bot

app = Flask("My echo bot")

FB_ACCESS_TOKEN = "PAGE_ACCESS_TOKEN_HERE"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "TOKKEN007"


@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Its Working", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()

	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender = messaging_event['sender']['id']
				recipient = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					if messaging_event['message'].get('text'):
						query = messaging_event['message']['text']
						bot.send_text_message(sender, query)
	return "ok", 200


if __name__ == "__main__":
	app.run(port=8000, use_reloader = True)
