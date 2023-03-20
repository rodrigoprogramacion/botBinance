
import json
import requests
import config
from flask import Flask, request, render_template
from binance.cm_futures import CMFutures


app = Flask(__name__)

cm_futures_client = CMFutures (key=config.API_KEY, secret=config.SECRET_KEY)


def ObtenerFechaServer() -> int:
    endpoint= "https://testnet.binancefuture.com/fapi/v1/time"
    r = requests.get(endpoint)
    resp = r.json()
    return resp["serverTime"]


def orden(side, quantity, symbol, price):
    try:
        print(f"Enviando orden... {side} - {quantity} - {symbol} - {price}")
        orden = cm_futures_client.new_order(symbol=symbol, side=side, type="LIMIT", quantity=quantity, timestamp=str(ObtenerFechaServer()), price=price, timeInForce="GTC")
    except Exception as e:
        print("a ocurrido un error - {}".format(e))
        return False
    return orden


@app.route('/')

def bienvenida():
    return render_template('index.html')


@app.route("/alerta", methods=['POST'])

def alerta():
    
    data = json.loads(request.data) 

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:

            return {
            "Codigo":"Error",
            "Mensaje":"Passphrase incorrecto"
            }

    print(data['ticker'])  
    print(data['bar'])

    side = data['strategy']['order_action'].upper()                                       
    quantity = data['strategy']['order_contracts']
    symbol = data['ticker'].upper()
    precio=data['strategy']['order_price']
    price=format(precio,'.1f')
   
    respuesta=orden(side,quantity,symbol,price)

    if respuesta:
        return {
            "Codigo":"200",
            "Mensaje:":"Orden ejecutada"
        }
    

    else:
        print("Orden Error")
        return {
            
            "Codigo":"500",
            "Mensaje": "Orden Failed",
           
         }



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
