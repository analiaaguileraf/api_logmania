from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from database import guardar_log, obtener_logs
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Tokens validos para autenticar los servicios de los clientes 1 y 2
tokens_validos = ["mi_token_unico", "token_cliente_1", "token_cliente_2"]

@app.post("/logs")
async def recibir_logs(request: Request):
    token = request.headers.get("Authorization")
    if not token or token.split()[1] not in tokens_validos:
        raise HTTPException(status_code=401, detail="Token inválido")

    log_data = await request.json()
    log_data["received_at"] = datetime.now().isoformat()
    guardar_log(log_data)

    return {"mensaje": "Log recibido y almacenado correctamente"}

# Endpoint para el archivo HTML
@app.get("/", response_class=HTMLResponse)
async def leer_index():
    with open("index.html", "r") as file:
        return file.read()

# Endpoint para obtener logs con filtros
@app.get("/logs")
async def obtener_logs_api(
    fecha_hora_inicio: datetime = Query(None, description="Fecha de inicio del evento"),
    fecha_hora_fin: datetime = Query(None, description="Fecha de fin del evento"),
    received_at_inicio: datetime = Query(None, description="Fecha de inicio de recepcion"),
    received_at_fin: datetime = Query(None, description="Fecha de fin de recepcion")
):
    logs = obtener_logs()
    
    # Filtros
    if fecha_hora_inicio:
        logs = [log for log in logs if log[1] >= fecha_hora_inicio]
    if fecha_hora_fin:
        logs = [log for log in logs if log[1] <= fecha_hora_fin]
    if received_at_inicio:
        logs = [log for log in logs if log[5] >= received_at_inicio]
    if received_at_fin:
        logs = [log for log in logs if log[5] <= received_at_fin]

    return {"logs": logs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
