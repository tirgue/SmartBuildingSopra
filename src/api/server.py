from flask import *
import json
import os
import sys
import RPi.GPIO as GPIO
import platform


from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def getConfigFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../config/' + 'config.json') as file:
        config = json.load(file)
        return config

def writeConfigFile(outfile):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../config/' + 'config.json','w') as file:
        config = json.dump(outfile,file,ensure_ascii=False, indent=2)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def resource_not_found(e):
    return jsonify(error=str(e)), 500

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400

@app.route("/api/config", methods=['GET'])
def getConfig():
    config = getConfigFile()
    return jsonify(config)

@app.route("/api/config", methods=['POST'])
def postConfig():
    try : 
        writeConfigFile(request.get_json())
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except BadRequest:
        abort(400,description="Le JSON est mal formaté")
    except Exception as e:
        abort(500,description="Une erreur est survenue")
 


@app.route("/api/config/<name>",methods=['GET'])
def getConfigByName(name):
    try : 
        config = getConfigFile()
        sensor = config['Capteurs'][name]
        return jsonify(sensor)
    except KeyError : 
        abort(404,description="La ressource recherchée n'existe pas")
    except Exception : 
        abort(500,description="Une erreur est survenue")

@app.route("/api/config/<name>", methods=['POST'])
def postConfigByName(name):
    try :
        config = getConfigFile()
        config['Capteurs'][name] = request.get_json()
        writeConfigFile(config)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except BadRequest:
        abort(400,description="Le JSON est mal formaté")
    except Exception as e:
        print(str(e))
        abort(500,description="Une erreur est survenue")
 
@app.route("/api/info",methods=['GET'])
def getInfo():
    try : 
        return jsonify({
            "Python Version" : sys.version.split('\n'),
            #"Linux Distribution" :  platform.linux_distribution(),
            "System name" : platform.system(),
            "Release version" : platform.release(),
            "Architecture" : platform.architecture(),
            "Machine" : platform.machine(),
            "Platform" : platform.platform(),
            "Uname": platform.uname(),
            "Version" : platform.version(),
        })
    except Exception as e : 
        abort(500,description="Une erreur est survenue")


@app.route("/api/status", methods=['GET'])
def getStatus():
    try:
        GPIO.setmode(GPIO.BCM)
        state = GPIO.input(13)
        print(state)
        return "ok"
    except Exception as e : 
        print(str(e))
        abort(500,description="Une erreur est survenue")