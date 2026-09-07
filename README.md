# Device Systems API

API REST desarrollada con **FastAPI** para la gestión de usuarios del sistema `device_systems`.

Este proyecto fue desarrollado como parte del reto integrador **Fundamentos de FastAPI**, aplicando modelos Pydantic, validaciones, parámetros de ruta, parámetros de consulta, códigos HTTP, modelos de respuesta y headers personalizados.

---

## Tecnologías utilizadas

* Python
* FastAPI
* Pydantic
* Uvicorn
* uv
* Swagger UI

---

## Estructura del proyecto

```text
device_systems/
│
├── app/
│   ├── main.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   └── routes/
│       └── user_routes.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Instalación

### 1. Clonar o descargar el proyecto

Ubicarse en la carpeta del proyecto:

```powershell
cd device_systems
```

### 2. Instalar las dependencias

Si el proyecto utiliza `uv`, ejecutar:

```powershell
uv sync
```

---

## Ejecución

Para iniciar el servidor:

```powershell
uv run uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

---

## Documentación automática

FastAPI proporciona documentación automática mediante Swagger UI.

Abrir:

```text
http://127.0.0.1:8000/docs
```

También se puede consultar la documentación alternativa:

```text
http://127.0.0.1:8000/redoc
```

---

# Endpoints

## GET `/users`

Obtiene todos los usuarios registrados.

Ejemplo:

```http
GET /users
```

---

## GET `/users/{user_id}`

Obtiene un usuario utilizando su ID.

Ejemplo:

```http
GET /users/1
```

Si el usuario no existe, la API devuelve:

```json
{
    "detail": "Usuario no encontrado"
}
```

Código HTTP:

```text
404 Not Found
```

---

## GET `/users?role=admin`

Filtra los usuarios por rol.

Roles permitidos:

```text
admin
support
user
```

Ejemplo:

```http
GET /users?role=admin
```

---

## GET `/users?is_active=true`

Filtra los usuarios según su estado.

Para usuarios activos:

```http
GET /users?is_active=true
```

Para usuarios inactivos:

```http
GET /users?is_active=false
```

También es posible combinar filtros:

```http
GET /users?role=admin&is_active=true
```

---

# POST `/users`

Registra un nuevo usuario.

Ejemplo de solicitud:

```json
{
    "name": "Ana Torres",
    "email": "ana@gmail.com",
    "role": "support",
    "is_active": true
}
```

Respuesta:

```json
{
    "id": 4,
    "name": "Ana Torres",
    "email": "ana@gmail.com",
    "role": "support",
    "is_active": true
}
```

Código HTTP:

```text
201 Created
```

El ID es generado automáticamente por la API.

---

# Validaciones

## Nombre

El nombre es obligatorio y debe contener como mínimo tres caracteres.

Ejemplo incorrecto:

```json
{
    "name": "Jo",
    "email": "jo@gmail.com",
    "role": "user",
    "is_active": true
}
```

La API responde con:

```text
422 Unprocessable Entity
```

---

## Email

El correo debe tener un formato válido.

Ejemplo incorrecto:

```json
{
    "name": "Jorge",
    "email": "correo-invalido",
    "role": "user",
    "is_active": true
}
```

---

## Rol

Solamente se permiten:

```text
admin
support
user
```

Ejemplo incorrecto:

```json
{
    "name": "Jorge",
    "email": "jorge@gmail.com",
    "role": "manager",
    "is_active": true
}
```

---

## Correo duplicado

La API verifica que no exista otro usuario con el mismo correo.

Si se intenta registrar un correo existente:

```text
409 Conflict
```

Respuesta:

```json
{
    "detail": "El correo electrónico ya está registrado"
}
```

---

# Modelos Pydantic

El proyecto utiliza dos modelos principales.

### UserCreate

Modelo utilizado para recibir los datos de creación de un usuario:

```text
name
email
role
is_active
```

### UserResponse

Modelo utilizado para las respuestas:

```text
id
name
email
role
is_active
```

La separación entre estos modelos permite controlar los datos que recibe y devuelve la API.

---

# Headers personalizados

La API agrega los siguientes headers a las respuestas:

```text
X-App-Name: device_systems
X-API-Version: 1.0
```

Estos permiten identificar la aplicación y la versión de la API.

---

# Códigos HTTP utilizados

| Código | Descripción                       |
| ------ | --------------------------------- |
| 200    | Solicitud realizada correctamente |
| 201    | Usuario creado correctamente      |
| 404    | Usuario no encontrado             |
| 409    | Correo electrónico duplicado      |
| 422    | Datos enviados no válidos         |

---

# Pruebas

Las pruebas pueden realizarse utilizando:

* Swagger UI
* Postman
* Thunder Client

Se recomienda utilizar Swagger UI para comprobar rápidamente todos los endpoints:

```text
http://127.0.0.1:8000/docs
```

---

# Consideraciones

Actualmente los usuarios se almacenan temporalmente en una lista en memoria.

Esto significa que los usuarios creados se perderán cuando se detenga el servidor.

Para una aplicación en producción sería necesario utilizar una base de datos, pero para este reto se utiliza almacenamiento en memoria con el objetivo de trabajar los fundamentos de FastAPI y las API REST.

---

## Autor

Proyecto académico desarrollado para el reto:

**GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI**

Proyecto: `device_systems`
