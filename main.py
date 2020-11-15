from flask import Flask, render_template, request, Response
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

from algo import Algorithm
from msg_announcer import MessageAnnouncer


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
executor = ThreadPoolExecutor(1)
algo = Algorithm()
announcer = MessageAnnouncer()


def getContent():
    return f'## Knight tour solver\n\n{algo}\n'


def moveLoop():
    print('- Move loop started')
    while algo.move():
        announcer.announceSse(getContent())
        sleep(1)
    algo.placeAt()
    print('- Move loop ended')


@app.route('/')
def root():
    algo.placeAt()
    executor.submit(moveLoop)
    return render_template('md_sse.html', mdStr=getContent(), base_url=urljoin(request.base_url, 'listen'))


@app.errorhandler(500)
def server_error(e):
    print('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/ping')
def ping():
    algo.move()
    announcer.announceSse(getContent())
    return {}


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
