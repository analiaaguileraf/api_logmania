import requests
from datetime import datetime

def enviar_log():
    url = "http://127.0.0.1:8000/logs"
    headers = {
        "Authorization": "Bearer token_cliente_2",
        "Content-Type": "application/json"
    }
    log_data = {
        "fecha_hora": datetime.now().isoformat(),
        "nombre_servicio": "Servicio_cliente2",
        "nivel_severidad": "Error",
        "mensaje": "Mensaje de prueba xd"
    }
    response = requests.post(url, headers=headers, json=log_data)
    print(response.json())

if __name__ == "__main__":
    enviar_log()
