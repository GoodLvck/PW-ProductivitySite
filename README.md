# ProductivitySite

Aplicacion web construida con Django para gestionar productividad academica.

## Estructura del proyecto

- `ProductivitySite/`: codigo fuente de Django
- `docker-compose.yml`: orquestacion local con Docker Compose
- `.env.example`: plantilla de variables de entorno

## Requisitos previos

Para ejecutar el proyecto en local necesitas:

- Python `3.14.x`
- `pip`

Para ejecutar el proyecto con contenedores necesitas:

- Docker
- Docker Compose

## Variables de entorno

La aplicacion sigue un enfoque cercano a 12-factor app: la configuracion se inyecta mediante variables de entorno.

Variables principales:

- `DJANGO_DEBUG`: activa o desactiva el modo debug
- `DJANGO_SECRET_KEY`: clave secreta de Django
- `DJANGO_ALLOWED_HOSTS`: hosts permitidos separados por comas
- `DJANGO_LANGUAGE_CODE`: idioma por defecto
- `DJANGO_TIME_ZONE`: zona horaria
- `DJANGO_USE_I18N`: activa internacionalizacion
- `DJANGO_USE_TZ`: activa soporte de zonas horarias
- `DJANGO_STATIC_URL`: URL base para estaticos
- `DJANGO_LOGIN_REDIRECT_URL`: ruta de redireccion tras login
- `DJANGO_LOGOUT_REDIRECT_URL`: ruta de redireccion tras logout
- `DJANGO_DEFAULT_FROM_EMAIL`: email remitente por defecto
- `DJANGO_NOTIFY_EMAIL`: email de notificaciones
- `DJANGO_EMAIL_BACKEND`: backend de correo de Django
- `DJANGO_EMAIL_HOST`: servidor SMTP
- `DJANGO_EMAIL_PORT`: puerto SMTP
- `DJANGO_EMAIL_HOST_USER`: usuario SMTP
- `DJANGO_EMAIL_HOST_PASSWORD`: contrasena SMTP
- `DJANGO_EMAIL_USE_TLS`: activa TLS para SMTP
- `DJANGO_EMAIL_USE_SSL`: activa SSL para SMTP
- `DJANGO_EMAIL_TIMEOUT`: tiempo maximo de espera al conectar con SMTP
- `SQLITE_PATH`: ruta al fichero SQLite
- `APP_PORT`: puerto publicado por Docker Compose

Para desarrollo puedes crear un fichero `.env` en la raiz del repositorio tomando como referencia `.env.example`.
Cuando ejecutes Django en local, `SQLITE_PATH` debe apuntar a una ruta valida y escribible en tu maquina. En Docker Compose esa ruta se sobreescribe automaticamente a `/data/db.sqlite3`.

## Configuracion del correo de contacto

El formulario de contacto de la landing usa `send_mail()` de Django. La configuracion del envio se hace por variables de entorno.

En desarrollo, el valor recomendado es:

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Con ese backend, Django no envia correos reales: imprime el contenido del email en la salida de la aplicacion o en los logs del contenedor. Es la forma mas simple de probar que el formulario funciona.

Para usar un servidor SMTP real, cambia el backend y define las credenciales:

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DJANGO_EMAIL_HOST=smtp.example.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=your-account@example.com
DJANGO_EMAIL_HOST_PASSWORD=your-smtp-password
DJANGO_EMAIL_USE_TLS=true
DJANGO_EMAIL_USE_SSL=false
DJANGO_EMAIL_TIMEOUT=10
DJANGO_DEFAULT_FROM_EMAIL=your-account@example.com
DJANGO_NOTIFY_EMAIL=contact@example.com
```

Ejemplo comun con Gmail:

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DJANGO_EMAIL_HOST=smtp.gmail.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=your-account@gmail.com
DJANGO_EMAIL_HOST_PASSWORD=your-app-password
DJANGO_EMAIL_USE_TLS=true
DJANGO_EMAIL_USE_SSL=false
DJANGO_DEFAULT_FROM_EMAIL=your-account@gmail.com
DJANGO_NOTIFY_EMAIL=your-account@gmail.com
```

Si usas Gmail, debes generar una app password y no reutilizar tu contrasena normal.

## Ejecucion en local

1. Entra en la carpeta de la aplicacion:

```bash
cd ProductivitySite
```

2. Crea y activa un entorno virtual:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install .
```

4. Crea tu fichero `.env` a partir de `.env.example` y ajusta los valores que necesites.

```bash
cp .env.example .env
```

El proyecto carga automaticamente el fichero `.env` tanto en ejecucion local como con Docker Compose. Para desarrollo local, revisa especialmente `DJANGO_SECRET_KEY` y `SQLITE_PATH`.

5. Ejecuta migraciones:

```bash
python manage.py migrate
```

6. Arranca el servidor:

```bash
python manage.py runserver
```

La aplicacion quedara disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Ejecucion con Docker Compose

Desde la raiz del repositorio:

1. Crea tu fichero `.env` a partir de `.env.example` y ajusta los valores si lo necesitas.

2. Construye y levanta los servicios:

```bash
docker compose up --build
```

3. Abre la aplicacion en [http://127.0.0.1:8080](http://127.0.0.1:8080) o en el puerto indicado por `APP_PORT`.

Detalles del despliegue en Docker:

- El servicio `web` se construye desde `ProductivitySite/Dockerfile`
- Durante la build se instalan `pip`, `setuptools` y `wheel`, y despues las dependencias del proyecto desde `pyproject.toml`
- Al arrancar, ejecuta `python manage.py migrate`
- La base de datos SQLite se persiste en un volumen Docker usando `SQLITE_PATH=/data/db.sqlite3`
- Docker Compose lee el fichero `.env` de la raiz del repositorio para interpolar valores
- El contenedor solo recibe las variables que `docker-compose.yml` expone en `environment`
- Si `DJANGO_EMAIL_BACKEND` usa el backend de consola, los mensajes del formulario de contacto apareceran en `docker compose logs`

### Correo en Docker

Para que el formulario de contacto envie correos desde Docker, no basta con definir las variables SMTP en `.env`: tambien deben estar expuestas en `docker-compose.yml`. Este proyecto ya las reenvia al servicio `web`.

El flujo correcto es:

1. Crear `.env` desde `.env.example`
2. Rellenar las variables SMTP en `.env`
3. Levantar el proyecto con `docker compose up --build`

Ejemplo minimo para SMTP real en Docker:

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DJANGO_EMAIL_HOST=smtp.gmail.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=your-account@gmail.com
DJANGO_EMAIL_HOST_PASSWORD=your-app-password
DJANGO_EMAIL_USE_TLS=true
DJANGO_EMAIL_USE_SSL=false
DJANGO_DEFAULT_FROM_EMAIL=your-account@gmail.com
DJANGO_NOTIFY_EMAIL=your-account@gmail.com
```

Si quieres probar el formulario sin enviar correos reales, deja:

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

En ese caso, el contenido del mensaje aparecera en los logs del contenedor:

```bash
docker compose logs -f
```

Para detener los contenedores:

```bash
docker compose down
```

Para detenerlos eliminando tambien el volumen de datos:

```bash
docker compose down -v
```

## Administracion de Django

Para acceder al panel de administracion de Django necesitas crear un superusuario.

1. Asegurate de que los contenedores estan levantados:

```bash
docker compose up -d
```

2. Crea el usuario administrador dentro del contenedor:

```bash
docker compose exec web python manage.py createsuperuser
```

3. Introduce el nombre de usuario, correo y contrasena cuando Django lo pida.

4. Accede al panel en [http://127.0.0.1:8080/admin](http://127.0.0.1:8080/admin) e inicia sesion con ese usuario.

Si estas ejecutando la aplicacion en local sin Docker, el comando equivalente es:

```bash
cd ProductivitySite
python manage.py createsuperuser
```

## Despliegue

Para un despliegue controlado, el flujo recomendado es:

1. Definir variables de entorno reales para el entorno destino, especialmente `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false` y `DJANGO_ALLOWED_HOSTS`.
2. Construir la imagen:

```bash
docker compose build
```

3. Arrancar la aplicacion:

```bash
docker compose up -d
```

4. Ver logs si hace falta:

```bash
docker compose logs -f
```

## Notas

- La configuracion actual usa SQLite. Para un despliegue de produccion mas robusto, conviene migrar a una base de datos gestionada como PostgreSQL.
- El contenedor usa `runserver`, que es suficiente para desarrollo. Para produccion, seria mejor usar un servidor WSGI como Gunicorn.
