import ssl
import json

import websocket
import bitstamp.client

import credencias


def cliente():
    return bitstamp.client.Trading(username=credencias.USERNAME, key=credencias.KEY, secret=credencias.SECRET)

def vender(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


def comprar(quantidade):
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)


def ao_abrir(ws):
    print("Abriu a conexão")

    json_subscribe = """
    {
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}  
"""
    ws.send(json_subscribe)

def ao_fechar(ws):

    print("Fechou a conexão")


def erro(ws, erro):
    print("Deu Erro")
    print(erro)


def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)

    if price > 10745:
        vender()
    elif price < 10715:
        comprar()
    else:
        print("Vamos aguardar")




if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=erro)


    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
