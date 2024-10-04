### **Reporte de Prueba de Integración: `RegistrationTest` - Prueba de Registro de Usuarios**

**Nombre de la Función:** `register`  
**Fecha de la Prueba:** 4 de octubre de 2024  
**Responsable:** Jesús Sánchez Sosme  
**Tecnología:** Django (Python)  
**Ubicación del Código:** `all.py` en el módulo `shopApp/views`  
**Nombre del Archivo de Prueba:** `test_registration.py`

---

#### **1. Análisis de los Requisitos y Especificaciones del Software**
El objetivo de la funcionalidad `register` es permitir que los nuevos usuarios puedan registrarse en el sistema y crear una cuenta con su respectiva autenticación. La vista debe cumplir con los siguientes requisitos:

- **Validación de formulario**: Los usuarios deben ingresar todos los datos requeridos (nombre de usuario, contraseña y confirmación de contraseña) de manera correcta.
- **Creación de usuario**: Si el formulario es válido, se debe crear un nuevo usuario y guardarlo en la base de datos.
- **Redirección correcta**: Después de un registro exitoso, el usuario debe ser redirigido a la página de inicio o a otra página definida.
- **Prevención de registros duplicados**: Un usuario no debe poder registrarse con un nombre de usuario ya existente.

**Principio Aplicado: Testing muestra la presencia de defectos, no su ausencia**  
El análisis de esta prueba se centró en verificar la correcta creación de cuentas, manejo de errores en la validación de formularios y la prevención de duplicados.

---

#### **2. Identificación de Escenarios y Condiciones de Prueba**
Se identificaron los siguientes escenarios clave para probar la vista `register`:

- **Escenario 1**: Un nuevo usuario intenta registrarse con todos los datos correctos.
- **Escenario 2**: Un usuario intenta registrarse con un nombre de usuario ya existente.
- **Escenario 3**: El formulario de registro es incompleto o tiene errores en la confirmación de la contraseña.

**Principio Aplicado: Las pruebas exhaustivas son imposibles**  
Se seleccionaron los casos más relevantes que cubren los problemas más comunes relacionados con el registro de usuarios, como la validación y la duplicidad de nombres de usuario, para obtener una mayor cobertura con menos casos.

---

#### **3. Definición de Objetivos y Alcance de las Pruebas**
El objetivo principal de estas pruebas es asegurar que los usuarios puedan registrarse correctamente cuando se introducen datos válidos, y que los errores de duplicación o validación del formulario se manejen apropiadamente. Las condiciones a validar son:

- El formulario de registro funciona correctamente y valida todos los campos.
- No es posible crear un usuario con un nombre de usuario duplicado.
- Los errores de validación del formulario se muestran de manera clara al usuario.

**Principio Aplicado: Testing temprano ahorra tiempo y dinero**  
La identificación de errores en la validación del formulario de registro o en el manejo de usuarios duplicados en las primeras etapas de desarrollo evita que estos problemas se conviertan en defectos más costosos de corregir en producción.

---

#### **4. Diseño y Escritura de Casos de Prueba Claros y Concisos**
Se diseñaron los siguientes casos de prueba para cubrir los escenarios clave:

1. **`test_user_can_register_successfully`**:
   - **Precondiciones**: Un usuario intenta registrarse con datos válidos.
   - **Acciones**:
     1. Enviar una solicitud `POST` con todos los campos del formulario correctos.
   - **Resultado esperado**: El usuario debe ser creado correctamente y redirigido a la página de inicio.

2. **`test_user_cannot_register_twice`**:
   - **Precondiciones**: Un usuario con un nombre de usuario ya existente intenta registrarse.
   - **Acciones**:
     1. Enviar una solicitud `POST` con un nombre de usuario que ya está registrado.
   - **Resultado esperado**: El sistema debe devolver un error de duplicación.

3. **`test_password_confirmation_mismatch`**:
   - **Precondiciones**: El usuario introduce contraseñas que no coinciden.
   - **Acciones**:
     1. Enviar una solicitud `POST` con contraseñas diferentes en los campos de confirmación.
   - **Resultado esperado**: El sistema debe devolver un error indicando que las contraseñas no coinciden aqui esta la iamgen de que esta ejecutado correctamente.

   ![alt text](image.png)

**Principio Aplicado: El testing depende del contexto**  
El diseño de estas pruebas se centró en las interacciones críticas para los usuarios, garantizando la seguridad de sus datos y una experiencia de usuario fluida en el proceso de registro.

---

#### **5. Revisión y Refinamiento de Casos de Prueba**
Los casos de prueba fueron revisados para asegurar que cubran todas las condiciones importantes:

- **Validación de formulario**: Verificar que todos los campos requeridos sean validados correctamente y que los errores de validación se manejen apropiadamente.
- **Manejo de duplicación**: Asegurarse de que los nombres de usuario duplicados no se permitan.
- **Manejo de contraseñas**: Verificar que las contraseñas y confirmaciones coincidan correctamente.

**Principio Aplicado: El agrupamiento de defectos se presenta de manera desproporcionada**  
Las pruebas se centran en las áreas donde es más probable que ocurran errores, como la validación del formulario y la duplicación de usuarios.

---

#### **6. Ejecución de Pruebas y Reporte de Defectos**
Las pruebas se ejecutaron utilizando `unittest` en Django, con los siguientes resultados:

1. **`test_user_can_register_successfully`**: **PASSED**
   - El sistema registró correctamente al usuario y lo redirigió a la página de inicio después de la creación.

2. **`test_user_cannot_register_twice`**: **FAILED**
   - El sistema no manejó adecuadamente el caso de duplicación de usuarios. El error se debió a un mal manejo de la lógica de duplicación.

   **Error detectado**: `KeyError: 'password'`. Esto ocurrió debido a un fallo en la validación del formulario, donde el campo `password` no estaba siendo manejado correctamente.

3. **`test_password_confirmation_mismatch`**: **PASSED**
   - El sistema devolvió correctamente un error cuando las contraseñas no coincidían.

**Principio Aplicado: La paradoja del pesticida**  
El caso que falló se ha identificado como un error nuevo que no había sido detectado previamente. Esto demuestra la importancia de actualizar las pruebas para encontrar nuevos defectos.

---

#### **7. Actualización y Mantenimiento de los Casos de Prueba a lo Largo del Ciclo de Vida del Software**
Dado que se detectó un problema en la validación de los campos de contraseña, se actualizarán las pruebas para verificar que este problema se resuelva correctamente. Además, se añadirán nuevas pruebas para manejar casos adicionales de duplicación de usuarios y manejo de errores de contraseña.

**Principio Aplicado: La ausencia de errores no significa un software útil**  
Aunque la mayoría de las pruebas pasaron, se detectó un error crítico en el manejo de duplicación de usuarios. Este problema se abordará en la próxima iteración de desarrollo.

---

### **Conclusión**
Las pruebas de registro demostraron que el sistema maneja correctamente la creación de usuarios y la validación de contraseñas, pero fallaron en manejar los casos de duplicación de usuarios. Se identificó un `KeyError` que afectaba la validación del formulario y será corregido en las próximas actualizaciones del código. Las pruebas son clave para asegurar la funcionalidad correcta del registro y la seguridad de los usuarios en el sistema.