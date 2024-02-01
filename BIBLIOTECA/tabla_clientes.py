from sql_librerias import conectar_db,desconectar_db

conexion,cursor=conectar_db("biblioteca.db")

cursor.execute("""CREATE TABLE clientes(
                    id_cliente           INT PRIMARY KEY,
                    nombre               TEXT NOT NULL
                    )

                """)

desconectar_db(conexion,cursor)