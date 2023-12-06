FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-2023-06-05

WORKDIR /project
RUN apt-get update && apt-get upgrade -y
RUN apt-get install jq -y
COPY ./Pipfile.lock /project
ENV PYTHONPATH "${PYTHONPATH}:/project/"
RUN jq -r '.default | to_entries[] | .key + .value.version' Pipfile.lock > requirements.txt
RUN pip install -r requirements.txt

COPY [".", "./"]
