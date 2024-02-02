# Biblioteca con listas

## Contenido

1. [Información General](#información-general)
2. [Funcionalidades](#funcionalidades)
3. [Instrucciones de Uso](#instrucciones-de-uso)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Requisitos del Sistema](#requisitos-del-sistema)
6. [Instalación](#instalación)
7. [Configuración](#configuración)
8. [Uso](#uso)
9. [Contribuciones](#contribuciones)
10. [Licencia](#licencia)
11. [Contacto](#contacto)

## Información General

Este proyecto implementa un Sistema de Gestión de Librería en Python a travez de modulos utilizando interfaz grafica para la ejecucion de este programa, este sistema muestra diferentes fucniones para administrar los libros, los clientes y las ventas y compras que estos puedan realiar. A través de una interfaz, los usuarios pueden realizar diversas operaciones, como ingresar clientes, registrar libros, realizar ventas y obtener estadísticas sobre las ventas reealizas y clientes

## Funcionalidades

1. ### Clientes:

    - Ingresar nuevos clientes.
    - Mostrar una lista de clientes registrados.
    - Borrar clientes, teniendo en cuenta las restricciones de eliminación.
    - Buscar clientes por su código y mostrar información detallada.
    - Actualizar la información de un cliente, como su nombre.

2. ### Libros:

    - Ingresar nuevos libros con su código ISBN, título, precio y unidades disponibles.
    - Mostrar una lista de libros registrados.
    - Borrar libros, teniendo en cuenta las restricciones de eliminación.
    - Buscar libros por su código y mostrar información detallada.
    - Actualizar la información de un libro, como su título, precio o unidades disponibles.
    - Actualizar la cantidad de unidades de un libro y su precio.

3. ### Ventas:

    - Realizar ventas, registrando la cantidad vendida y actualizando las existencias.
    - Mostrar una lista de todas las ventas realizadas.
    - Buscar ventas por su código y mostrar información detallada.
    - Eliminar ventas, ajustando las existencias de libros correspondientes.
    - Actualizar la cantidad vendida en una venta existente.

4. ### Estadísticas:

    - Obtener las ventas totales de libros por su código ISBN.
    - Identificar el libro más y menos vendido.
    - Calcular la venta total de la librería.
    - Identificar el cliente con la mayor compra por venta.
    - Identificar el cliente con el mayor volumen de compra total.

## Requisitos del Sistema

    - Python 3.x
    - Consola o entorno compatible con la ejecución de Python.
    - Extencion prettyTable.
    - Base de datos SQLite

## Instalación
1. Clona o descarga el repositorio.
2. habre tu base de datos.
3. Ejecuta el script main.py desde tu terminal o entorno de desarrollo.


## Instrucciones de Uso
1. Interactuar con el Menú Principal:

    Una vez que el script esté en ejecución, se presentará un menú principal con opciones numeradas. dodne debe ingresa el número correspondiente a la operación que deseas realizar y presiona Enter, para que se ejecute la opcion.

2. Explorar las Funcionalidades:

    Se presentarán menús secundarios según la opción seleccionada. Sigue las instrucciones en la consola para interactuar con las funcionalidades específicas, como ingresar clientes, libros, ventas entre otras opciones.

3. Salir del Programa:

    Una vez quieras finalizar la ejecucion del programa,puedes seleccionar la opción para salir del programa.

## Estructura del Proyecto

El proyecto se organiza en módulos que abordan distintas áreas del sistema, como clientes, libros, ventas y estadísticas. Cada módulo contiene funciones específicas para realizar las operaciones relacionadas con su área correspondiente.


## Configuración

No se requiere configuración adicional para el funcionamiento básico. Sin embargo, se pueden realizar ajustes en el código según las necesidades específicas del usuario.

## Uso

Una vez se decida utilizar el programa, siga las opciones proporcionadas, para asi realizar las distintas operaciones que el programa te ofrece ingresando la opcion segun el menu presentado.

## Contribuciones

Puedes contribuir en este codigo poniendo a prueba sus validaciones, creando una copia podras implementar los cambios que necesites, para adaptarlo a tus necesidades.


## Contacto

Para preguntas o comentarios, puedes contactarme a través de [correo electrónico](alanisdeavilat@gmail.com).

