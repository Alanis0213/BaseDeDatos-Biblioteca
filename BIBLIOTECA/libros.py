from tkinter import *
from tkinter import messagebox
from modulo_libros import ingresar_libros, lista_libros, eliminar_libro, actualizar_libro
from conectar_y_desconectar import*
from tkinter import ttk

def ventana_ingresar_libro():
    ventana_agregar_libro = Toplevel()
    ventana_agregar_libro.title("Agregar libro")
    ventana_agregar_libro.geometry("300x300")
    ventana_agregar_libro.config(bg="orange")

    codigo_label = Label(ventana_agregar_libro, text="Código del libro:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_agregar_libro)
    codigo_entry.pack()

    titulo_label = Label(ventana_agregar_libro, text="Título:")
    titulo_label.pack()
    titulo_entry = Entry(ventana_agregar_libro)
    titulo_entry.pack()

    precio_label = Label(ventana_agregar_libro, text="Precio:")
    precio_label.pack()
    precio_entry = Entry(ventana_agregar_libro)
    precio_entry.pack()

    unidades_label = Label(ventana_agregar_libro, text="Unidades:")
    unidades_label.pack()
    unidades_entry = Entry(ventana_agregar_libro)
    unidades_entry.pack()

    
    def limpiar_campos():
        codigo_entry.config(state="normal")
        codigo_entry.delete(0, END)
        titulo_entry.config(state="normal")
        titulo_entry.delete(0,END)
        precio_entry.config(state="normal")
        precio_entry.delete(0,END)
        unidades_entry.config(state="normal")
        unidades_entry.delete(0,END)
    
    def guardar():
        codigo = codigo_entry.get()
        titulo = titulo_entry.get()
        precio = precio_entry.get()
        unidades = unidades_entry.get()

        if codigo == "" or titulo == "" or precio == "" or unidades == "":
            messagebox.showinfo("Error", "Por favor, ingrese todos los campos.")
            return

        try:
            precio = float(precio)
            unidades = int(unidades)
        except ValueError:
            messagebox.showinfo("Error", "Precio y unidades deben ser números.")
            return

        conexion, cursor = conectar_db("alanis.db")

        cursor.execute("SELECT id_libros FROM libros WHERE id_libros = ?", (codigo,))
        resultado = cursor.fetchone()
        if resultado is not None:
            messagebox.showinfo("Error", "El código ISBN ya ha sido registrado. Intente nuevamente.")
            desconectar_db(conexion, cursor)
            return

        sentencia = "INSERT INTO libros(id_libros, nombre, precio, unidades) VALUES (?, ?, ?, ?)"
        cursor.execute(sentencia, (codigo, titulo, precio, unidades))
        conexion.commit()
        desconectar_db(conexion, cursor)
        messagebox.showinfo("Éxito", "Libro registrado exitosamente.")
        
    
    guardar_button = Button(ventana_agregar_libro, text="Guardar", command=guardar)
    limpiar_button=Button(ventana_agregar_libro, text="limpiar",command=limpiar_campos)
    limpiar_button.pack()
    guardar_button.pack()


def ventana_listar_libros():
    ventana_listar = Toplevel()
    ventana_listar.title("Listar libros")
    ventana_listar.geometry("900x500")
    ventana_listar.config(bg="orange")

    def cargar_libro(event):
        selected_row = tabla_libros.focus()
        if selected_row:
            values = tabla_libros.item(selected_row)["values"]
            codigo_libro_entry.config(state="normal")
            codigo_libro_entry.delete(0, END)
            codigo_libro_entry.insert(END, values[0])
            codigo_libro_entry.config(state="disabled")
            titulo_libro_entry.config(state="normal")
            titulo_libro_entry.delete(0, END)
            titulo_libro_entry.insert(END, values[1])
            titulo_libro_entry.config(state="disabled")
            precio_libro_entry.config(state="normal")
            precio_libro_entry.delete(0, END)
            precio_libro_entry.insert(END, values[2])
            precio_libro_entry.config(state="disabled")
            unidades_libro_entry.config(state="normal")
            unidades_libro_entry.delete(0, END)
            unidades_libro_entry.insert(END, values[3])
            unidades_libro_entry.config(state="disabled")

    tabla_frame = Frame(ventana_listar)
    tabla_frame.pack(pady=10)

    tabla_libros = ttk.Treeview(tabla_frame, columns=("codigo_libro", "titulo_libro", "precio_libro", "unidades_libro"), show="headings")
    tabla_libros.heading("codigo_libro", text="Código de libro")
    tabla_libros.heading("titulo_libro", text="Título")
    tabla_libros.heading("precio_libro", text="Precio")
    tabla_libros.heading("unidades_libro", text="Unidades")
    tabla_libros.pack(side=LEFT, fill=Y)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_libros.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tabla_libros.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_libros.yview)

    libros = lista_libros()
    if libros:
        for libro in libros:
            tabla_libros.insert("", index='end', values=(libro[0], libro[1], libro[2], libro[3]))
    else:
        tabla_libros.insert("", index='end', values=("No hay libros registrados.",))
    tabla_libros.bind("<ButtonRelease-1>", cargar_libro)

    datos_libro_frame = Frame(ventana_listar)
    datos_libro_frame.pack(pady=10)

    codigo_libro_label = Label(ventana_listar, text="Código de libro:")
    codigo_libro_label.pack()
    codigo_libro_entry = Entry(ventana_listar)
    codigo_libro_entry.pack()

    titulo_libro_label = Label(ventana_listar, text="Título de libro:")
    titulo_libro_label.pack()
    titulo_libro_entry = Entry(ventana_listar)
    titulo_libro_entry.pack()

    precio_libro_label = Label(ventana_listar, text="Precio de libro:")
    precio_libro_label.pack()
    precio_libro_entry = Entry(ventana_listar)
    precio_libro_entry.pack()

    unidades_libro_label = Label(ventana_listar, text="Unidades de libro:")
    unidades_libro_label.pack()
    unidades_libro_entry = Entry(ventana_listar)
    unidades_libro_entry.pack()
def ventana_eliminar_libro():
    ventana_borrar_libro = Toplevel()
    ventana_borrar_libro.title("Eliminar libro")
    ventana_borrar_libro.geometry("200x150")
    ventana_borrar_libro.config(bg="orange")

    codigo_label = Label(ventana_borrar_libro, text="Código del libro:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_borrar_libro)
    codigo_entry.pack()

    def eliminar():
        codigo = codigo_entry.get()
        if codigo != "":
            confirmacion=messagebox.askyesno("confirmar","estas seguro de que desea eliminar este libro")
            if confirmacion:
                resutado=eliminar_libro(codigo)
                if resutado is True:
                    messagebox.showinfo("exito","el libro se ha eliminado de forma correcta")
                    ventana_borrar_libro.destroy()
            else:
                messagebox.showinfo("error","no se encontro ninguna venta con este codigo")
        else:
            messagebox.showinfo("Error", "Por favor, ingresa el código del libro")

    eliminar_button = Button(ventana_borrar_libro, text="Eliminar", command=eliminar)
    eliminar_button.pack()


def ventana_actualizar_libro():
    ventana_actualizar = Toplevel()
    ventana_actualizar.title("Actualizar libro")
    ventana_actualizar.geometry("1000x500")
    ventana_actualizar.config(bg="orange")

    def cargar_libros():
        libros = obtener_libros()  # Replace obtener_libros() with the function that fetches books from the database
        tabla_libros.delete(*tabla_libros.get_children())
        for libro in libros:
            tabla_libros.insert("", index='end', values=(libro[0], libro[1], libro[2], libro[3]))

    def cargar_libro(event):
        selected_row = tabla_libros.focus()
        if selected_row:
            values = tabla_libros.item(selected_row)["values"]
            codigo_entry.config(state="normal")
            codigo_entry.delete(0, END)
            codigo_entry.insert(END, values[0])
            codigo_entry.config(state="disabled")
            nombre_entry.delete(0, END)
            nombre_entry.insert(END, values[1])
            precio_entry.delete(0, END)
            precio_entry.insert(END, values[2])
            unidades_entry.delete(0, END)
            unidades_entry.insert(END, values[3])

    def actualizar():
        codigo = codigo_entry.get()
        nuevo_titulo = nombre_entry.get()
        nuevo_precio = precio_entry.get()
        nuevas_unidades = unidades_entry.get()

        if codigo != "" and nuevo_titulo != "" and nuevo_precio != "" and nuevas_unidades != "":
            if actualizar_libro(codigo, nuevo_titulo, nuevo_precio, nuevas_unidades):
                messagebox.showinfo("Actualización exitosa", "El libro se ha actualizado correctamente.")
                ventana_actualizar.destroy()
                cargar_libros()  # Reload the table after successful update
            else:
                messagebox.showinfo("Error", "El código del libro no se encontró en la base de datos.")
        else:
            messagebox.showinfo("Error", "Por favor, llenar todos los campos.")

    tabla_frame = Frame(ventana_actualizar)
    tabla_frame.pack(pady=10)

    tabla_libros = ttk.Treeview(tabla_frame, columns=("codigo", "nombre", "precio", "unidades"), show="headings")
    tabla_libros.heading("codigo", text="Código")
    tabla_libros.heading("nombre", text="Título")
    tabla_libros.heading("precio", text="Precio")
    tabla_libros.heading("unidades", text="Unidades")
    tabla_libros.pack(side=LEFT, fill=Y)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_libros.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tabla_libros.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_libros.yview)

    tabla_libros.bind("<ButtonRelease-1>", cargar_libro)

    cargar_libros()

    codigo_label = Label(ventana_actualizar, text="Código del libro:")
    codigo_label.pack()
    codigo_entry = Entry(ventana_actualizar)
    codigo_entry.pack()

    nombre_label = Label(ventana_actualizar, text="Nuevo título:")
    nombre_label.pack()
    nombre_entry = Entry(ventana_actualizar)
    nombre_entry.pack()

    precio_label = Label(ventana_actualizar, text="Nuevo precio:")
    precio_label.pack()
    precio_entry = Entry(ventana_actualizar)
    precio_entry.pack()

    unidades_label = Label(ventana_actualizar, text="Nuevas unidades:")
    unidades_label.pack()
    unidades_entry = Entry(ventana_actualizar)
    unidades_entry.pack()

    actualizar_button = Button(ventana_actualizar, text="Actualizar", command=actualizar)
    actualizar_button.pack()

def obtener_libros():
    conexion, cursor = conectar_db("alanis.db")
    sentencia = """SELECT *
                FROM libros
    """
    cursor.execute(sentencia)
    libros = cursor.fetchall()
    desconectar_db(conexion, cursor)
    return libros

def ventana_buscar_libro():
    ventana = Toplevel()
    ventana.title("Buscar Libro")
    ventana.geometry("300x100")
    ventana.config(bg="orange")
    def buscar_libro():
        codigo = entry_codigo.get()
        if codigo != "":
            conexion, cursor = conectar_db("alanis.db")
            sentencia = """SELECT *
                        FROM libros
                        WHERE id_libros = ?"""
            cursor.execute(sentencia, (codigo,))
            libro = cursor.fetchone()
            desconectar_db(conexion, cursor)

            if libro:
                messagebox.showinfo("Libro Encontrado", f"ISBN: {libro[0]}, Título: {libro[1]}, Precio: {libro[2]}, Unidades: {libro[3]}")
            else:
                messagebox.showinfo("Libro No Encontrado", "No se encontró ningún libro con ese código.")
        else:
            messagebox.showinfo("Error", "Por favor, ingrese un código de libro.")

    label_codigo = Label(ventana, text="Código del libro:")
    label_codigo.pack()

    entry_codigo = Entry(ventana)
    entry_codigo.pack()

    btn_buscar = Button(ventana, text="Buscar", command=buscar_libro)
    btn_buscar.pack()



