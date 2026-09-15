# device_systems

## 1. Nombre del proyecto

**device_systems**

---

## 2. Descripción de la API

**device_systems** es una API REST desarrollada con **FastAPI** para la gestión de usuarios.

El proyecto corresponde a la evolución de una API inicial y actualmente cuenta con operaciones CRUD completas para los usuarios:

- Consultar todos los usuarios.
- Consultar un usuario por su ID.
- Crear nuevos usuarios.
- Actualizar completamente un usuario mediante PUT.
- Actualizar parcialmente un usuario mediante PATCH.
- Eliminar usuarios mediante DELETE.

La información de los usuarios se almacena temporalmente en una estructura en memoria que simula una base de datos.

La API también implementa:

- Validación de datos mediante Pydantic.
- Manejo de errores mediante `HTTPException`.
- Dependency Injection mediante `Depends()`.
- Documentación automática mediante Swagger UI y ReDoc.
- Códigos de estado HTTP apropiados para cada operación.

---

# 3. Tecnologías utilizadas

Las principales tecnologías utilizadas en el desarrollo de la API son:

| Tecnología | Uso |
|---|---|
| Python 3.13 | Lenguaje de programación |
| FastAPI | Framework para desarrollar la API REST |
| Uvicorn | Servidor para ejecutar la aplicación |
| Pydantic | Validación y definición de datos |
| Email-validator | Validación de correos electrónicos |
| UV | Administración de dependencias y ejecución del proyecto |
| Swagger UI | Documentación y pruebas de la API |
| ReDoc | Documentación alternativa de la API |

---

# 4. Estructura del proyecto

```text
device_systems/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routes/
│   │   └── user_routes.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── dependencies/
│   │   └── user_dependencies.py
│   │
│   └── data/
│       └── users_db.py
│
├── src/
│   └── device_systems/
│       └── __init__.py
│
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md