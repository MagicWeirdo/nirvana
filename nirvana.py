from wsgiref.util import request_uri
from wsgiref.simple_server import make_server
from urllib.parse import urlparse


# HTTP Request
class HttpRequest:
    def __init__(self, method=None, url=None, headers=None, body=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def setMethod(self, method):
        self.method = method

    def getMethod(self):
        return self.method

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url

    def setHeader(self, key, value):
        if self.headers == None:
            self.headers = dict()

        self.headers[key] = value

    def getHeader(self, key):
        if self.headers == None:
            return None
        else:
            return self.headers[key]

    def setHeaders(self, headers):
        if self.headers == None:
            self.headers = dict()

        for key in headers.keys():
            self.headers[key] = headers[key]

    def getHeaders(self):
        return self.headers

    def setBody(self, data):
        self.body = data

    def getBody(self):
        return self.body


# HTTP Response
class HttpResponse:
    def __init__(self, status=None, headers=None, body=None):
        self.status = status
        self.headers = headers
        self.body = body

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setHeader(self, key, value):
        if self.headers == None:
            self.headers = []

        self.headers[key] = value

    def getHeader(self, key):
        if self.headers == None:
            return None
        else:
            return self.headers[key]

    def setHeaders(self, headers):
        if self.headers == None:
            self.headers = dict()

        for key in headers.keys():
            self.headers[key] = headers[key]

    def getHeaders(self):
        headers = []
        for key in self.headers.keys():
            headers.append((key, self.headers[key]))

        return headers

    def setBody(self, data):
        self.body = data

    def getBody(self):
        return self.body


# Nirvana Application
class App:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.actions = []

    def get(self, path, callback):
        self.actions.append({
            'method': 'GET',
            'path': path,
            'callback': callback
        })

    def delete(self, path, callback):
        self.actions.append({
            'method': 'DELETE',
            'path': path,
            'callback': callback
        })

    def post(self, path, callback):
        self.actions.append({
            'method': 'POST',
            'path': path,
            'callback': callback
        })

    def put(self, path, callback):
        self.actions.append({
            'method': 'PUT',
            'path': path,
            'callback': callback
        })

    def patch(self, path, callback):
        self.actions.append({
            'method': 'PATCH',
            'path': path,
            'callback': callback
        })

    def handle(self, request):
        callback = self.dispatch(request)

        if callback != None:
            return callback(request)
        else:
            response = HttpResponse()
            response.setStatus('404 Not Found')
            response.setHeaders({})
            response.setBody(bytes('', 'utf8'))
            return response


    def dispatch(self, request):
        method = request.getMethod()
        path = urlparse(request.getUrl()).path

        for action in self.actions:
            if(action['method'] == method and action['path'] == path):
                return action['callback']

        return None


    def run(self):
        # WSGI Application
        def application(environ, start_response):
            method = environ['REQUEST_METHOD']
            url = request_uri(environ)

            headers = dict()
            for key in environ.keys():
                if key.startswith('HTTP_'):
                    headers[key[5:]] = environ[key]

            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0

            request_body = environ['wsgi.input'].read(request_body_size)

            request = HttpRequest(method, url, headers, request_body)
            response = self.handle(request)

            start_response(response.getStatus(), response.getHeaders())

            return [response.getBody()]

        print('Server running at %s:%s' % (self.host, self.port))

        httpd = make_server(self.host, self.port, application)
        httpd.serve_forever()
