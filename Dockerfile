FROM python:3.8-slim
RUN pip install PyGithub requests
COPY entrypoint.py /entrypoint.py
ENTRYPOINT python /entrypoint.py
