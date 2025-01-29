from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from flask import Flask, render_template, request
import os

model = GigaChat(
    credentials=os.getenv('CREDENTIALS'),
    scope=os.getenv('SCOPE'),
    model=os.getenv('MODEL'),
    verify_ssl_certs=False
)

app = Flask(__name__)

response = 'nothing'

@app.route('/', methods=['POST', 'GET'])
def index():
    global response
    if request.method == "POST":
        information = request.form['something']
        task = f"Сейчас я опишу тебе компанию и ее деятельность. {information}. Придумай стратегию для развития этого бизнеса"
        messages = [HumanMessage(content=task)]
        response = model.invoke(messages)
        response = response.content.replace('###', '').replace('**', '')
        return render_template('output.html', response=response)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
