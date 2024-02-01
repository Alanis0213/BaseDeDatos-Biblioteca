from sql_librerias import conectar_db,desconectar_db
from prettytable import PrettyTable
from modulo_clientes import ingresar_cliente,lista_clientes,eliminar_cliente,buscar_cliente,actualizar_cliente
from modulo_libros import *
from modulo_ventas import *
from modulo_estadisticas import *
clientes=[["juan",3100]]
#nombre del cliente, codigo del cliente
libros=[]
#codigo del libro ISBN, titulo del libro,precio del libro, unidades de libros disponibles
ventas=[]
#codigo de venta (generado automaticamente),codigo del cliente,codigo del libro,cantidad vendida,valor de la venta

#["maria",3101],["pedro",3102],["laura",3103]
#[12552,"iliada",5300,25],[12553,"platero",2500,16],[12554,"cien",3600,35]
def menu_clientes():
    while True:
        print("==== Menú clientes ====")
        print("1 - Ingresar clientes")
        print("2 - Lista de clientes")
        print("3 - Borrar cliente") 
        print("4 - Buscar cliente")
        print("5 - Actualizar cliente")
        print("6 - Salir")
        opcion1 = input("Ingrese una opción: ")

        if opcion1 == '1':
            ingresar_cliente()
        elif opcion1 == '2':
            lista_clientes(clientes)
        elif opcion1 == '3':
            eliminar_cliente(clientes)
        elif opcion1 == '4':
            buscar_cliente(clientes)
        elif opcion1 == '5':
            actualizar_cliente(clientes)
        elif opcion1 == '6':
            break
        else:
            print("Opción inválida - intente nuevamente")

def menu_libros():
    while True:
        print("==== Menú libros ====")
        print("1 - Ingresar libros")
        print("2 - Lista de libros")
        print("3 - Borrar libro")
        print("4 - Buscar libro")
        print("5 - Actualizar libro")
        print("6 - Salir")
        opcion1 = input("Ingrese una opción: ")

        if opcion1 == '1':
            ingresar_libros(libros)
        elif opcion1 == '2':
            lista_libros(libros)
        elif opcion1 == '3':
            eliminar_cliente(libros)
        elif opcion1 == '4':
            buscar_libro(libros)
        elif opcion1 == '5':
            actualizar_libro(libros)
        elif opcion1 == '6':
            break
        else:
            print("Opción inválida - intente nuevamente")

def menu_ventas():
    while True:
        print("==== Menu Ventas ====")
        print("1 - Realizar venta")
        print("2 - Lista de ventas realizadas")
        print("3 - Buscar venta realizada")
        print("4 - Borrar venta")
        print("5 - Actualizar venta")
        print("6 - Salir")
        opcion4 = input("Ingrese una opción: ")
        if opcion4 == '1':
            registrar_venta()
        elif opcion4 == '2':
            mostrar_ventas()
        elif opcion4 == '3':
            buscar_venta()
        elif opcion4 == '4':
            eliminar_venta()
        elif opcion4 == '5':
            actualizar_venta()
        elif opcion4 == '6':
            break
        else:
            print("Opción inválida")

def menu_estadisticas():
    while True:
        print("==== Menu estadísticas ====")
        print("1 - Ventas totales de libros por ISBN")
        print("2 - Libro más y menos vendido")
        print("3 - Venta total de la librería")
        print("4 - Cliente con mayor compra por venta")
        print("5 - Cliente con mayor volumen de compra total")
        print("6 - Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == '1':
            obtener_ventas_totales_por_codigo_libro()
        elif opcion == '2':
            mostrar_libros_mas_y_menos_vendido()
        elif opcion == '3':
            calcular_venta_total_libreria()
        elif opcion == '4':
            cliente_mayor_compra()
        elif opcion == '5':
            volumen_compra()
        elif opcion == '6':
            break
        else:
            print("Opción inválida")

while True:
        print("====Menu principal====")
        print("1 - clientes")
        print("2 - libros")
        print("3 - ventas")
        print("4 - estadisticas")
        print("5 - salir")
        opcion=input("ingrese una opcipn: ")
        if opcion == '1':
            menu_clientes()
        elif opcion == '2':
            menu_libros()
        elif opcion == '3':
            menu_ventas()
        elif opcion == '4':
            menu_estadisticas()
        elif opcion=='5':
            print("fin del programa")
            break
        else:
            print("opcion invalida, intente nuevamente")