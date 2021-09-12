How to setup:

Standalone:
    -  For first run install dependecies:
        Execute in terminal: pip3 install -r requirements.txt

    - For running app:
        Execute in terminal: uvicorn main:app
    - Use API!

Containerized:
    - docker-compose up
    - Use API!


How to use:

send HTTP request to http://127.0.0.1:8000/api?serial=XXX&policy=XXXXXXXXXX
or if application containerized check open container port


For using proxy:
    Add proxys list to proxys.txt in format "http://user:pass@proxy_address:proxy_port", one proxy at line.