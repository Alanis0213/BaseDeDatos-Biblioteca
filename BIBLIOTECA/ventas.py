from tkinter import *
from sql_librerias import conectar_db, desconectar_db
from modulo_ventas import*
from tkinter import messagebox
from tkinter import ttk

def ventana_registrar_venta():
    ventana = Toplevel()
    ventana.title("Registrar Venta")
    ventana.geometry("300x300")
    ventana.config(bg="violet")

    def registrar_venta():
        id_cliente = entry_cliente.get()
        codigo_libro = entry_libro.get()
        cantidad = entry_cantidad.get()

        if id_cliente == "" or codigo_libro == "" or cantidad == "":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        try:
            id_cliente = int(id_cliente)
            codigo_libro = int(codigo_libro)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para cliente, libro y cantidad.")
            return

        if id_cliente <= 0 or codigo_libro <= 0 or cantidad <= 0:
            messagebox.showerror("Error", "Por favor, ingrese una cantidad valida.")
            return

        conexion, cursor = conectar_db("biblioteca.db")

        # Verificar si el cliente existe
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
            messagebox.showerror("Error", "El cliente no existe.")
            desconectar_db(conexion, cursor)
            

        # Verificar si el libro existe
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
            messagebox.showerror("Error", "El libro no existe.")
            desconectar_db(conexion, cursor)
            return

        # Obtener datos del libro
        sentencia = """SELECT unidades, precio
                        FROM libros
                        WHERE id_libros = ?"""
        cursor.execute(sentencia, (codigo_libro,))
        libro = cursor.fetchone()
        if libro is None:
            messagebox.showerror("Error", "El libro no existe.")
            desconectar_db(conexion, cursor)
            return

        if cantidad > libro[0]:
            messagebox.showerror("Error", "No hay suficientes unidades disponibles.")
            desconectar_db(conexion, cursor)
            return

        nuevo_codigo_venta = obtener_ultimo_codigo_venta() + 5
        valor_venta = cantidad * libro[1]
        nuevas_unidades = libro[0] - cantidad

        # Insertar venta en la base de datos
        sentencia = """INSERT INTO Ventas (codigo_venta, id_cliente, id_libro, cantidad, valor_venta)
                        VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(sentencia, (nuevo_codigo_venta, id_cliente, codigo_libro, cantidad, valor_venta))
        conexion.commit()

        # Actualizar unidades del libro
        sentencia = """UPDATE libros
                        SET unidades = ?
                        WHERE id_libros = ?"""
        cursor.execute(sentencia, (nuevas_unidades, codigo_libro))
        conexion.commit()

        print("Venta registrada exitosamente.")
        print(f"Código de venta: V-{nuevo_codigo_venta}")
        # Mostrar mensaje de confirmación
        messagebox.showinfo("Venta Registrada", "La venta se ha registrado exitosamente.")
        desconectar_db(conexion, cursor)
        limpiar_campos()

    def limpiar_campos():
        entry_cliente.delete(0, END)
        entry_libro.delete(0, END)
        entry_cantidad.delete(0, END)

    # Crear etiquetas y campos de entrada
    label_cliente = Label(ventana, text="Código del cliente:")
    label_cliente.pack()
    entry_cliente = Entry(ventana)
    entry_cliente.pack()

    label_libro = Label(ventana, text="Código del libro:")
    label_libro.pack()
    entry_libro = Entry(ventana)
    entry_libro.pack()

    label_cantidad = Label(ventana, text="Cantidad:")
    label_cantidad.pack()
    entry_cantidad = Entry(ventana)
    entry_cantidad.pack()

    # Botón de registrar venta
    btn_registrar = Button(ventana, text="Registrar Venta", command=registrar_venta)
    btn_registrar.pack()
    btn_limpiar = Button(ventana, text="Limpiar", command=limpiar_campos)
    btn_limpiar.pack()

    ventana.mainloop()

def ventana_listar_ventas():
    ventana_ventas = Toplevel()
    ventana_ventas.title("Lista de Ventas")
    ventana_ventas.geometry("1050x500")
    ventana_ventas.config(bg="violet")

    def cargar_ventas():
        ventas = obtener_ventas()
        tabla_ventas.delete(*tabla_ventas.get_children())
        for venta in ventas:
            tabla_ventas.insert("", index='end', values=(venta[0], venta[1], venta[2], venta[3], venta[4]))

    def cargar_venta(event):
        selected_row = tabla_ventas.focus()
        if selected_row:
            values = tabla_ventas.item(selected_row)["values"]
            codigo_venta_entry.config(state="normal")
            codigo_venta_entry.delete(0, END)
            codigo_venta_entry.insert(END, values[0])
            codigo_venta_entry.config(state="disabled")
            id_cliente_entry.config(state="normal")
            id_cliente_entry.delete(0, END)
            id_cliente_entry.insert(END, values[1])
            id_cliente_entry.config(state="disabled")
            id_libro_entry.config(state="normal")
            id_libro_entry.delete(0, END)
            id_libro_entry.insert(END, values[2])
            id_libro_entry.config(state="disabled")
            cantidad_entry.config(state="normal")
            cantidad_entry.delete(0, END)
            cantidad_entry.insert(END, values[3])
            cantidad_entry.config(state="disabled")
            valor_venta_entry.config(state="normal")
            valor_venta_entry.delete(0, END)
            valor_venta_entry.insert(END, values[4])
            valor_venta_entry.config(state="disabled")

    tabla_frame = Frame(ventana_ventas)
    tabla_frame.pack(pady=10)

    tabla_ventas = ttk.Treeview(tabla_frame, columns=("codigo_venta", "id_cliente", "id_libro", "cantidad", "valor_venta"), show="headings")
    tabla_ventas.heading("codigo_venta", text="Código de venta")
    tabla_ventas.heading("id_cliente", text="Código de cliente")
    tabla_ventas.heading("id_libro", text="Código de libro")
    tabla_ventas.heading("cantidad", text="Cantidad")
    tabla_ventas.heading("valor_venta", text="Valor de venta")
    tabla_ventas.pack(side=LEFT, fill=Y)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_ventas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tabla_ventas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_ventas.yview)

    tabla_ventas.bind("<ButtonRelease-1>", cargar_venta)

    cargar_ventas()

    codigo_venta_label = Label(ventana_ventas, text="Código de venta:")
    codigo_venta_label.pack()
    codigo_venta_entry = Entry(ventana_ventas)
    codigo_venta_entry.pack()

    id_cliente_label = Label(ventana_ventas, text="Código de cliente:")
    id_cliente_label.pack()
    id_cliente_entry = Entry(ventana_ventas)
    id_cliente_entry.pack()

    id_libro_label = Label(ventana_ventas, text="Código de libro:")
    id_libro_label.pack()
    id_libro_entry = Entry(ventana_ventas)
    id_libro_entry.pack()

    cantidad_label = Label(ventana_ventas, text="Cantidad:")
    cantidad_label.pack()
    cantidad_entry = Entry(ventana_ventas)
    cantidad_entry.pack()

    valor_venta_label = Label(ventana_ventas, text="Valor de venta:")
    valor_venta_label.pack()
    valor_venta_entry = Entry(ventana_ventas)
    valor_venta_entry.pack()

def obtener_ventas():
    conexion, cursor = conectar_db("biblioteca.db")
    sentencia = """SELECT *
                    FROM Ventas"""
    cursor.execute(sentencia)
    ventas = cursor.fetchall()
    desconectar_db(conexion, cursor)
    return ventas

def ventana_actualizar_venta():
    ventana_actualizar_venta = Toplevel()
    ventana_actualizar_venta.title("Actualizar Venta")
    ventana_actualizar_venta.geometry("1050x500")
    ventana_actualizar_venta.config(bg="violet")

    def cargar_ventas():
        ventas = obtener_ventas()
        tabla_ventas.delete(*tabla_ventas.get_children())
        for venta in ventas:
            tabla_ventas.insert("", index='end', values=(venta[0], venta[1], venta[2], venta[3], venta[4]))

    def cargar_venta(event):
        selected_row = tabla_ventas.focus()
        if selected_row:
            values = tabla_ventas.item(selected_row)["values"]
            codigo_entry.config(state="normal")
            codigo_entry.delete(0, END)
            codigo_entry.insert(END, values[0])
            codigo_entry.config(state="disabled")
            cliente_entry.delete(0, END)
            cliente_entry.insert(END, values[1])
            libro_entry.delete(0, END)
            libro_entry.insert(END, values[2])
            cantidad_entry.delete(0, END)
            cantidad_entry.insert(END, values[3])
            actualizar_valor_venta()

    def guardar_actualizacion():
        codigo_venta = codigo_entry.get()
        if codigo_venta != "":
            nuevo_codigo_cliente = cliente_entry.get()
            nuevo_id_libro = libro_entry.get()
            nuevas_unidades = cantidad_entry.get()
            actualizar_venta(codigo_venta, nuevo_codigo_cliente, nuevo_id_libro, nuevas_unidades, ventana_actualizar_venta)
            ventana_actualizar_venta.destroy()
            cargar_ventas()

        else:
            mensaje = "Debe haber un código de venta"
            ventana_actualizar_venta.text_widget.insert(END, mensaje + "\n")
            ventana_actualizar_venta.text_widget.see(END)
            cargar_ventas()

    def limpiar_campos():
        codigo_entry.config(state="normal")
        codigo_entry.delete(0, END)
        codigo_entry.config(state="disabled")
        cliente_entry.delete(0, END)
        libro_entry.delete(0, END)
        cantidad_entry.delete(0, END)
        valor_venta_label.config(text="")

    def actualizar_valor_venta():
        nuevo_id_libro = libro_entry.get()
        nuevas_unidades = cantidad_entry.get()
        if nuevo_id_libro != "" and nuevas_unidades != "":
            precio_libro = obtener_precio_libro(nuevo_id_libro)
            valor_venta = precio_libro * int(nuevas_unidades)
            valor_venta_label.config(text=f"Valor Venta: {valor_venta}")
        else:
            valor_venta_label.config(text="")

    tabla_frame = Frame(ventana_actualizar_venta)
    tabla_frame.pack(pady=10)

    tabla_ventas = ttk.Treeview(tabla_frame, columns=("codigo", "cliente", "libro", "cantidad", "valor_venta"), show="headings")
    tabla_ventas.heading("codigo", text="Código")
    tabla_ventas.heading("cliente", text="Cliente")
    tabla_ventas.heading("libro", text="Libro")
    tabla_ventas.heading("cantidad", text="Cantidad")
    tabla_ventas.heading("valor_venta", text="Valor Venta")
    tabla_ventas.pack(side=LEFT, fill=Y)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_ventas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tabla_ventas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_ventas.yview)

    tabla_ventas.bind("<ButtonRelease-1>", cargar_venta)

    cargar_ventas()

    codigo_label = Label(ventana_actualizar_venta, text="Código:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_actualizar_venta)
    codigo_entry.pack()

    cliente_label = Label(ventana_actualizar_venta, text="Cliente:")
    cliente_label.pack()
    cliente_entry = Entry(ventana_actualizar_venta)
    cliente_entry.pack()

    libro_label = Label(ventana_actualizar_venta, text="Libro:")
    libro_label.pack()
    libro_entry = Entry(ventana_actualizar_venta)
    libro_entry.pack()

    cantidad_label = Label(ventana_actualizar_venta, text="Cantidad:")
    cantidad_label.pack()
    cantidad_entry = Entry(ventana_actualizar_venta)
    cantidad_entry.pack()
    cantidad_entry.bind("<KeyRelease>", lambda event: actualizar_valor_venta())

    valor_venta_label = Label(ventana_actualizar_venta, text="")
    valor_venta_label.pack()

    guardar_button = Button(ventana_actualizar_venta, text="Guardar", command=guardar_actualizacion)
    guardar_button.pack()

    limpiar_button = Button(ventana_actualizar_venta, text="Limpiar", command=limpiar_campos)
    limpiar_button.pack()

    text_widget = Text(ventana_actualizar_venta)
    text_widget.pack(fill=BOTH, expand=True)

def ventana_eliminar_venta():
    ventana_borrar_venta = Toplevel()
    ventana_borrar_venta.title("Eliminar venta")
    ventana_borrar_venta.geometry("200x200")
    ventana_borrar_venta.config(bg="violet")

    codigo_label = Label(ventana_borrar_venta, text="Código de venta:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_borrar_venta)
    codigo_entry.pack()

    def eliminar():
        codigo_venta = codigo_entry.get()
        if codigo_venta != "":
            confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro que deseas eliminar esta venta?")
            if confirmacion:
                resultado = eliminar_venta(codigo_venta)  
                if resultado is True:
                    messagebox.showinfo("Éxito", "La venta se ha eliminado correctamente.")
                    ventana_borrar_venta.destroy()
                else:
                    messagebox.showinfo("error", "no se econtro ninguna venta con este codigo,")
            else:
                messagebox.showinfo("Error", "No se encontró ninguna venta con ese código.")
        else:
            messagebox.showinfo("Error", "Por favor, ingrese el código de la venta")

    eliminar_button = Button(ventana_borrar_venta, text="Eliminar", command=eliminar)
    eliminar_button.pack()

    ventana_borrar_venta.mainloop()
    
def ventana_buscar_venta():
    ventana = Toplevel()
    ventana.title("Buscar Venta")
    ventana.geometry("300x100")
    ventana.config(bg="violet")

    def buscar_venta():
        codigo_venta = entry_codigo.get()
        if codigo_venta != "":
            conexion, cursor = conectar_db("biblioteca.db")
            sentencia = """SELECT *
                        FROM Ventas
                        WHERE codigo_venta = ?"""
            cursor.execute(sentencia, (codigo_venta,))
            venta = cursor.fetchone()
            desconectar_db(conexion, cursor)

            if venta:
                messagebox.showinfo("Venta Encontrada", f"Código de venta: V-{venta[0]}, Código de cliente: {venta[1]}, Código de libro: {venta[2]}, Cantidad vendida: {venta[3]}, Valor de venta: {venta[4]}")
            else:
                messagebox.showinfo("Venta No Encontrada", "No se encontró ninguna venta con ese código.")
        else:
            messagebox.showinfo("Error", "Por favor, ingrese un código de venta.")

    label_codigo = Label(ventana, text="Código de venta:")
    label_codigo.pack()

    entry_codigo = Entry(ventana)
    entry_codigo.pack()

    btn_buscar = Button(ventana, text="Buscar", command=buscar_venta)
    btn_buscar.pack()

    ventana.mainloop()
    
