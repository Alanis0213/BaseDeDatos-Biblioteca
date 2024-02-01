from sql_librerias import conectar_db,desconectar_db
from prettytable import PrettyTable
def obtener_ventas_totales_por_codigo_libro():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT id_libro, SUM(cantidad) AS ventas_totales
                    FROM Ventas
                    GROUP BY id_libro"""
    cursor.execute(sentencia)
    ventas_totales_por_libro = cursor.fetchall()

    print("Ventas por libro:")
    for venta in ventas_totales_por_libro:
        codigo_libro = venta[0]
        ventas_totales = venta[1]
        print("Libro con código", codigo_libro, "- Ventas totales:", ventas_totales)
    desconectar_db(conexion, cursor)

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

        print("==============================================")
        print("Libro más vendido:")
        print("Código:", libro_mas_vendido[0])
        print("Unidades vendidas:", libro_mas_vendido[1])
        print("==============================================")
        print("Libro menos vendido:")
        print("Código:", libro_menos_vendido[0])
        print("Unidades vendidas:", libro_menos_vendido[1])
        print("==============================================")
    else:
        print("No hay registros de ventas.")

def calcular_venta_total_libreria():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT SUM(valor_venta) AS venta_total
                    FROM Ventas"""
    cursor.execute(sentencia)
    venta_total_libreria = cursor.fetchone()[0]
    desconectar_db(conexion, cursor)

    print("====================================================")
    print("Venta Total de la librería:", venta_total_libreria)
    print("====================================================")

def cliente_mayor_compra():
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

    if cliente_mayor_compra is not None:
        nombre_cliente = cliente_mayor_compra[0]
        total_compra = cliente_mayor_compra[1]

        print("====================================================")
        print("El cliente con la mayor compra por venta fue:", nombre_cliente)
        print("Total de compra:", total_compra)
        print("====================================================")
    else:
        print("No se encontró ningún cliente en la base de datos.")

def volumen_compra():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT Clientes.nombre, SUM(Ventas.valor_venta) AS volumen_compra
                    FROM Ventas
                    JOIN Clientes ON Ventas.id_cliente = Clientes.id_cliente
                    GROUP BY Ventas.id_cliente
                    ORDER BY volumen_compra DESC
                    LIMIT 1"""
    cursor.execute(sentencia)
    cliente_mayor_volumen_compra = cursor.fetchone()
    desconectar_db(conexion, cursor)

    if cliente_mayor_volumen_compra is not None:
        nombre_cliente = cliente_mayor_volumen_compra[0]
        volumen_compra = cliente_mayor_volumen_compra[1]

        print("===================================================================")
        print("El cliente con el mayor volumen de compra total es:", nombre_cliente)
        print("Volumen de compra:", volumen_compra)
        print("===================================================================")
    else:
        print("No se encontró ningún cliente en la base de datos.")
