#!/usr/bin/env python3

# Imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import unittest
import sys

# Settings
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8080
DEBUG = True
ENCODING = 'UTF-8'


# List implementation of set
class BasicSet:

    def __init__(self, seed=None):
        if seed and isinstance(seed, int):
            self.set = [seed]
        else:
            self.set = []

    def __str__(self):
        return f'[{",".join(str(item) for item in self.set)}]'

    def _list(self):
        return list(str(item) for item in self.set)

    def AddItem(self, value):
        found = False
        for element in self.set:
            if element == value:
                found = True
                break
        if found:
            return False
        else:
            self.set.append(value)
            return True

    def RemoveItem(self, value):
        found = False
        for element in self.set:
            if element == value:
                found = True
                break
        if found:
            self.set.remove(value)
            return True
        else:
            return False

    def HasItem(self, value):

        found = False
        for element in self.set:
            if element == value:
                found = True
                break
        if found:
            return True
        else:
            return False


# Handler that bridges HTTP server with backend
class Handler():

    def __init__(self):
        self.set = BasicSet()

    def add_item(self, value):
        return self.set.AddItem(value)

    def remove_item(self, value):
        return self.set.RemoveItem(value)

    def has_item(self, value):
        return self.set.HasItem(value)


# HTTP handling functions
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests in a separate thread """


class HTTPServer(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            self.response_handler()
        except Exception as e:
            self.response_code(500)
            raise

    def do_GET(self):
        try:
            self.response_handler()
        except Exception as e:
            self.response_code(500)
            raise

    # Generic handler for HTTP methods
    def response_handler(self):

        PATH = str(self.path).lower()

        # Status endpoint
        if 'status' in PATH:
            response = handler.set
            self.response_data(response)

        # AddItem endpoint
        elif 'add' in PATH:

            path_data = None
            try:
                path_data = PATH.split('/')[-1]
                request_data = int(path_data)
            except ValueError as e:
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    request_data = int(post_data)
                except (TypeError, ValueError) as e:
                    self.response_code(406)
                    return

            result = handler.add_item(request_data)
            if result:
                self.response_data('"ok"', 201)
            else:
                self.response_data()

        # RemoveItem endpoint
        elif 'remove' in PATH:

            path_data = None
            try:
                path_data = PATH.split('/')[-1]
                request_data = int(path_data)
            except ValueError as e:
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    request_data = int(post_data)
                except (TypeError, ValueError) as e:
                    self.response_code(406)
                    return

            result = handler.remove_item(request_data)
            if result:
                self.response_data()
            else:
                self.response_data('"nonexistent"', 400)

        # HasItem endpoint
        elif 'has' in PATH:

            path_data = None
            try:
                path_data = PATH.split('/')[-1]
                request_data = int(path_data)
            except ValueError as e:
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    request_data = int(post_data)
                except (TypeError, ValueError) as e:
                    self.response_code(406)
                    return

            result = handler.has_item(request_data)
            self.response_data(f'"{result}"')

        # Unmatched endpoint
        else:
            self.response_code(404)
            return

    # Return response with data in JSON format
    def response_data(self, value='"ok"', code=200):

        # Craft response
        response = f'{{"result":{value}}}'
        response_length = len(response)

        # Response headers
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', response_length)
        self.end_headers()

        # Send response
        self.wfile.write(bytes(response, encoding=ENCODING))
        return

    # Return response code with no data, usually for errors
    def response_code(self, value):
        self.send_response(int(value))
        self.end_headers()


# Unit tests
class UnitTests(unittest.TestCase):

    # Positive Tests
    def test_set_has(self):
        test_set = BasicSet(1)
        self.assertTrue(test_set.HasItem(1))
        del(test_set)

    def test_set_add(self):
        test_set = BasicSet()
        test_set.AddItem(1)
        self.assertTrue(test_set.HasItem(1))
        del(test_set)

    def test_set_remove(self):
        test_set = BasicSet()
        test_set.AddItem(1)
        test_set.RemoveItem(1)
        self.assertFalse(test_set.HasItem(1))
        del(test_set)

    # Negative Tests
    def test_set_has_negative(self):
        test_set = BasicSet()
        self.assertFalse(test_set.HasItem(2))
        del(test_set)

    def test_set_add_negative(self):
        test_set = BasicSet()
        test_set.AddItem(1)
        self.assertFalse(test_set.AddItem(1))
        del(test_set)

    def test_set_remove_negative(self):
        test_set = BasicSet()
        self.assertFalse(test_set.RemoveItem(1))
        del(test_set)

    def test_set_unique(self):
        test_set = BasicSet()
        test_set.AddItem(1)
        test_set.AddItem(1)
        test_set.AddItem(2)
        self.assertTrue(len(test_set._list()) == 2)
        del(test_set)


# HTTP server thread
def httpLaunch():
    httpd = ThreadedHTTPServer((LISTEN_HOST, LISTEN_PORT), HTTPServer)
    print('Server started on', LISTEN_HOST + ':' + str(LISTEN_PORT))
    httpd.serve_forever()


# Main function
if __name__ == '__main__':

    # Init handler
    handler = Handler()

    # Run tests
    if 'test' in sys.argv:
        print('Starting Unit Tests')
        unittest.main(argv=[''])

    # Launch application
    else:
        # Create handler and start HTTP server
        httpThread = threading.Thread(target=httpLaunch, args=())
        httpThread.start()

