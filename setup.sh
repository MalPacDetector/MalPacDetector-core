#!/bin/bash

echo 'Setuping the python environment and dependencies...'
python3 -m venv env && \
source env/bin/activate && \
pip3 install -r training/requirements.txt
deactivate
echo 'Setuping the python environment and dependencies done!'

echo 'Setuping the node environment and dependencies...'
cd feature-extract && \
npm install && \
npm run compile && \
echo 'Setuping the node environment and dependencies done!'