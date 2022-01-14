#!/bin/bash
activate () {
    . $PWD/.env/bin/activate
}
activate
cd src/
export FLASK_APP=api
export FLASK_ENV=development
python3 api/api.py & python3 deploy.py &