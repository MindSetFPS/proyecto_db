# Framework

Elegiremos el framework de Django por su rapidez, facilidad de implementación, extensiones y compatibilidad.
Creamos un entorno vitual.
Posteriormente instalamos django.
Procedemos a crear el proyecto, y luego a crear nuestra app.
Ahora creamos un super usuario para poder manejar los datos de la base de datos.
Creamos la conexión a la base de datos.
Creamos nuestras tablas.
Creamos nuestras vistas.
Creamos nuestras rutas.

El proyecto require un archivo .env con la siguiente estructura:

```
MP_ACCESS_TOKEN=key
MP_WEBHOOK_SECRETE_KEY=key
```

Para hacer los test de systema contamos con selenium que nos permitirá probar nuestra aplicación desde los navegadores chrome y firefox. Para hacer uso de ellos deberemos instalar la librería de python correspondiente, y descargar los binarios de los controladores de cada respectivo navegador.