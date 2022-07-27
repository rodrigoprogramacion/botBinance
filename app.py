
import requests
import config
from flask import Flask, request, json, jsonify
from binance.cm_futures import CMFutures
from datetime import datetime




def ObtenerFechaServer() -> int:
    endpoint= "https://testnet.binancefuture.com/fapi/v1/time"
    r = requests.get(endpoint)
    resp = r.json()
    return resp["serverTime"]

def log(texto:str):
    f = open("ordenes.log", "a")
    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -> " + texto + "\n")
    f.close()

def OrdenMarket(simbolo:str, cantidad:float, side:str) -> dict:
        endPoint = "https://testnet.binancefuture.com/fapi/v1/order"
        parametros = "timestamp="+str(ObtenerFechaServer())
        parametros += "&symbol="+simbolo.upper()
        parametros +="&side="+side.upper()
        parametros +="&type=MARKET"
        parametros +="&quantity=" + str(cantidad)

    

        r=requests.post(endPoint, params=parametros)
        return r.json()

app = Flask(__name__)

cm_futures_client = CMFutures (key=config.API_KEY, secret=config.SECRET_KEY)

def orden(side, quantity, symbol):
    try:
        print(f"Enviando orden... {side} - {quantity} - {symbol}")
        orden = cm_futures_client.new_order(symbol=symbol, side=side, type="MARKET", quantity=quantity, timestamp=str(ObtenerFechaServer()))
        print(orden)
    except Exception as e:
        print("a ocurrido un error - {}".format(e))
        return False
    return True



@app.route("/alerta", methods=['POST'])

def alerta():
    
    data = json.loads(request.data)    
    side = data['strategy']['order_action'].upper()                                       
    quantity = data['strategy']['order_contracts']
    symbol = data['ticker'].upper()
    passphrase= data['passphrase']
    enviar_orden=orden(side,quantity,symbol)
    

    return {
            
            "Conexion":"Exitosa",
            "Mensaje": data,
           
            }



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
