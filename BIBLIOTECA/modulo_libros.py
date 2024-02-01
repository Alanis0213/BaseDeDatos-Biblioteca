from sql_librerias import conectar_db,desconectar_db
from prettytable import PrettyTable
from tkinter import messagebox
def ingresar_libros(libros):
    while True:
        conexion, cursor = conectar_db("biblioteca.db")
        print("===============================================")
        print("Para salir, ingrese '0' en ambos campos.")
        codigo = input("Ingrese el código del libro (ISBN): ")
        if codigo == '0':
            break

        cursor.execute("SELECT id_libros FROM libros WHERE id_libros = ?", (codigo,))
        resultado = cursor.fetchone()
        if resultado is not None:
            print("================================================")
            print()
            print("El código ISBN ya ha sido registrado. Intente nuevamente.")
            print()
            print("================================================")
            continue

        nombre = input("Ingrese el título del libro: ")
        if nombre == '0':
            break
        precio = float(input("Ingrese el precio del libro: "))
        if precio == 0:
            break
        unidades = int(input("Ingrese la cantidad de unidades disponibles: "))
        if unidades == 0:
            break

        libros.append([codigo, nombre, precio, unidades])
        sentencia = "INSERT INTO libros(id_libros, nombre, precio, unidades) VALUES (?, ?, ?, ?)"
        cursor.execute(sentencia, (codigo, nombre, precio, unidades))
        conexion.commit()
        desconectar_db(conexion, cursor)
        print("Libro registrado exitosamente.")
        
def lista_libros():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                   FROM libros"""
    cursor.execute(sentencia)
    libros = cursor.fetchall()
    desconectar_db(conexion, cursor)
    return libros


def eliminar_libro(codigo):
    conexion, cursor = conectar_db("biblioteca.db")

    sentencia = """SELECT id_libro
                    FROM Ventas
                    WHERE id_libro = ?"""
    cursor.execute(sentencia, (codigo,))
    venta = cursor.fetchone()

    if venta is not None:
        messagebox.showinfo("Error", "El libro está registrado en una venta. No se puede eliminar.")
        desconectar_db(conexion, cursor)
        return
    sentencia = """DELETE FROM libros
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (codigo,))
    conexion.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Éxito", "Libro borrado exitosamente.")
    else:
        messagebox.showinfo("Error", "No se encontró el libro.")

    desconectar_db(conexion, cursor)

def buscar_libro(libros):
    while True:
        print("=========================================")
        print("Para salir, ingrese '0'")
        codigo = input("Ingrese el código del libro a buscar: ")
        if codigo == '0':
            break
        conexion, cursor = conectar_db("biblioteca.db")
        print("=========================================")
        sentencia = """SELECT *
                    FROM libros
                    WHERE id_libros = ?
        """
        cursor.execute(sentencia, (codigo,))
        libro = cursor.fetchone()
        if libro:
            print(f"Libro encontrado: ISBN: {libro[0]}, Título: {libro[1]}, Precio: {libro[2]}, Unidades: {libro[3]}")
        else:
            print("Libro no encontrado.")
        desconectar_db(conexion, cursor)

def actualizar_libro(codigo, nuevo_titulo, nuevo_precio, nuevas_unidades):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                FROM libros
                WHERE id_libros = ?
    """
    cursor.execute(sentencia, (codigo,))
    libro = cursor.fetchone()
    if libro:
        print("=========================================")
        print(f"Libro encontrado: Código: {libro[0]}, Título: {libro[1]}, Precio: {libro[2]}, Unidades: {libro[3]}")
        print("=========================================")

        # Create a list and assign the updated values
        nuevo_libro = list(libro)
        if nuevo_titulo.strip():
            nuevo_libro[1] = nuevo_titulo
        if nuevo_precio.strip():
            nuevo_libro[2] = float(nuevo_precio)
        if nuevas_unidades.strip():
            nuevo_libro[3] = int(nuevas_unidades)

        # Convert the list back to a tuple
        nuevo_libro = tuple(nuevo_libro)

        sentencia = """UPDATE libros
            SET nombre = ?, precio = ?, unidades = ?
            WHERE id_libros = ?
        """
        cursor.execute(sentencia, (nuevo_libro[1], nuevo_libro[2], nuevo_libro[3], codigo))
        conexion.commit()
        desconectar_db(conexion, cursor)
        return True
    else:
        desconectar_db(conexion, cursor)
        return False

