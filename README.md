# instacover-integration-component

Basic REST server build in python using Fastapi library.

Usage:
Send and receive POST requests with Instacover Instacar API for creating car vehicle inspection sessions and receiving responses once those sessions are finished.

To develop on local use Pipenv:
 - set all environment variables in .env file
 - run 'pipenv install'
 - run 'pipenv shell'
 - start server with 'uvicorn --app-dir=rest_api main:app --reload' - to start with autoreload on changes