from flask import Flask, render_template, request
from pusher import Pusher

app = Flask(__name__)
pusher = Pusher(app_id='1112407',
  key='ffd58499afb37a208daa',
  secret='a1e17a7bd3703f0155f5',
  cluster='ap2',
  ssl=True)

@app.route('/')
def index():
    return render_template('sender.html')

@app.route('/receiver')
def msg_html():
    return render_template('receiver.html')

@app.route('/messages', methods=['POST'])
def message():
    data = request.form
    pusher.trigger(u'my-msg', u'my-event', {
    	'message': data['messages']
    })
    return "message sent"

if __name__ == '__main__':
    app.run(debug=True)
