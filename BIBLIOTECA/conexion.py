import sqlite3


try:
    conexion=sqlite3.Connection("biblioteca.db")
    print("base de datos abierta correctamente")
    conexion.close()
except sqlite3.OperationalError as error :
    print('error al abrir la base de datos:',  error)


