# Backend REST API para Gestion Educativa y Admisiones

## Datos del Proyecto

**Universidad:** UTE  
**Escuela:** Tecnologias  
**Carrera:** Desarrollo de Software  
**Materia:** Programacion IV  
**Estudiante:** Alex Macias  
**Docente:** Ing. Francisco Higuera  
**Fecha:** 04/06/2026

---

## Resumen General

Este proyecto implementa una API REST para administrar procesos academicos y de admision en una institucion educativa. La solucion esta construida con **Django**, **Django REST Framework** y autenticacion mediante **JWT** usando SimpleJWT.

El sistema usa **PostgreSQL** como base de datos principal para las entidades transaccionales y **MongoDB** para almacenar informacion documental relacionada con asistencias y actividades academicas.

La API permite gestionar facultades, carreras, docentes, estudiantes, materias, matriculas, notas, asistencias y actividades. Ademas, incluye filtros, busqueda, ordenamiento, paginacion y control de permisos segun el tipo de usuario.

---

## Tecnologias Utilizadas

- **Python 3.13+**
- **Django 6**
- **Django REST Framework**
- **SimpleJWT**
- **PostgreSQL**
- **MongoDB**
- **django-filter**
- **django-cors-headers**
- **Gunicorn**
- **uv** o **pip** para gestion de dependencias

---

## Funcionalidades Principales

- Registro de usuarios.
- Login con tokens JWT.
- Refresh de token de acceso.
- Logout con invalidacion de refresh token.
- CRUD de facultades.
- CRUD de carreras.
- CRUD de docentes.
- CRUD de estudiantes.
- CRUD de materias.
- CRUD de matriculas.
- CRUD de notas academicas.
- Registro y consulta de asistencias en MongoDB.
- Registro y consulta de actividades academicas en MongoDB.
- Paginacion automatica de resultados.
- Filtros por campos importantes.
- Busqueda por texto en recursos seleccionados.
- Ordenamiento por parametros de consulta.
- Validaciones de negocio en modelos y serializers.
- Coleccion de Postman lista para pruebas.

---

## Arquitectura del Proyecto

El backend esta organizado como una aplicacion Django llamada `gestion`, dentro de un proyecto principal llamado `config`.

Estructura principal:

```text
Backend_gestion_educativa/
+-- config/
|   +-- settings.py
|   +-- urls.py
|   +-- asgi.py
|   +-- wsgi.py
+-- gestion/
|   +-- models.py
|   +-- serializers.py
|   +-- views.py
|   +-- urls.py
|   +-- permissions.py
|   +-- auth_views.py
|   +-- asistencia_views.py
|   +-- actividades_views.py
|   +-- mongo_serializers.py
+-- deploy/
+-- manage.py
+-- pyproject.toml
+-- Procfile
+-- runtime.txt
+-- gestion_educativa_postman.json
```

---

## Bases de Datos

### PostgreSQL

PostgreSQL se utiliza para almacenar la informacion principal del sistema:

- Facultades
- Carreras
- Docentes
- Estudiantes
- Materias
- Matriculas
- Notas
- Usuarios de Django

### MongoDB

MongoDB se utiliza para informacion documental y flexible:

- Asistencias
- Actividades academicas

---

## Instalacion Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlexMa77/AdmisionesApi.git
cd Backend_gestion_educativa
```

### 2. Crear el entorno virtual

Opcion recomendada con `uv`:

```bash
uv venv
uv sync
.venv\Scripts\Activate.ps1
```

Opcion alternativa con `pip`:

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install .
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raiz del proyecto con una configuracion similar:

```env
DEBUG=True
SECRET_KEY=django-insecure-cambiar-en-produccion
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=gestion_educativa_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

TEST_DB_NAME=gestion_educativa_test_db

MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DB=gestion_educativa_db

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=False
```

### 4. Crear la base de datos en PostgreSQL

Antes de ejecutar migraciones, crea la base de datos:

```sql
CREATE DATABASE gestion_educativa_db;
```

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

Servidor local:

```text
http://127.0.0.1:8000/
```

---

## Autenticacion y Seguridad

La API usa autenticacion mediante **JWT**.

Para iniciar sesion, envia una peticion `POST` a:

```text
/api/auth/login/
```

Body de ejemplo:

```json
{
  "username": "admin",
  "password": "mi_password"
}
```

Respuesta esperada:

```json
{
  "refresh": "token_refresh",
  "access": "token_access"
}
```

Para consumir endpoints protegidos, agrega el token de acceso en la cabecera:

```http
Authorization: Bearer <token_access>
```

Permisos generales:

- Los endpoints publicos pueden consultarse sin token.
- Los endpoints autenticados requieren un usuario con token JWT valido.
- Las operaciones de escritura sobre entidades principales requieren usuario administrador (`is_staff = True`).

---

## Endpoints de Autenticacion

| Recurso | Endpoint | Metodo | Acceso |
| :--- | :--- | :--- | :--- |
| Registro | `/api/auth/register/` | `POST` | Publico |
| Login | `/api/auth/login/` | `POST` | Publico |
| Refresh token | `/api/auth/refresh/` | `POST` | Publico |
| Logout | `/api/auth/logout/` | `POST` | Autenticado |

---

## Endpoints Principales

Todos los endpoints funcionales usan el prefijo `/api/`.

| Recurso | Endpoint | Metodos | Acceso |
| :--- | :--- | :--- | :--- |
| Salud del sistema | `/api/health/` | `GET` | Publico |
| Facultades | `/api/facultades/` | `GET`, `POST` | `GET` publico, `POST` admin |
| Facultad detalle | `/api/facultades/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` publico, otros admin |
| Carreras | `/api/carreras/` | `GET`, `POST` | `GET` publico, `POST` admin |
| Carrera detalle | `/api/carreras/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` publico, otros admin |
| Docentes | `/api/docentes/` | `GET`, `POST` | `GET` autenticado, `POST` admin |
| Docente detalle | `/api/docentes/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` autenticado, otros admin |
| Estudiantes | `/api/estudiantes/` | `GET`, `POST` | `GET` autenticado, `POST` admin |
| Estudiante detalle | `/api/estudiantes/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` autenticado, otros admin |
| Materias | `/api/materias/` | `GET`, `POST` | `GET` autenticado, `POST` admin |
| Materia detalle | `/api/materias/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` autenticado, otros admin |
| Matriculas | `/api/matriculas/` | `GET`, `POST` | `GET` autenticado, `POST` admin |
| Matricula detalle | `/api/matriculas/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` autenticado, otros admin |
| Notas | `/api/notas/` | `GET`, `POST` | `GET` autenticado, `POST` admin |
| Nota detalle | `/api/notas/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | `GET` autenticado, otros admin |
| Asistencias | `/api/asistencias/` | `GET`, `POST` | Autenticado |
| Asistencia detalle | `/api/asistencias/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Autenticado |
| Actividades | `/api/actividades/` | `GET`, `POST` | Autenticado |
| Actividad detalle | `/api/actividades/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE` | Autenticado |

---

## Filtros, Busqueda y Ordenamiento

La API soporta parametros de consulta para facilitar el consumo desde frontend o herramientas como Postman.

Ejemplos:

```text
/api/facultades/?search=ingenieria
/api/carreras/?facultad=1&activo=true
/api/estudiantes/?semestre_actual=3
/api/materias/?carrera=1&semestre=2
/api/matriculas/?periodo=2026-1
/api/notas/?aprobado=true
/api/asistencias/?materia_id=1&fecha=2026-06-04
/api/actividades/?tipo=tarea&activo=true
```

Tambien se puede ordenar en endpoints compatibles:

```text
/api/materias/?ordering=semestre
/api/notas/?ordering=-nota_final
```

---

## Campos Principales por Entidad

### Facultad

- `nombre`
- `codigo`
- `descripcion`
- `activo`

### Carrera

- `facultad`
- `nombre`
- `codigo`
- `duracion_semestres`
- `activo`

### Docente

- `user`
- `cedula`
- `telefono`
- `especialidad`
- `activo`

### Estudiante

- `user`
- `carrera`
- `cedula`
- `telefono`
- `semestre_actual`
- `activo`

### Materia

- `carrera`
- `docente`
- `nombre`
- `codigo`
- `creditos`
- `semestre`
- `activo`

### Matricula

- `estudiante`
- `materia`
- `periodo`
- `estado`

Estados validos:

- `activa`
- `retirada`
- `finalizada`

### Nota

- `matricula`
- `parcial1`
- `parcial2`
- `examen_final`

Campos calculados automaticamente:

- `nota_final`
- `aprobado`

### Asistencia

- `matricula_id`
- `materia_id`
- `estudiante_id`
- `fecha`
- `presente`
- `observacion`

### Actividad

- `materia_id`
- `titulo`
- `descripcion`
- `tipo`
- `fecha_limite`
- `creado_por`
- `activo`

Tipos validos:

- `tarea`
- `examen`
- `proyecto`
- `anuncio`

---

## Reglas de Negocio

1. La duracion de una carrera debe estar entre 1 y 12 semestres.
2. La cedula de docentes debe ser unica.
3. La cedula de estudiantes debe ser unica.
4. El semestre actual del estudiante debe estar entre 1 y 12.
5. Los creditos de una materia deben estar entre 1 y 10.
6. El semestre de una materia debe estar entre 1 y 12.
7. Un estudiante no puede matricularse dos veces en la misma materia durante el mismo periodo.
8. Cada matricula puede tener una sola nota asociada.
9. La nota final se calcula automaticamente cuando existen `parcial1`, `parcial2` y `examen_final`.
10. Un estudiante aprueba si su nota final es mayor o igual a 7.00.

---

## Paginacion

Los endpoints principales utilizan paginacion por pagina. El tamano configurado por defecto es de 10 registros por pagina.

Ejemplo:

```text
/api/estudiantes/?page=2
```

---

## Pruebas con Postman

El proyecto incluye una coleccion de Postman:

```text
gestion_educativa_postman.json
```

Esta coleccion permite probar:

- Registro de usuario.
- Login y almacenamiento de token.
- Refresh de token.
- Logout.
- Operaciones CRUD principales.
- Flujo de creacion de datos relacionados.
- Consultas autenticadas.
- Pruebas de asistencias y actividades.

Para usarla:

1. Importa el archivo en Postman.
2. Configura la URL base del servidor.
3. Ejecuta login para obtener el token.
4. Prueba los endpoints protegidos usando el token generado.

---

## Pruebas Automatizadas

El proyecto incluye pruebas basicas con Django TestCase.

Para ejecutarlas:

```bash
python manage.py test
```

Actualmente se valida el endpoint de salud del sistema:

```text
/api/health/
```

---

## Despliegue

El proyecto incluye archivos base para despliegue:

- `Procfile` para ejecutar con Gunicorn.
- `runtime.txt` para definir version de Python.
- `deploy/nginx.conf` como referencia de Nginx.
- `deploy/gunicorn.service` como referencia de servicio Gunicorn.

Comando usado en `Procfile`:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Para produccion se recomienda:

- Usar `DEBUG=False`.
- Configurar un `SECRET_KEY` seguro.
- Definir correctamente `ALLOWED_HOSTS`.
- Configurar PostgreSQL y MongoDB en servidores persistentes.
- Servir archivos estaticos desde `STATIC_ROOT`.
- Configurar HTTPS.

---

## Estado del Proyecto

El backend se encuentra funcional para pruebas locales y presentacion academica. Incluye autenticacion, persistencia relacional, persistencia documental, reglas de negocio, endpoints REST y coleccion de pruebas con Postman.

Como mejoras futuras se pueden agregar:

- Mas pruebas automatizadas para modelos y endpoints.
- Documentacion Swagger/OpenAPI.
- Roles mas detallados para estudiantes, docentes y administradores.
- Validaciones adicionales para procesos de admision.
- Panel administrativo personalizado.
