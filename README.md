# FastAPI REST API Tutorial

Este repositorio es un ejemplo de una API RESTful implementada con FastAPI. Incluye conceptos como DDD, Vertical Slices, Inyección de Dependencias, Seguridad, Swagger y más.


## Tutoriales en Video

### Video 1: Introducción y Configuración Inicial
En este vídeo tratamos la versión inicial, básica pero funcional, aunque claro, no hay seguridad ni ninguna de las técnicas que se han desarrollado a posteriori.

- [Ver en YouTube](https://youtu.be/9oUlpbcC8BQ)
- [Código correspondiente a este vídeo](https://github.com/jgcarmona-com/fastapi-rest-api-tutorial/tree/fa96b75)

### Vídeo 2: 
TODO: grabar y publicar el vídeo.

## Características

- **FastAPI**: Framework web moderno y de alto rendimiento para construir APIs con Python 3.7+ basado en estándares como OpenAPI y JSON Schema.
- **RESTful API**: Diseño de la API siguiendo los principios REST.
- **Domain-Driven Design (DDD)**: Separación clara de las responsabilidades y lógica del dominio.
- **Vertical Slices**: Organización del código por características en lugar de por capas técnicas.
- **Inyección de Dependencias**: Gestión e inyección de dependencias con FastAPI.
- **Seguridad**: Implementación de autenticación y autorización.
- **Swagger**: Documentación interactiva de la API.

## Estructura del Proyecto

```
qna_api/
│
├── auth/
│   ├── models.py
│   ├── routes.py
│   └── service.py
│
├── core/
│   ├── base_repository.py
│   ├── config.py
│   ├── constants.py
│   ├── database.py
│   └── logging.py
│
├── domain/
│   ├── answer.py
│   ├── question.py
│   └── user.py
│
├── questions/
│   ├── models.py
│   ├── repositories.py
│   ├── routes.py
│   └── services.py
│
└── user/
    ├── controller.py
    ├── models.py
    ├── repository.py
    └── service.py
```

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/jgcarmona-com/fastapi-rest-api-tutorial.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd fastapi-rest-api-tutorial
    ```

3. Crea un entorno virtual y activa:
    ```bash
    python -m venv .venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

5. Configura las variables de entorno:
    Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=sqlite:///./sql_app.db
    INITIAL_ADMIN_USERNAME=admin
    INITIAL_ADMIN_EMAIL=admin@example.com
    INITIAL_ADMIN_PASSWORD=admin
    ```

6. Inicia la aplicación:
    Desde vscode selecciona la opción local o docker y ejecútalo.

## Uso

1. Visita `http://127.0.0.1:8000` y te redirigirá a /doc para ver la documentación interactiva de la API (swagger).
2. Visita `http://127.0.0.1:8000/redoc` para ver la documentación alternativa de la API.

## Enlaces útiles

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Repositorio en GitHub](https://github.com/jgcarmona-com/fastapi-rest-api-tutorial)

## Versiones anteriores

- [Versión del primer vídeo](https://github.com/jgcarmona-com/fastapi-rest-api-tutorial/tree/fa96b75)
- [Primer vídeo en YouTube](https://youtu.be/9oUlpbcC8BQ)
