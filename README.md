# Invera ToDo-List Challenge (Python/Django Jr-SSr)

## Objetivos:

El usuario de la aplicación tiene que ser capaz de:

- Autenticarse
- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

## Requisitos Previos

Antes de comenzar, verifica tener los siguientes requerimientos:

* Instala [Docker](https://www.docker.com/get-started/) 
* (Opcional) Si deseas ejecutarlo localmente, debes tener instalado `python 3.10+`
  
  ```sh
  python3.10 --version
  ```
## Modo de Uso

1. Primero, ejecutalo siguiendo los pasos de [Ejecución en Docker](#ejecución-en-docker).
2. La API expone los siguientes endpoints:
    1. Un POST endpoint para [crear cuenta](#crear-cuenta) en: `http://127.0.0.1:8000/api/register/`
    2. Un POST endpoint para [login](#login) en: `http://127.0.0.1:8000/api/login/`
    3. Un POST endpoint para [refrescar token](#refrescar-token) en: `http://127.0.0.1:8000/api/token/refresh/`
    4. Un GET endpoint to [listar tareas del usuario](#listar-tareas) en: `http://127.0.0.1:8000/api/tasks/`
    5. Un POST endpoint para [crear tarea](#crear-tarea) en: `http://127.0.0.1:8000/api/tasks/`
    6. Un GET endpoint para [obtener una tarea](#obtener-tarea) en: `http://127.0.0.1:8000/api/tasks/<id>`
    7. Un PUT y un PATCH endpoint para [modificar una tarea](#modificar-tarea) en: `http://127.0.0.1:8000/api/tasks/<id>/`
    8. Un PATCH endpoint para [finalizar una tarea](#finalizar-tarea) en: `http://127.0.0.1:8000/api/tasks/<id>/done/`
    9. Un DELETE endpoint para [eliminar una tarea](#eliminar-tarea) en: `http://127.0.0.1:8000/api/tasks/<id>/`


> Además, los siguientes endopoints están disponibles para consultar documentación:
> - `http://127.0.0.1:8000/api/swagger/`
> - `http://127.0.0.1:8000/api/redoc/`

### Crear cuenta
* Endpoint: `POST` `api/register/`
* Payload:
 ```json
{
    "username": "string",
    "email": "user@example.com",
    "password": "string"
}
```
> `email` es opcional
* Response:
    - Status code: 201
```json
{
    "id": 0,
    "username": "string",
    "email": "user@example.com",
    "password": "string"
}
```


### Login
* Endpoint: `POST` `api/login/`
* Payload:
```json
{
    "username": "string",
    "password": "string"
}
```
* Response:
    - Status code: 200
```json
{
    "refresh": "token-key",
    "access": "token-key"
}
```

### Refrescar token
* Endpoint: `POST` `api/token/refresh/`
* Payload:
```json
{
    "refresh": "token-key"
}
```
* Response:
    - Status code: 200
```json
{
    "access": "token-key"
}
```

### Listar tareas
* Endpoint: `GET` `api/tasks/`
* Query parameters:
    * `content` = busca las tareas que tengan esa cadena de caracteres en el título o en la descripción.
    * `date` = busca las tareas que hayan sido creadas ese dia. Formato `YYYY-MM-DD`
* Response:
    - Status code: 200
```json
[
  {
    "id": 0,
    "title": "string",
    "description": "string",
    "done": false,
    "created_at": "2024-03-03T14:15:22Z"
  }
  ...
]
```

### Crear tarea
* Endpoint: `POST` `api/tasks/`
* Payload:
```json
{
    "title": "string",
    "description": "string"
}
```
> `description` is opcional
* Response:
    - Status code: 201
```json
{
    "id": 0,
    "title": "string",
    "description": "string",
    "done": false,
    "created_at": "2024-03-03T14:15:22Z"
}
```

### Obtener tarea
* Endpoint: `GET` `api/tasks/<int:id>/`
* Response:
    - Status code: 200
```json
{
    "id": 0,
    "title": "string",
    "description": "string",
    "done": false,
    "created_at": "2024-03-03T14:15:22Z"
}
```

### Modificar tarea
* Endpoint: `PUT` `api/tasks/<int:id>/`
* Payload: 
```json
{
    "title": "string",
    "description": "string"
}
```
* Response:
    - Status code: 200
```json
{
    "id": 0,
    "title": "string",
    "description": "string",
    "done": false,
    "created_at": "2024-03-03T14:15:22Z"
}
```

-------
#### Modificar parcialmente una tarea
* Endpoint: `PATCH` `api/tasks/<int:id>/`
* Payload: 
```json
{
    "description": "string"
}
```
* Response:
    - Status code: 200
```json
{
    "id": 0,
    "title": "string",
    "description": "string",
    "done": false,
    "created_at": "2024-03-03T14:15:22Z"
}
```

### Finalizar tarea
* Endpoint: `PATCH` `api/tasks/<int:id>/done/`
* Response:
    - Status code: 204 -> si la tarea cambió al estado `done`
    - Status code: 304 -> si la tarea ya estaba en estado `done`


### Eliminar tarea
* Endpoint: `DELETE` `api/tasks/<int:id>/`
* Response:
    - Status code: 204

### Ejecución en Docker

1. Desde la consola o terminal cloná este repositorio

```sh
  git clone https://github.com/gabisluciana/todo-challenge.git
  ```

2. Ubicate en la carpeta `todo-challenge` creada
```sh
  cd todo-challenge/
  ```

3. Ejecuta el siguiente comnando para crear y correr la imagen en Docker

```sh
  docker-compose up --build   
  ```

4. Podés probar los endpoints desde la interfaz de Diango Rest Framework navegando los endpoints o utilizar la herramienta que prefieras como:

- [Postman](https://www.postman.com/)
- [curl](https://curl.se/)
- [Insomnia](https://insomnia.rest/download)


### Ejecución de pruebas en Docker

* Con el repositorio clonado y ubicado en la carpeta correspondiente como se explica en la sección [Ejecución en Docker](#ejecución-en-docker), ejecutar el siguiente comando:
Ejecuta el siguiente comnando para crear y correr la imagen en Docker

```sh
  docker-compose -f docker-compose.test.yml up --build               
  ```

Las pruebas se ejecutarán y podrás ver el resultado en la consola.
