#!/bin/bash
cd $HOME/SmartBuildingSopra/src/
export FLASK_APP=api
export FLASK_ENV=development
python3 api/api.py & python3 deploy.py &
