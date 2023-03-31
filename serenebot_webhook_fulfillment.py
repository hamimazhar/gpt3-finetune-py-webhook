from flask import Flask, request
import os
import openai
import sys

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')  # this is the home page route
def hello_world(
):  # this is the home page function that generates the page code
    return "Hello world!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        req = request.get_json(silent=True, force=True)
        fulfillmentText = 'you said'
        query_result = req.get('queryResult')
        query = query_result.get('queryText')

        start_sequence = "\nSereneot->"
        restart_sequence = "\nUser->"

        if query_result.get('action') == 'input.unknown':

            response = openai.Completion.create(
                model="davinci:ft-personal-2023-03-30-00-46-09",
                prompt="The following is a conversation with an AI assistant whose name is SereneBot. SereneBot can have meaningful conversations with users. SereneBot  is helpful, empathic, and friendly. SereneBot's objective is to make the user feel better by feeling heard, tell them jokes, and provide them with mental health resources. With each response, SereneBot  prompts the user to continue the conversation in a natural way. SereneBot  also recommends music to the user based on their preference. SereneBot  will search the internet to help provide mental health resources to the user to help them with sadness, anxiety or depression. SereneBot-> Hello, I am SerenBot, your personal mental health assistant. What's on your mind today?->",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n"]

  )

        result = response.get('choices')[0].get('text')

        return {
            "fulfillmentText":
            result,
            "source":
            "webhookdata"
        }
        return '200'
    except Exception as e:
        print('error',e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('oops',exc_type, fname, exc_tb.tb_lineno)
        return '400'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
