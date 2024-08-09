import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="logging_db",
        user="postgres",
        password="123456",
        host="localhost",
        port="5433"
    )

def guardar_log(log_data):
    conn = conectar()  
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO logs (fecha_hora, nombre_servicio, nivel_severidad, mensaje, received_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        log_data["fecha_hora"],
        log_data["nombre_servicio"],
        log_data["nivel_severidad"],
        log_data["mensaje"],
        log_data["received_at"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_logs():
    conn = conectar()  
    cursor = conn.cursor()
    select_query = "SELECT * FROM logs ORDER BY fecha_hora DESC"
    cursor.execute(select_query)
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return logs
