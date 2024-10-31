
# 🎫 Event Tickets API

API para la gestión de eventos y boletos, construida con Flask y MySQL, y completamente dockerizada para facilitar su despliegue y pruebas. Sigue los pasos a continuación para configurar y ejecutar la aplicación, y consulta el [Diseño Técnico en Notion](https://brunopunki.notion.site/Event-Ticketing-API-Dise-o-T-cnico-12ed4324f98780dea4eae30ffeb1002d) para una visión detallada del sistema.

## 📋 Requisitos Previos
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## ⚙️ Configuración y Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/bruno-orozco/event-tickets-api.git
   cd event-tickets-api
   ```

2. **Ejecutar la aplicación**:
   ```bash
   docker-compose up --build
   ```
   La API estará disponible en `http://localhost:5000/graphql/v1`.


3. **Detener la aplicación**:
   ```bash
   docker-compose down
   ```


## 🧪 Ejecución de Pruebas Unitarias

Para ejecutar las pruebas unitarias, utiliza el contenedor de pruebas `test`:

1. Inicia el contenedor de pruebas:
   ```bash
   docker-compose up test
   ```
   Esto ejecutará las pruebas definidas en los directorios `app/events/unittest` y `app/tickets/unittest`.


## 📂 Estructura del Proyecto

La arquitectura de este proyecto sigue el paradigma Modelo-Vista-Controlador (MVC) para mantener una separación clara entre la lógica de datos, la lógica de negocio y la interfaz.

```
├── app
│   ├── modules               # Módulos individuales con responsabilidad única
│   │   ├── controllers       # Controladores para la lógica de negocio de eventos
│   │   ├── graphql           # Definiciones de consultas y mutaciones de eventos
│   │   ├── models            # Modelos de datos de eventos
│   │   ├── schemas           # Esquemas GraphQL y validaciones de eventos
│   │   ├── services          # Servicios específicos para eventos
│   │   └── unittest          # Pruebas unitarias para la lógica de eventos
├── tests
│   └── unit                  # Pruebas unitarias para funciones individuales
│
├── Dockerfile                # Configuración de la imagen Docker
├── docker-compose.yml        # Configuración de servicios y contenedores
├── requirements.txt          # Dependencias del proyecto
└── manage.py                 # Punto de entrada para ejecutar la aplicación

```