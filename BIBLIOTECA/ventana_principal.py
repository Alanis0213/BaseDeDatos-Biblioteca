from tkinter import *
from clientes import ventana_ingresar_cliente, ventana_listar_clientes, ventana_eliminar_cliente,ventana_actualizar_cliente,ventana_buscar_cliente
from libros import *
from ventas import*
from estadisticas import*

root = Tk()
root.title("Librería")

root.geometry(f"{900}x{400}+{100}+{50}")
marco=Frame(root,width=3000,height=1000)
marco.config(bg="sky blue")  
marco.pack() 


 
menu_bar = Menu(root)

clientes_menu = Menu(menu_bar, tearoff=0)
clientes_menu.add_command(label="Ingresar", command=ventana_ingresar_cliente)
clientes_menu.add_command(label="Listar", command=ventana_listar_clientes)
clientes_menu.add_command(label="Eliminar", command=ventana_eliminar_cliente)
clientes_menu.add_command(label="buscar", command=ventana_buscar_cliente)
clientes_menu.add_command(label="Actualizar", command=ventana_actualizar_cliente)
menu_bar.add_cascade(label="Clientes", menu=clientes_menu)

libros_menu = Menu(menu_bar, tearoff=0)
libros_menu.add_command(label="Ingresar", command=ventana_ingresar_libro)
libros_menu.add_command(label="Listar", command=ventana_listar_libros)
libros_menu.add_command(label="Eliminar", command=ventana_eliminar_libro)
libros_menu.add_command(label="buscar",command=ventana_buscar_libro)
libros_menu.add_command(label="Actualizar", command=ventana_actualizar_libro)
menu_bar.add_cascade(label="Libros", menu=libros_menu)

ventas_menu = Menu(menu_bar, tearoff=0)
ventas_menu.add_command(label="Registrar Venta", command=ventana_registrar_venta)
ventas_menu.add_command(label="Listar Ventas", command=ventana_listar_ventas)
ventas_menu.add_command(label="Buscar Venta", command=ventana_buscar_venta)
ventas_menu.add_command(label="Eliminar Venta", command=ventana_eliminar_venta)
ventas_menu.add_command(label="Actualizar Venta", command=ventana_actualizar_venta)
menu_bar.add_cascade(label="Ventas", menu=ventas_menu)


estadisticas_menu=Menu(menu_bar,tearoff=0)
estadisticas_menu.add_command(label="Ventas totales de libros por ISBN",command=ventana_estadisticas_1)
estadisticas_menu.add_command(label="Libro más y menos vendido",command=ventana_estadisticas_2)
estadisticas_menu.add_command(label="Venta total de la librería",command=ventana_estadisticas_3)
estadisticas_menu.add_command(label="Cliente con mayor compra por venta",command=ventana_estadisticas_4)
estadisticas_menu.add_command(label="Cliente con mayor volumen de compra total",command=ventana_estadisticas_5)
menu_bar.add_cascade(label="estadisticas",menu=estadisticas_menu)

root.config(menu=menu_bar)
root.mainloop()
