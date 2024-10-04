
### **Reporte de Prueba de Integración: `UserPrivacyTest` - Prueba de Privacidad de Usuarios**

**Nombre de la Función:** `user_data`  
**Fecha de la Prueba:** 4 de octubre de 2024  
**Responsable:** Jesús Sánchez Sosme  
**Tecnología:** Django (Python)  
**Ubicación del Código:** `user_data.py` en el módulo `shopApp/views`  
**Nombre del Archivo de Prueba:** `test_privacy.py`

---

#### **1. Análisis de los Requisitos y Especificaciones del Software**
El objetivo de la funcionalidad `user_data` es asegurar que los usuarios solo puedan acceder a sus propios datos, garantizando que ningún usuario pueda ver o modificar la información de otros usuarios. La vista debe cumplir con los siguientes requisitos:

- **Usuarios autenticados**: Solo pueden acceder a su propia información.
- **Usuarios no autenticados**: No pueden acceder a la información de usuarios registrados.
- **Verificación de permisos**: Si un usuario intenta acceder a los datos de otro, debe recibir un código 403 (acceso prohibido).

**Principio Aplicado: Testing muestra la presencia de defectos, no su ausencia**  
El análisis de esta prueba se centró en verificar la segregación correcta de permisos entre usuarios. La prueba busca demostrar la presencia de defectos en la gestión de permisos si no se siguen correctamente las reglas definidas.

---

#### **2. Identificación de Escenarios y Condiciones de Prueba**
Se identificaron los siguientes escenarios clave para probar la vista `user_data`:

- **Escenario 1**: Un usuario autenticado intenta acceder a los datos de otro usuario.
- **Escenario 2**: Un usuario no autenticado intenta acceder a los datos de un usuario registrado.
- **Escenario 3**: Un usuario autenticado accede correctamente a sus propios datos.

**Principio Aplicado: Las pruebas exhaustivas son imposibles**  
Se seleccionaron los casos más relevantes, como el manejo de permisos y accesos incorrectos, en lugar de probar todas las combinaciones posibles. Esto permite optimizar el tiempo de prueba y centrarse en las áreas más críticas.

---

#### **3. Definición de Objetivos y Alcance de las Pruebas**
El objetivo principal de estas pruebas es verificar que los usuarios solo puedan acceder a su propia información y que los accesos no autorizados sean correctamente bloqueados con un código de error 403. Las condiciones a validar son:

- Los usuarios autenticados solo pueden ver sus propios datos.
- Los usuarios no autenticados no pueden ver datos de usuarios registrados.
- Los intentos de acceso no autorizado deben devolver un error 403.

**Principio Aplicado: Testing temprano ahorra tiempo y dinero**  
La detección de problemas de permisos y seguridad en etapas tempranas de desarrollo es clave para evitar defectos críticos en producción. Esto ahorra recursos y evita vulnerabilidades graves de seguridad.

---

#### **4. Diseño y Escritura de Casos de Prueba Claros y Concisos**
Se diseñaron los siguientes casos de prueba para cubrir los escenarios clave:

1. **`test_user_cannot_access_other_user_data`**:
   - **Precondiciones**: Dos usuarios (`user1` y `user2`) están registrados en el sistema.
   - **Acciones**:
     1. Iniciar sesión como `user1`.
     2. Intentar acceder a los datos de `user2` mediante la vista `user_data`.
   - **Resultado esperado**: El sistema debe devolver un código 403 (acceso prohibido).

2. **`test_unregistered_cannot_access_user_data`**:
   - **Precondiciones**: Un usuario no registrado intenta acceder a los datos de `user1`.
   - **Acciones**:
     1. Realizar una solicitud `GET` a la vista `user_data` sin estar autenticado.
   - **Resultado esperado**: El sistema debe redirigir al formulario de inicio de sesión.
   **Aqui esta la imagen de que se ejecuto correctamente**
   ![alt text](image-2.png)
   **Aqui cuando no se ejecuto bien y me dio los errores**
   ![alt text](image-3.png)

**Principio Aplicado: El testing depende del contexto**  
Cada prueba se ajusta al contexto de privacidad y control de acceso, asegurando que se verifiquen las condiciones que podrían ser vulnerables, como el acceso a datos no autorizados.

---

#### **5. Revisión y Refinamiento de Casos de Prueba**
Los casos de prueba fueron revisados para garantizar que cubran todas las condiciones críticas de acceso:

- **Verificación de permisos**: Se asegura que el código 403 se devuelva en casos de acceso no autorizado.
- **Manejo de autenticación**: Se comprueba que los usuarios no autenticados sean redirigidos correctamente a la página de inicio de sesión.

**Principio Aplicado: El agrupamiento de defectos se presenta de manera desproporcionada**  
Las pruebas se enfocan en las áreas donde es más probable que se agrupe la mayoría de los errores, como la autenticación y los permisos de acceso.

---

#### **6. Ejecución de Pruebas y Reporte de Defectos**
Las pruebas se ejecutaron utilizando `unittest` en Django, con los siguientes resultados:

1. **`test_user_cannot_access_other_user_data`**: **PASSED**
   - El sistema devolvió correctamente un código 403 cuando `user1` intentó acceder a los datos de `user2`.

2. **`test_unregistered_cannot_access_user_data`**: **PASSED**
   - El sistema redirigió correctamente a la vista de inicio de sesión cuando un usuario no autenticado intentó acceder a los datos de `user1`.

**Principio Aplicado: La paradoja del pesticida**  
Se refinaron los casos de prueba para garantizar que no se repitan las mismas pruebas de manera innecesaria. Esto permite identificar nuevos defectos y prevenir problemas en futuras iteraciones.

---

#### **7. Actualización y Mantenimiento de los Casos de Prueba a lo Largo del Ciclo de Vida del Software**
Los casos de prueba se mantendrán actualizados conforme evolucione la lógica del sistema, añadiendo nuevos escenarios que contemplen el acceso a cuentas inactivas o eliminadas. Esto asegura una cobertura constante a lo largo del ciclo de vida del software.

**Principio Aplicado: La ausencia de errores no significa un software útil**  
Aunque las pruebas pasaron sin errores, se realizaron recomendaciones adicionales para mejorar la usabilidad y la claridad de los mensajes de error que se muestran cuando un usuario recibe un código 403.

---

### **Conclusión**
Las pruebas de privacidad demostraron que el sistema maneja correctamente la segregación de acceso a los datos de usuario, garantizando que los usuarios autenticados solo puedan ver sus propios datos y que los accesos no autorizados sean correctamente bloqueados. Los resultados fueron satisfactorios y el código está listo para producción, con la implementación correcta de los principios de testing.

