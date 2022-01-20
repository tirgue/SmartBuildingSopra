from flask import *
import json
import os
import sys
import RPi.GPIO as GPIO
import platform
from threading import Thread
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
    try : 
        config = getConfigFile()
        return jsonify(config)
    except Exception as e:
        print(str(e))
        abort(500,description="Une erreur est survenue") 

@app.route("/api/config", methods=['POST'])
def postConfig():
    try : 
        writeConfigFile(request.get_json())
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except BadRequest:
        abort(400,description="Le JSON est mal formaté")
    except Exception as e:
        print(str(e))
        abort(500,description="Une erreur est survenue")
 


@app.route("/api/config/sensor/<name>",methods=['GET'])
def getConfigByName(name):
    try : 
        config = getConfigFile()
        sensor = config['Capteurs'][name]
        return jsonify(sensor)
    except KeyError : 
        abort(404,description="La ressource recherchée n'existe pas")
    except Exception : 
        abort(500,description="Une erreur est survenue")

@app.route("/api/config/sensor", methods=['POST'])
def postConfigByName():
    try :
        config = getConfigFile()
        config['Capteurs'].update(request.get_json())
        writeConfigFile(config)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except BadRequest:
        abort(400,description="Le JSON est mal formaté")
    except Exception as e:
        print(str(e))
        abort(500,description="Une erreur est survenue")

@app.route("/api/config/sensor/<name>", methods=['DELETE'])
def deleteConfigByName(name):
    try :
        config = getConfigFile()
        for key, value in list(config['Capteurs'].items()):
            if (key == name):
                del config['Capteurs'][name]
                
        writeConfigFile(config)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
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

if __name__ == "__main__":
    

    try :
        app.run()
    except Exception as e :
        print(str(e))


