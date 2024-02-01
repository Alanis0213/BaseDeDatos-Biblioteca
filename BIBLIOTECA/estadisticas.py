from tkinter import *
from clientes import ventana_ingresar_cliente, ventana_listar_clientes, ventana_eliminar_cliente, ventana_actualizar_cliente, ventana_buscar_cliente
from libros import *
from ventas import *

def ventana_estadisticas_1():
    ventana = Toplevel()
    ventana.title("Estadísticas - Ventas totales por código de libro")
    ventana.geometry("300x200")

    def obtener_ventas_totales_por_codigo_libro():
        conexion, cursor = conectar_db("biblioteca.db")
        sentencia = """SELECT id_libro, SUM(cantidad) AS ventas_totales
                    FROM Ventas
                    GROUP BY id_libro"""
        cursor.execute(sentencia)
        ventas_totales_por_libro = cursor.fetchall()
        desconectar_db(conexion, cursor)

        resultados_text.delete("1.0", END)  # Borrar resultados anteriores

        if ventas_totales_por_libro:
            resultados_text.insert(END, "Ventas por libro:\n")
            for venta in ventas_totales_por_libro:
                codigo_libro = venta[0]
                ventas_totales = venta[1]
                resultados_text.insert(END, f"Libro con código {codigo_libro} - Ventas totales: {ventas_totales}\n")
        else:
            resultados_text.insert(END, "No hay ventas registradas.")
        
    resultados_text = Text(ventana, height=10, width=30)
    resultados_text.pack()

    obtener_ventas_button = Button(ventana, text="Obtener Ventas", command=obtener_ventas_totales_por_codigo_libro)
    obtener_ventas_button.pack()

def ventana_estadisticas_2():
    ventana = Toplevel()
    ventana.title("Estadísticas - Libro más y menos vendido")
    ventana.geometry("300x150")

    def mostrar_libros_mas_y_menos_vendido():
        conexion, cursor = conectar_db("biblioteca.db")
        sentencia = """SELECT id_libro, SUM(cantidad) AS unidades_vendidas
                        FROM Ventas
                        GROUP BY id_libro
                        ORDER BY unidades_vendidas DESC"""
        cursor.execute(sentencia)
        libros_vendidos = cursor.fetchall()
        desconectar_db(conexion, cursor)

        if libros_vendidos:
            libro_mas_vendido = libros_vendidos[0]
            libro_menos_vendido = libros_vendidos[-1]

            messagebox.showinfo("Estadísticas", f"Libro más vendido:\nCódigo: {libro_mas_vendido[0]}\nUnidades vendidas: {libro_mas_vendido[1]}\n\nLibro menos vendido:\nCódigo: {libro_menos_vendido[0]}\nUnidades vendidas: {libro_menos_vendido[1]}")
            ventana.destroy()
        else:
            messagebox.showinfo("Estadísticas", "No hay registros de ventas.")
            ventana.destroy()

    btn_mostrar_estadisticas = Button(ventana, text="Mostrar Estadísticas", command=mostrar_libros_mas_y_menos_vendido)
    btn_mostrar_estadisticas.pack()

def ventana_estadisticas_3():
    ventana = Toplevel()
    ventana.title("Estadísticas - Venta Total de la Librería")
    ventana.geometry("300x100")

    def calcular_venta_total_libreria():
        conexion, cursor = conectar_db("biblioteca.db")
        sentencia = """SELECT SUM(valor_venta) AS venta_total
                        FROM ventas"""
        cursor.execute(sentencia)
        venta_total_libreria = cursor.fetchone()[0]
        desconectar_db(conexion, cursor)

        messagebox.showinfo("Venta Total de la Librería", f"La venta total de la librería es: {venta_total_libreria}")
        ventana.destroy()
    btn_calcular = Button(ventana, text="Calcular Venta Total", command=calcular_venta_total_libreria)
    btn_calcular.pack()

def ventana_estadisticas_4():
    ventana = Toplevel()
    ventana.title("Estadística: Cliente con mayor compra por venta")
    ventana.geometry("300x100")

    def obtener_cliente_mayor_compra():
        conexion, cursor = conectar_db("biblioteca.db")
        sentencia = """SELECT Clientes.nombre, SUM(Ventas.valor_venta) AS total_compra
                    FROM Ventas
                    JOIN Clientes ON Ventas.id_cliente = Clientes.id_cliente
                    GROUP BY Ventas.id_cliente
                    ORDER BY total_compra DESC
                    LIMIT 1"""
        cursor.execute(sentencia)
        cliente_mayor_compra = cursor.fetchone()
        desconectar_db(conexion, cursor)

        if cliente_mayor_compra:
            nombre_cliente = cliente_mayor_compra[0]
            total_compra = cliente_mayor_compra[1]

            messagebox.showinfo("Cliente con mayor compra por venta", f"El cliente con la mayor compra por venta fue: {nombre_cliente}\nTotal de compra: {total_compra}")
            ventana.destroy()
        else:
            messagebox.showinfo("Cliente con mayor compra por venta", "No se encontró ningún cliente en la base de datos.")
            ventana.destroy()

    btn_obtener_estadistica = Button(ventana, text="Obtener Estadística", command=obtener_cliente_mayor_compra)
    btn_obtener_estadistica.pack()

def ventana_estadisticas_5():
    ventana = Toplevel()
    ventana.title("Estadísticas - Cliente con Mayor Volumen de Compra Total")
    ventana.geometry("300x100")

    def obtener_cliente_mayor_volumen_compra():
        conexion, cursor = conectar_db("biblioteca.db")
        sentencia = """SELECT Clientes.nombre, Ventas.valor_venta AS volumen_compra
                    FROM Ventas
                    JOIN Clientes ON Ventas.id_cliente = Clientes.id_cliente
                    GROUP BY Ventas.id_cliente
                    ORDER BY volumen_compra DESC
                    LIMIT 1"""
        cursor.execute(sentencia)
        cliente_mayor_volumen_compra = cursor.fetchone()
        desconectar_db(conexion, cursor)

        if cliente_mayor_volumen_compra:
            nombre_cliente = cliente_mayor_volumen_compra[0]
            volumen_compra = cliente_mayor_volumen_compra[1]
            messagebox.showinfo("Cliente con Mayor Volumen de Compra Total", f"El cliente con el mayor volumen de compra total es: {nombre_cliente}\nVolumen de compra: {volumen_compra}")
            ventana.destroy
        else:
            messagebox.showinfo("Cliente con Mayor Volumen de Compra Total", "No se encontró ningún cliente en la base de datos.")
            ventana.destroy()
    btn_obtener_estadistica = Button(ventana, text="Obtener Estadística", command=obtener_cliente_mayor_volumen_compra)
    btn_obtener_estadistica.pack()