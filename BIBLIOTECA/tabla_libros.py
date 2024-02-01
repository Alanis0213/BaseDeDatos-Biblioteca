from sql_librerias import conectar_db,desconectar_db

conexion,cursor=conectar_db("biblioteca.db")

cursor.execute("""CREATE TABLE libros(
                    id_libros           INT PRIMARY KEY,
                    nombre              TEXT NOT NULL,
                    precio              REAL NOT NULL,
                    unidades            INT NOT NULL
                    )

                """)

desconectar_db(conexion,cursor)