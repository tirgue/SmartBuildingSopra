#!/bin/bash
activate () {
    . $PWD/.env/bin/activate
}
activate
cd src/api/
export FLASK_APP=server
export FLASK_ENV=development
flask run
