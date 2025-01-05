# Reto_Seek

Por favor usar como usuario de prueba 'test' y como contraseña 't18$V3Y9]lE)' con este pueden obtener el token de autenticación en el primer endpoint.

## Biblioteca API Backend

Este es un backend para una aplicación de gestión de libros, desarrollada utilizando Django Rest Framework (DRF) y MongoDB como base de datos. La API permite realizar operaciones CRUD sobre los libros y obtener información detallada, incluyendo operaciones de agregación con MongoDB para obtener estadísticas sobre los libros.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.8+**
- **MongoDB 6.0.19** (para la base de datos)
- **Mongosh 2.3.2** (para interactuar con MongoDB)
- **Django 3.1.12**
- **Django Rest Framework 3.15.1**
- **Django Simple JWT 5.2.2** para autenticación basada en JWT
- **Djongo 1.3.7** para conectar MongoDB con Django
- **drf-spectacular 0.28.0** para la documentación de la API
- **pip** para gestionar dependencias de Python

## Instalación

1. **Clonar el repositorio**:

   Clone el repositorio a tu máquina local:

   ```bash
   git clone https://github.com/hdballestan/Reto_Seek.git
   cd Reto_Seek
   ```
2. Crear un entorno virtual:

Es recomendable utilizar un entorno virtual para gestionar las dependencias:

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows usa 'venv\Scripts\activate'
   ```

3. Instalar dependencias:

Instale las dependencias necesarias utilizando pip:

 ```bash
    pip install -r requirements.txt
   ```

4. Configurar MongoDB:

Asegúrese de tener una instancia de MongoDB en funcionamiento. Puede usar MongoDB en local o en la nube (MongoDB Atlas).

En caso de que desees configurar MongoDB localmente, puedes seguir las instrucciones de instalación en [https://www.mongodb.com/](mongodb).

5.Configuración de variables de entorno:

Cree un archivo .env en la raíz del proyecto con las siguientes variables (como se muestra en el archivo env_example.txt):
 ```bash
    HOST=localhost
    PORT=27017
    USERNAME=
    DBPASS=
    SOURCE=
    CLIENT=mongodb://some:some@localhost:27017/some
   ```

6. Aplicar migraciones:

 ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```

## Ejecución 

Para ejecutar el servidor de desarrollo de Django, use el siguiente comando:

```bash
    python manage.py runserver
   ```

Esto iniciará el servidor en http://127.0.0.1:8000/. La API estará disponible en las siguientes rutas:

    POST /api/token/: Obtén un token de acceso JWT con el nombre de usuario y contraseña.
    GET /api/books/: Obtén una lista paginada de libros.
    POST /api/books/: Crea un nuevo libro.
    GET /api/books/{id}/: Obtén detalles de un libro específico.
    PUT /api/books/{id}/: Actualiza los detalles de un libro específico.
    DELETE /api/books/{id}/: Elimina un libro específico.
    GET /api/books/avg_price/{year}/: Obtén el precio promedio de los libros publicados en un año específico.

## Pruebas

Para realizar las pruebas unitarias de la API, ejecute:
```bash
    python manage.py test
   ```

## Documentación de la API

La API está documentada utilizando drf-spectacular. Puede acceder a la documentación de la API en:
```bash
    http://127.0.0.1:8000/schema/
   ```

# Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

