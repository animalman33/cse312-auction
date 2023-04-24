
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:slim

EXPOSE 8080

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt


WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# RUN chown appuser /wait
# USER appuser
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# During debugginG, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD /wait && python -u main.py
