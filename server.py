from flask import *
import threading
import time
import humanfriendly
import os

# app
app = Flask(__name__, static_folder='ports/')

@app.route('/')
def index():
    return render_template('index.html', cache=cache)

@app.route('/port/<port>')
def viewPort(port):
    data = cache[port]
    return render_template('port.html', port=port, data=data)

@app.route('/get/<port>')
def rawPort(port):
    return app.send_static_file(port)

# cache
ports = ['80', '8080', '22', '21', '23', '6379', '27017', '3306']
cache = {}

def refreshCache():
    for port in ports:
        lines = sum(1 for line in open('ports/' + port))
        size = int(os.path.getsize('ports/' + port ))

        cache[port] = {
                'lines': lines,
                'formattedLines': f'{lines:,}',
                'size': size,
                'formattedSize': humanfriendly.format_size(size)
        }

def cacheRefreshLoop():
    while True:
        refreshCache()
        time.sleep(1)

def startCacheThread():
    cacheRefreshThread = threading.Thread(target=cacheRefreshLoop)
    cacheRefreshThread.start()

# run app
if __name__ == '__main__':
    startCacheThread()
    app.run(host='0.0.0.0', port=1337)
else:
    startCacheThread()
    # gunicorn runs the app
