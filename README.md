# CMFPythonMockServer

This collection of python scripts is for mocking request/response for Android, iOS, API.
You can use it on aws since it is deployed but for more verbosity you can run it locally.
There are few scripts which you can run:

1. run_listener.py  basic API to talk to server
2. run_socket_listener.py opens a socket and acts as API
3. run_client_socket_server.py runs terminal app where you can behave as client side

How to run:

1. create a environments folder if you haven't got one say `myenv`
2. create virtual environment `virtualenv -p python3 myenv`
3. source myenv/bin/activate
4. pip install -r requirements.txt
5. python3 run_listener.py
