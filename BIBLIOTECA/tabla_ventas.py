from sql_librerias import conectar_db,desconectar_db

conexion,cursor=conectar_db("biblioteca.db")

cursor.execute("""CREATE TABLE ventas(
                    codigo_venta          INT PRIMARY KEY,
                    id_cliente            INT NOT NULL,
                    id_libro              INT NOT NULL,
                    cantidad              INT NOT NULL,
                    valor_venta           REAL NOT NULL
                    )

                """)

desconectar_db(conexion,cursor)