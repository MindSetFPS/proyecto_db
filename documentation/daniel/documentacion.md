### **Reporte de Prueba: Escalabilidad

**Nombre de la Función:** `add_to_cart`
**Fecha de la Prueba:** 4 de Octubre de 2024  
**Responsable:** Daniel Ivan Escobar Vasquez
**Tecnología:** Django (Python)  
**Ubicación del Código:** nginx.conf, docker-compose.yml  
**Nombre del Archivo de Prueba:** `test_add_to_cart.py`

#### 1. **Análisis de los Requisitos y Especificaciones del Software**

El software debe ser capaz de manejar una carga de 10,000 usuarios simultáneos, distribuyendo las solicitudes entre dos hosts que ejecutan una instancia de la aplicación cada uno. NGINX gestionará la distribución de la carga. Si alguna instancia muestra pérdida de rendimiento, se espera que NGINX redirija las solicitudes de manera balanceada entre las dos instancias o incluso entre más si se agregan en el futuro. El sistema debe mantener un tiempo de respuesta aceptable (p. ej., < 500 ms por solicitud).

#### 2. **Identificación de Escenarios y Condiciones de Prueba**

Escenario 1: 10,000 usuarios simultáneos accediendo al servicio sin interrupciones.
Escenario 2: Degradación de rendimiento en uno de los hosts (simulación de falla parcial en una instancia).
Escenario 3: Redistribución automática de la carga entre ambas instancias.
Escenario 4: Validación del tiempo de respuesta promedio de las solicitudes bajo alta carga.
Escenario 5: Monitorización del rendimiento de NGINX y los hosts.

#### 3. **Definición de Objetivos y Alcance de las Pruebas**

Objetivo:

Validar que el servicio pueda manejar 10,000 usuarios simultáneos sin pérdida significativa de rendimiento.
Verificar la capacidad del balanceador de carga (NGINX) para distribuir equitativamente las solicitudes entre los dos hosts en condiciones normales y degradadas.
Alcance:

Se evaluará el rendimiento del sistema completo, incluyendo la redirección de tráfico, balanceo de carga y tiempos de respuesta.


#### 4. **Diseño y Escritura de Casos de Prueba Claros y Concisos**

- **Caso de prueba 1:**: Simulación de 10,000 usuarios simultáneos accediendo a la aplicación a través de NGINX
    - **Precondiciones:** NGINX configurado, 2 hosts activos
    - **Pasos:**
        1. Ejecutar la prueba de carga
        2. Monitorear los tiempos de respuesta y el uso de recursos en los hosts

    - **Resultado Esperado:** 
    NGINX balancea la carga uniformemente entre los dos hosts y los tiempos de respuesta son menores a 500 ms


#### 5. **Revisión y Refinamiento de Casos de Prueba**

#### 6. **Ejecución de Pruebas y Reporte de Defectos**

#### 7. **Actualización y Mantenimiento de los Casos de Prueba a lo Largo del Ciclo de Vida del Software**

### **Conclusión**
