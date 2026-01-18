FROM jenkins/jenkins:lts

USER root

# Install Python3 and pip3
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl git && \
    rm -rf /var/lib/apt/lists/*

# Install commonly used Python packages
RUN pip3 install --break-system-packages --no-cache-dir \
    pytest \
    pytest-html \
    pytest-json-report \
    requests \
    selenium \
    jsonschema

USER jenkins
