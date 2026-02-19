import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # si tienes contraseña, ponla
    database="enigh"
)

cursor = conexion.cursor()
