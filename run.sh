#!/bin/bash
activate () {
    . $PWD/.env/bin/activate
}
activate
cd src/api/
export FLASK_APP=api
export FLASK_ENV=development
python3 api.py