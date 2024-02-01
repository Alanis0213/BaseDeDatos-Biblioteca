from sql_librerias import conectar_db,desconectar_db
from prettytable import PrettyTable
from tkinter import messagebox
from tkinter import*
from tkinter import ttk

def registrar_venta():
    while True:
        print("===========================================")
        print("Para salir, ingrese '0'")
        id_cliente = int(input("Ingrese el código del cliente: "))
        conexion, cursor = conectar_db("biblioteca.db")
        if id_cliente == 0:
            break
        sentencia = """SELECT id_cliente
                        FROM clientes"""
        cursor.execute(sentencia)
        clientes = cursor.fetchall()
        cliente_encontrado = False
        for cliente in clientes:
            if cliente[0] == id_cliente:
                cliente_encontrado = True
                break
        if not cliente_encontrado:
            print("El cliente no existe.")
            desconectar_db(conexion, cursor)
            continue
        while True:
            codigo_libro = int(input("Ingrese el código del libro: "))
            sentencia = """SELECT id_libros
                            FROM libros"""
            cursor.execute(sentencia)
            libros = cursor.fetchall()
            libro_encontrado = False
            for libro in libros:
                if libro[0] == codigo_libro:
                    libro_encontrado = True
                    break
            if not libro_encontrado:
                print("El libro no existe.")
            else:
                break
        while True:
            cantidad = int(input("Ingrese la cantidad vendida: "))
            if cantidad <= 0:
                print("Ingrese una cantidad válida.")
            else:
                break
        sentencia = """SELECT unidades, precio
                        FROM libros
                        WHERE id_libros = ?"""
        cursor.execute(sentencia, (codigo_libro,))
        libro = cursor.fetchone()
        if libro is None:
            print("El libro no existe.")
        elif cantidad > libro[0]:
            print("No hay suficientes unidades disponibles.")
        else:
            nuevo_codigo_venta = obtener_ultimo_codigo_venta() + 5
            valor_venta = cantidad * libro[1]
            nuevas_unidades = libro[0] - cantidad

            sentencia = """INSERT INTO Ventas (codigo_venta, id_cliente, id_libro, cantidad, valor_venta)
                            VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sentencia, (nuevo_codigo_venta, id_cliente, codigo_libro, cantidad, valor_venta))
            conexion.commit()

            sentencia = """UPDATE libros
                            SET unidades = ?
                            WHERE id_libros = ?"""
            cursor.execute(sentencia, (nuevas_unidades, codigo_libro))
            conexion.commit()
            
            print("Venta registrada exitosamente.")
            print(f"Código de venta: V-{nuevo_codigo_venta}")
            desconectar_db(conexion, cursor)

def obtener_ultimo_codigo_venta():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT MAX(codigo_venta)
                    FROM Ventas"""
    cursor.execute(sentencia)
    ultimo_codigo_venta = cursor.fetchone()[0]
    desconectar_db(conexion, cursor)
    if ultimo_codigo_venta is not None:
        return ultimo_codigo_venta
    return 0

def mostrar_ventas():
    print("==== Lista de ventas realizadas ====")
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                    FROM Ventas"""
    cursor.execute(sentencia)
    ventas = cursor.fetchall()
    tabla_ventas = PrettyTable(("Código de venta", "Código de cliente", "Código de libro", "Cantidad", "Valor de venta"))
    for venta in ventas:
        tabla_ventas.add_row(venta)
    print(tabla_ventas)
    desconectar_db(conexion, cursor)
    print("======================================")

def buscar_venta():
    while True:
        print("Para salir, ingrese '0'")
        codigo_venta = int(input("Ingrese el código de la venta a buscar: "))
        
        if codigo_venta == 0:
            break
        
        conexion, cursor = conectar_db("biblioteca.db")
        sentencia = """SELECT *
                        FROM Ventas
                        WHERE codigo_venta = ?"""
        cursor.execute(sentencia, (codigo_venta,))
        venta = cursor.fetchone()

        if venta is not None:
            print("================================")
            print(f"Código de venta: V-{venta[0]}, Código de cliente: {venta[1]}, Código de libro: {venta[2]}, Cantidad vendida: {venta[3]}, Valor de venta: {venta[4]}")
            print("=================================")
        else:
            print("======================================")
            print("La venta no fue encontrada.")

        desconectar_db(conexion, cursor)


        print("No se encontró ninguna venta con ese código.")

def eliminar_venta(codigo_venta):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                    FROM Ventas
                    WHERE codigo_venta = ?"""
    cursor.execute(sentencia, (codigo_venta,))
    venta = cursor.fetchone()

    if venta is not None:
        sentencia = """DELETE FROM Ventas
                        WHERE codigo_venta = ?"""
        cursor.execute(sentencia, (codigo_venta,))
        conexion.commit()
        print("La venta se eliminó correctamente.")
        messagebox.showinfo("Éxito", "La venta se eliminó correctamente.")
        
        sentencia = """SELECT unidades
                        FROM libros
                        WHERE id_libros = ?"""
        cursor.execute(sentencia, (venta[2],))
        
        unidades_libro = cursor.fetchone()[0]
        '''
        nuevas_unidades = unidades_libro + venta[3]
        sentencia = """UPDATE libros
                        SET unidades = ?
                        WHERE id_libros = ?"""
        cursor.execute(sentencia, (nuevas_unidades, venta[2]))
        conexion.commit()'''
    else:
        print("No se encontró ninguna venta con ese código.")

    desconectar_db(conexion, cursor)

def obtener_unidades_libro(id_libros):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT unidades
                   FROM libros
                   WHERE id_libros = ?"""
    cursor.execute(sentencia, (id_libros,))
    resultado = cursor.fetchone()
    desconectar_db(conexion, cursor)
    if resultado:
        return resultado[0]
    else:
        return 0

def obtener_precio_libro(id_libros):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT precio
                   FROM libros
                   WHERE id_libros = ?"""
    cursor.execute(sentencia, (id_libros,))
    resultado = cursor.fetchone()
    desconectar_db(conexion, cursor)
    if resultado:
        return resultado[0]
    else:
        return 0

def utilizar_unidades_libro(id_libros, unidades_utilizadas):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """UPDATE libros
                   SET unidades = ?
                   WHERE id_libros = ?"""
    cursor.execute(sentencia, (unidades_utilizadas, id_libros))
    conexion.commit()
    desconectar_db(conexion, cursor)

def obtener_ventas():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                   FROM ventas"""
    cursor.execute(sentencia)
    ventas = cursor.fetchall()
    desconectar_db(conexion, cursor)
    return ventas
'''
def actualizar_venta(codigo_venta, nuevo_codigo_cliente, nuevo_id_libro, unidad, ventana_actualizar_venta):
    codigo_venta = int(codigo_venta)
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                   FROM ventas
                   WHERE codigo_venta = ?"""
    cursor.execute(sentencia, (codigo_venta,))
    venta = cursor.fetchone()

    if venta is not None:
        cantidad_anterior = venta[3]
        unidades_anteriores = obtener_unidades_libro(venta[2])
        precio_libro_anterior = obtener_precio_libro(venta[2])

        nuevo_codigo_cliente = nuevo_codigo_cliente.strip()
        if nuevo_codigo_cliente == "":
            nuevo_codigo_cliente = venta[1] # Mantener el mismo código de cliente

        nuevo_id_libro = nuevo_id_libro.strip()
        if nuevo_id_libro == "":
            nuevo_id_libro = venta[2] # Mantener el mismo código de libro

        if nuevo_id_libro != "":
            unidades_nuevo_libro = obtener_unidades_libro(nuevo_id_libro)

        nuevas_unidades = unidad.strip()
        if nuevas_unidades == "":
            nuevas_unidades = cantidad_anterior
            
        else:
            nuevas_unidades = int(nuevas_unidades)
            diferencia_unidades = nuevas_unidades - cantidad_anterior
            unidades_disponibles_nuevo = unidades_nuevo_libro

        # Restaurar unidades al libro original
        utilizar_unidades_libro(venta[2], unidades_anteriores + cantidad_anterior)
        
        utilizar_unidades_libro(nuevo_id_libro,unidades_disponibles_nuevo-nuevas_unidades)
        
        if nuevo_id_libro!= "":
            # Restar unidades del nuevo libro solo si el código del libro cambió
            utilizar_unidades_libro(nuevo_id_libro, unidades_disponibles_nuevo- nuevas_unidades)
            if venta[2] != nuevo_id_libro:
                if unidades_nuevo_libro >= nuevas_unidades:
                    utilizar_unidades_libro(nuevo_id_libro, unidades_nuevo_libro - nuevas_unidades)
                    #utilizar_unidades_libro(nuevo_id_libro,nuevas_unidades - unidades_anteriores)
                    #utilizar_unidades_libro(venta[2], unidades_anteriores + cantidad_anterior)
                else:
                    messagebox.showinfo("error", "No hay suficientes unidades disponibles para el nuevo libro. La venta no se actualizará.")
                    return
                        
        if nuevas_unidades != "":
            if venta[2] != nuevo_id_libro:
                if unidades_nuevo_libro >= diferencia_unidades:
                    utilizar_unidades_libro(nuevo_id_libro, unidades_nuevo_libro - diferencia_unidades)
                else:
                    messagebox.showinfo("error","No hay suficientes unidades disponibles para el nuevo libro. La venta no se actualizará.")
                    return

        if nuevo_id_libro != "":
            precio_libro_actualizado = obtener_precio_libro(nuevo_id_libro)
            valor_venta = precio_libro_actualizado * nuevas_unidades
        else:
            
            valor_venta = precio_libro_anterior * nuevas_unidades

        sentencia = """UPDATE ventas
                       SET id_cliente = ?, id_libro = ?, cantidad = ?, valor_venta = ?
                       WHERE codigo_venta = ?"""
        cursor.execute(sentencia, (nuevo_codigo_cliente, nuevo_id_libro, unidad, valor_venta, codigo_venta))
        conexion.commit()

        messagebox.showinfo("exito", "Venta actualizada correctamente.")

        # Mostrar la venta actualizada
        mensaje_venta = f"Código de venta: {codigo_venta}\n"
        mensaje_venta += f"Nuevo código de cliente: {nuevo_codigo_cliente}\n"
        mensaje_venta += f"Nuevo código de libro: {nuevo_id_libro}\n"
        mensaje_venta += f"Cantidad vendida: {nuevas_unidades}\n"
        mensaje_venta += f"Valor de la venta: {valor_venta}"
        ventana_actualizar_venta.text_widget.insert(END, mensaje_venta + "\n")
        ventana_actualizar_venta.text_widget.see(END)

    else:
        messagebox.showinfo("error", "El código de venta no se encuentra en la lista.")
    desconectar_db(conexion, cursor)'''


def actualizar_venta(codigo_venta, nuevo_codigo_cliente, nuevo_id_libro, nuevas_unidades, ventana_actualizar_venta):
    codigo_venta = int(codigo_venta)
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                    FROM ventas
                    WHERE codigo_venta = ?"""
    cursor.execute(sentencia, (codigo_venta,))
    venta = cursor.fetchone()

    if venta is not None:
        cantidad_anterior = venta[3]
        unidades_anteriores = obtener_unidades_libro(venta[2])
        precio_libro_anterior = obtener_precio_libro(venta[2])

        nuevo_codigo_cliente = nuevo_codigo_cliente.strip()
        if nuevo_codigo_cliente == "":
            nuevo_codigo_cliente = venta[1]  # Mantener el mismo código de cliente

        nuevo_id_libro = nuevo_id_libro.strip()
        if nuevo_id_libro == "":
            nuevo_id_libro = venta[2]  # Mantener el mismo código de libro

        if nuevo_id_libro != "":
            unidades_nuevo_libro = obtener_unidades_libro(nuevo_id_libro)

        nuevas_unidades = nuevas_unidades.strip()
        if nuevas_unidades == "":
            nuevas_unidades = cantidad_anterior
        else:
            nuevas_unidades = int(nuevas_unidades)

        diferencia_unidades = nuevas_unidades - cantidad_anterior

        unidades_disponibles_original = unidades_anteriores + cantidad_anterior
        unidades_disponibles_nuevo = unidades_nuevo_libro

        if nuevo_id_libro != venta[2]:
            # El código del libro ha sido cambiado
            if unidades_nuevo_libro < nuevas_unidades:
                messagebox.showinfo(
                    "error", "No hay suficientes unidades disponibles para el nuevo libro. La venta no se actualizará."
                )
                desconectar_db(conexion, cursor)
                return
            else:
                 # Restaurar unidades al libro original
                utilizar_unidades_libro(venta[2], unidades_disponibles_original +  unidades_disponibles_nuevo)
                # Restar unidades del nuevo libro
                utilizar_unidades_libro(nuevo_id_libro, unidades_disponibles_nuevo - nuevas_unidades)
       
            # El código del libro no ha cambiado
        if unidades_disponibles_original - diferencia_unidades < 0:
                messagebox.showinfo("error","No hay suficientes unidades disponibles para el libro original. La venta no se actualizará.")
                desconectar_db(conexion, cursor)
                return
        else:
            # Actualizar unidades del libro original
                utilizar_unidades_libro(venta[2], unidades_disponibles_original - nuevas_unidades)

        if nuevo_id_libro != "":
            precio_libro_actualizado = obtener_precio_libro(nuevo_id_libro)
            valor_venta = precio_libro_actualizado * nuevas_unidades
        else:
            valor_venta = precio_libro_anterior * nuevas_unidades

        sentencia = """UPDATE ventas
                        SET id_cliente = ?, id_libro = ?, cantidad = ?, valor_venta = ?
                        WHERE codigo_venta = ?"""
        cursor.execute(
            sentencia,
            (nuevo_codigo_cliente, nuevo_id_libro, nuevas_unidades, valor_venta, codigo_venta),
        )
        conexion.commit()

        messagebox.showinfo("exito", "Venta actualizada correctamente.")

        # Mostrar la venta actualizada
        mensaje_venta = f"Código de venta: {codigo_venta}\n"
        mensaje_venta += f"Nuevo código de cliente: {nuevo_codigo_cliente}\n"
        mensaje_venta += f"Nuevo código de libro: {nuevo_id_libro}\n"
        mensaje_venta += f"Cantidad vendida: {nuevas_unidades}\n"
        mensaje_venta += f"Valor de la venta: {valor_venta}"
        ventana_actualizar_venta.text_widget.insert(END, mensaje_venta + "\n")
        ventana_actualizar_venta.text_widget.see(END)

    else:
        messagebox.showinfo("error", "El código de venta no se encuentra en la lista.")
    desconectar_db(conexion, cursor)

        

'''def obtener_unidades_libro(codigo_libro):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT unidades
                    FROM libros
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (codigo_libro,))
    unidades_libro = cursor.fetchone()
    desconectar_db(conexion, cursor)
    if unidades_libro is not None:
        return unidades_libro[0]
    return 0

def obtener_precio_libro(codigo_libro):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT precio
                    FROM libros
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (codigo_libro,))
    precio_libro = cursor.fetchone()
    desconectar_db(conexion, cursor)
    if precio_libro is not None:
        return precio_libro[0]
    return 0

def utilizar_unidades_libro(codigo_libro, nuevas_unidades):
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """UPDATE libros
                    SET unidades = ?
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (nuevas_unidades, codigo_libro))
    conexion.commit()
    desconectar_db(conexion, cursor)

def obtener_unidades_libro(codigo_libro):
    conexion,cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT unidades
                    FROM libros
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (codigo_libro,))
    unidades_libro = cursor.fetchone()
    conexion.close()

    if unidades_libro is not None:
        return unidades_libro[0]
    return 0

def obtener_precio_libro(codigo_libro):
    conexion,cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT precio
                    FROM libros
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (codigo_libro,))
    precio_libro = cursor.fetchone()
    conexion.close()

    if precio_libro is not None:
        return precio_libro[0]
    return 0

def utilizar_unidades_libro(codigo_libro, nuevas_unidades):
    conexion,cursor= conectar_db("biblioteca.db")
    sentencia = """UPDATE libros
                    SET unidades = ?
                    WHERE id_libros = ?"""
    cursor.execute(sentencia, (nuevas_unidades, codigo_libro))
    conexion.commit()
    conexion.close()
'''