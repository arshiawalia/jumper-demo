from flask import Flask, render_template, request
from pusher import Pusher
from google.cloud import datastore
import datetime

app = Flask(__name__)
pusher = Pusher(app_id='1112407',
  key='ffd58499afb37a208daa',
  secret='a1e17a7bd3703f0155f5',
  cluster='ap2',
  ssl=True)

client = datastore.Client("jumper-chat-demo-296719")

@app.route('/')
def index():
    return render_template('sender.html')

def insert(message):
    with client.transaction():
        key = client.key("Task")
        task = datastore.Entity(key=key)

        task.update(
            {
                "created_ts": datetime.datetime.now(),
                "message": message,
            }
        )
        client.put(task)

@app.route('/receiver')
def receiver():
    records = fetch_records(10)
    return render_template('receiver.html', records=records)

@app.route('/messages', methods=['POST'])
def message():
    msg = {'message': request.form['messages']}
    
    pusher.trigger(u'my-msg', u'my-event', msg)

    insert(msg)
    return "message sent"

def fetch_records(limit):
    query = client.query(kind='Task')
    query.order = ['-created_ts']
    return query.fetch(limit=limit)

if __name__ == '__main__':
    app.run(debug=True)
