from flask import Flask, render_template, request, Response
from urllib.parse import urljoin

from msg_announcer import announcer
import mydata


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def root():
    mydata.runDataPollingLoop()
    return render_template('md_sse.html', mdStr=mydata.getContent(), base_url=urljoin(request.base_url, 'listen'))


@app.errorhandler(500)
def server_error(e):
    print('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.route('/ping')
def ping():
    content = mydata.getContent()
    announcer.announceSse(content)
    return content, 200


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
