from sql_librerias import conectar_db, desconectar_db
from prettytable import PrettyTable
from tkinter import messagebox

def ingresar_cliente(id_cliente, nombre):
    conexion, cursor = conectar_db("biblioteca.db")

    cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))
    resultado = cursor.fetchone()
    if resultado is not None:
        messagebox.showinfo("Error", "El código de cliente ya ha sido registrado.")
    else:
        lista_clientes = [id_cliente, nombre]
        sentencia = "INSERT INTO clientes(id_cliente, nombre) VALUES (?, ?)"
        cursor.execute(sentencia, lista_clientes)
        conexion.commit()
        desconectar_db(conexion, cursor)
        messagebox.showinfo("Éxito", "Cliente registrado exitosamente.")

def lista_clientes():
    conexion, cursor = conectar_db("biblioteca.db")

    sentencia = """SELECT *
                    FROM clientes
                """
    cursor.execute(sentencia)
    clientes = cursor.fetchall()

    desconectar_db(conexion, cursor)

    return clientes

def eliminar_cliente(codigo):
    conexion, cursor = conectar_db("biblioteca.db")

    sentencia = """SELECT id_cliente
                    FROM Ventas
                    WHERE id_cliente = ?"""
    cursor.execute(sentencia, (codigo,))
    venta = cursor.fetchone()
    
    if venta is not None:
        messagebox.showinfo("Error", "El cliente está registrado en una venta. No se puede eliminar.")
        desconectar_db(conexion, cursor)
        return
    sentencia = """DELETE FROM Clientes
                        WHERE id_cliente = ?"""
    cursor.execute(sentencia, (codigo,))
    conexion.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Éxito", "cliente borrado exitosamente.")
    else:
        messagebox.showinfo("Error", "No se encontró el cliente.")

def actualizar_cliente(codigo, nuevo_nombre):
    conexion, cursor = conectar_db("biblioteca.db")

    sentencia = """SELECT *
                    FROM clientes
                    WHERE id_cliente = ?
    """
    cursor.execute(sentencia, (codigo,))
    cliente = cursor.fetchone()
    if cliente:
        sentencia = """UPDATE clientes
                    SET nombre = ?
                    WHERE id_cliente = ?
        """
        cursor.execute(sentencia, (nuevo_nombre, codigo))
        conexion.commit()
        desconectar_db(conexion, cursor)
        messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")
    else:
        messagebox.showinfo("Error", "Cliente no encontrado.")

def buscar_cliente():
    while True:
        print("=======================================")
        print("Para salir, ingrese '0'")
        codigo = int(input("Ingrese el código del cliente a buscar: "))
        if codigo == 0:
            break
        conexion, cursor = conectar_db("biblioteca.db")
        print("=======================================")
        sentencia = """SELECT *
                    FROM clientes
                    WHERE id_cliente = ?
        """
        cursor.execute(sentencia, (codigo,))
        cliente = cursor.fetchone()
        if cliente:
            print("============================================")
            print(f"Cliente encontrado: Código: {cliente[0]}, Nombre: {cliente[1]}")
            print("============================================")
        else:
            print("Cliente no encontrado.")
        desconectar_db(conexion, cursor)