from tkinter import *
from tkinter import messagebox
from modulo_clientes import ingresar_cliente, lista_clientes, eliminar_cliente, actualizar_cliente
from conectar_y_desconectar import*
from tkinter import ttk
def ventana_ingresar_cliente():
    ventana_agregar_cliente = Toplevel()
    ventana_agregar_cliente.title("Agregar cliente")
    ventana_agregar_cliente.geometry("200x150")
    ventana_agregar_cliente.config(bg="pink")

    id_cliente_label = Label(ventana_agregar_cliente, text="id_cliente:")
    id_cliente_label.pack()
    id_cliente_entry = Entry(ventana_agregar_cliente)
    id_cliente_entry.pack()

    nombre_label = Label(ventana_agregar_cliente, text="nombre:")
    nombre_label.pack()
    nombre_entry = Entry(ventana_agregar_cliente)
    nombre_entry.pack()

    def limpiar_campos():
        id_cliente_entry.config(state="normal")
        id_cliente_entry.delete(0, END)
        nombre_entry.config(state="normal")
        nombre_entry.delete(0,END)

    def guardar():
        id_cliente = id_cliente_entry.get()
        nombre = nombre_entry.get()
        if id_cliente != "" and nombre != "":
            ingresar_cliente(id_cliente, nombre)
            
        else:
            messagebox.showinfo("Error", "Por favor, ingresa todos los campos")

    guardar_button = Button(ventana_agregar_cliente, text="Guardar", command=guardar)
    limpiar_button=Button(ventana_agregar_cliente, text="limpiar",command=limpiar_campos)
    limpiar_button.pack()
    guardar_button.pack()

def ventana_listar_clientes():
    ventana_listar = Toplevel()
    ventana_listar.title("Listar clientes")
    ventana_listar.geometry("500x380")
    ventana_listar.config(bg="pink")

    def cargar_clientes():
        clientes = lista_clientes()
        tabla_clientes.delete(*tabla_clientes.get_children())
        for cliente in clientes:
            tabla_clientes.insert("", index='end', values=(cliente[0], cliente[1]))

    def cargar_cliente(event):
        selected_row = tabla_clientes.focus()
        if selected_row:
            values = tabla_clientes.item(selected_row)["values"]
            id_cliente_entry.config(state="normal")
            id_cliente_entry.delete(0, END)
            id_cliente_entry.insert(END, values[0])
            id_cliente_entry.config(state="disabled")
            nombre_cliente_entry.config(state="normal")
            nombre_cliente_entry.delete(0, END)
            nombre_cliente_entry.insert(END, values[1])
            nombre_cliente_entry.config(state="disabled")
    

    tabla_frame = Frame(ventana_listar)
    tabla_frame.pack(pady=10)

    tabla_clientes = ttk.Treeview(tabla_frame, columns=("id_cliente", "nombre_cliente"), show="headings")
    tabla_clientes.heading("id_cliente", text="ID de cliente")
    tabla_clientes.heading("nombre_cliente", text="Nombre de cliente")
    tabla_clientes.pack(side=LEFT, fill=Y)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_clientes.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tabla_clientes.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_clientes.yview)

    tabla_clientes.bind("<ButtonRelease-1>", cargar_cliente)

    cargar_clientes()

    id_cliente_label = Label(ventana_listar, text="ID de cliente:")
    id_cliente_label.pack()
    id_cliente_entry = Entry(ventana_listar)
    id_cliente_entry.pack()

    nombre_cliente_label = Label(ventana_listar, text="Nombre de cliente:")
    nombre_cliente_label.pack()
    nombre_cliente_entry = Entry(ventana_listar)
    nombre_cliente_entry.pack()

def ventana_eliminar_cliente():
    ventana_borrar_cliente = Toplevel()
    ventana_borrar_cliente.title("Eliminar cliente")
    ventana_borrar_cliente.geometry("200x150")
    ventana_borrar_cliente.config(bg="pink")

    codigo_label = Label(ventana_borrar_cliente, text="Código del cliente:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_borrar_cliente)
    codigo_entry.pack()

    def eliminar():
        codigo = codigo_entry.get()
        if codigo != "":
            confirmacion=messagebox.askyesno("confirmar","estas segiro de que desea eliminar este cliente ")
            if confirmacion:
                resultado=eliminar_cliente(codigo)
                if resultado is True:
                    messagebox.showinfo("exito","el cliente se ha eliminado de forma correcta")
                    ventana_borrar_cliente.destroy()
            else:
                messagebox.showinfo("error","no se encontro ningun cliente con ese codigo")
        else:
            messagebox.showinfo("Error", "Por favor, ingresa el código del cliente")

    eliminar_button = Button(ventana_borrar_cliente, text="Eliminar", command=eliminar)
    eliminar_button.pack()

def ventana_actualizar_cliente():
    ventana_actualizar = Toplevel()
    ventana_actualizar.title("Actualizar cliente")
    ventana_actualizar.geometry("500x500")
    ventana_actualizar.config(bg="pink")

    # Crear tabla para mostrar datos
    tabla_frame = Frame(ventana_actualizar)
    tabla_frame.pack(pady=10)

    tabla_clientes = ttk.Treeview(tabla_frame, columns=("codigo", "nombre"), show="headings")
    tabla_clientes.heading("codigo", text="Código")
    tabla_clientes.heading("nombre", text="Nombre")
    tabla_clientes.pack()

    # Cargar datos en la tabla
    clientes = obtener_clientes()
    tabla_clientes.delete(*tabla_clientes.get_children())
    for cliente in clientes:
        tabla_clientes.insert("", index="end", values=(cliente[0], cliente[1]))

    codigo_label = Label(ventana_actualizar, text="Código del cliente:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_actualizar)
    codigo_entry.pack()

    nombre_label = Label(ventana_actualizar, text="Nuevo nombre:")
    nombre_label.pack()
    nombre_entry = Entry(ventana_actualizar)
    nombre_entry.pack()

    def cargar_datos_seleccionados():
        selected_row = tabla_clientes.focus()
        if selected_row:
            values = tabla_clientes.item(selected_row)["values"]
            codigo_entry.config(state="normal")
            codigo_entry.delete(0, END)
            codigo_entry.insert(END, values[0])
            codigo_entry.config(state="disabled")
            nombre_entry.delete(0, END)
            nombre_entry.insert(END, values[1])

    tabla_clientes.bind("<ButtonRelease-1>", lambda event: cargar_datos_seleccionados())

    def actualizar():
        codigo = codigo_entry.get()
        nuevo_nombre = nombre_entry.get()
        if codigo != "" and nuevo_nombre != "":
            actualizar_cliente(codigo, nuevo_nombre)
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            # Actualizar la tabla después de la actualización
            clientes_actualizados = obtener_clientes()
            tabla_clientes.delete(*tabla_clientes.get_children())
            for cliente in clientes_actualizados:
                tabla_clientes.insert("", index="end", values=(cliente[0], cliente[1]))
        else:
            messagebox.showinfo("Error", "Por favor, ingresa el código del cliente y el nuevo nombre")

    actualizar_button = Button(ventana_actualizar, text="Actualizar", command=actualizar)
    actualizar_button.pack()

def obtener_clientes():
    conexion, cursor = conectar_db("alanis.db")
    sentencia = """SELECT *
                    FROM clientes"""
    cursor.execute(sentencia)
    clientes = cursor.fetchall()
    desconectar_db(conexion, cursor)
    return clientes

def ventana_buscar_cliente():
    ventana = Toplevel()
    ventana.title("Buscar Cliente")
    ventana.geometry("300x100")
    ventana.config(bg="pink")

    def buscar_cliente():
        codigo = entry_codigo.get()
        if codigo != "":
            try:
                codigo = int(codigo)
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un código válido.")
                return

            conexion, cursor = conectar_db("alanis.db")
            sentencia = """SELECT *
                        FROM clientes
                        WHERE id_cliente = ?"""
            cursor.execute(sentencia, (codigo,))
            cliente = cursor.fetchone()
            desconectar_db(conexion, cursor)

            if cliente:
                messagebox.showinfo("Cliente Encontrado", f"Código: {cliente[0]}, Nombre: {cliente[1]}")
            else:
                messagebox.showinfo("Cliente No Encontrado", "No se encontró ningún cliente con ese código.")
        else:
            messagebox.showinfo("Error", "Por favor, ingrese un código de cliente.")

    label_codigo = Label(ventana, text="Código del cliente:")
    label_codigo.pack()

    entry_codigo = Entry(ventana)
    entry_codigo.pack()

    btn_buscar = Button(ventana, text="Buscar", command=buscar_cliente)
    btn_buscar.pack()
