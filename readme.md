![](utm.png "Title")

# TSU Desarrollo de Software Multiplataforma
# Marlene Ruiz Barbosa
# Evaluación y Mejora para el Desarrollo de Software - 4°F
# 18 de Septiembre del 2024
### Abril Contreras Suaste
### Daniel Ivan Escobar Vasquez
### Jesús Sánchez Sosme

\pagebreak

# Contenidos

[1. Performance Testing](#performance-test)

[1.1 Prueba de Apache JMeter](#prueba-de-apache-jmeter)

[1.2 Prueba de Django Debug Toolbar](#prueba-de-django-debug-toolbar)

[1.3 Prueba de DDosify](#prueba-de-ddosify)

[2. Compatibility Testing](#compatibility-testing)

[2.1 Implementación](#implementación)

[3. Usability Testing](#usability-test)

# Performance Test

## Prueba de Apache JMeter
Pruebas de carga enviando múltiples solicitudes a un servidor web Apache para evaluar su rendimiento y capacidad de manejar la carga.

### Resultados
![alt text](performance.png)

![alt text](performance-1.png)


## Prueba de Django Debug Toolbar
Django Debug Toolbar es una herramienta de desarrollo para Django que muestra información sobre el rendimiento de una aplicación web, como el tiempo de respuesta de la base de datos, el número de consultas realizadas y el tiempo de ejecución de cada vista.

Descargamos el django debug toolbar y lo instalamos en nuestro proyecto de django. Esto hará que aparezca en nuestro navegador una barra de herramientas con información sobre el rendimiento de nuestra aplicación. 


Podemos ver el rendimiento de nuestra pagina como por ejemplo
En el de SQL panel te muestra todas las consultas SQL que se han ejecutado en la página actual. Es muy útil para identificar consultas ineficientes o repetitivas.

![SQL|Sin productos](performance-3.png)

![SQL|Con productos](performance-7.png)

La información de la barra Django Debug Toolbar indica que tu aplicación Django realizó 4 consultas SQL cuando se accedió a la página /cart/. Las consultas parecen estar relacionadas con la autenticación de usuario (auth_user), la tabla de sesiones de Django (django_session), el carrito de compras (shopApp_shoppingcart) y las categorías (shopApp_category).

## Prueba de Ddosify
Ddosify es una herramienta de prueba de carga y estrés de sitios web que permite a los usuarios simular un gran número de solicitudes a un servidor web para evaluar su rendimiento y capacidad de manejar la carga.

Podemos ver el cambio de rendimiento de nuestra pagina al agregar productos a la base de datos. En la primera imagen (Figure 2), la página se carga en aproximadamente 0.0302 segundos, mientras que en la segunda imagen (Figure 3), la página se carga en aproximadamente 0.0423 segundos. Esto puede deberse a que la página está realizando más consultas SQL o que está procesando más datos en la segunda imagen. Podemos entender que si tenemos más productos en nuestra base de datos, la pagina tardara mas en cargar.

![ddosify|Pagina de inicio sin productos](performance-4.png)

![ddosify|Pagina de inicio con productos](performance-6.png)

\newpage
El registro no tiene problemas.

![ddosify|Registro](performance-5.png)

\newpage

# Compatibility testing

Es un tipo de testing donde nos aseguramos de que nuestro software funcione de manera esperada en múltiples navegadores, dispositivos plataformas y sistemas operativos, con el fin de encontrar discrepancias de forma temprana.

## Implementación

Para realizar pruebas de compatibilidad entre distintos navegadores nos podemos valer de la herramienta Selenium que sirve para automatizar el uso de un navegador Firefox o Chrome.
En el, nos aseguraremos de que tanto la interfaz, como la funcionalidad de nuestro navegador sean las mismas en diferentes navegadores y sistemas operativos.

Creamos un test usando la utilidad TestCase de Django. 
Nuestra barra de navegación tiene 4 botones, cada uno de ellos tiene un dropdown que se activa al pasar el mouse sobre ellos.
Nuestro primer test corroborará que cuando entremos al sitio, el dropdown esté escondido y que el cursor sea el que lo active, esto en los navegadores Chrome y Firefox.

```python
class TestChrome(TestCase):
    def setUp(self):
        self.url = "http://192.168.1.140:3011"
        self.browser = webdriver.Chrome()

    def test_navbar(self):
        """ Should be none by default, block when hovering. """
        self.browser.get(self.url)
        action_chains = ActionChains(driver=self.browser)

        # Get products button
        products_button = self.browser.find_element(By.ID, "productos")
        
        # Get dropdown
        product_dropdown = products_button.find_element(By.XPATH, "following-sibling::*")

        # display is none by default
        self.assertEqual(product_dropdown.value_of_css_property("display"), 'none')
        
        # hover button, show dropdown
        action_chains.move_to_element(products_button).perform()
        
        # dropdown's display is block when hovering
        self.assertEqual(product_dropdown.value_of_css_property("display"), 'block')
```

Tras correr el test, ahora lo realizamos desde Firefox, para ello únicamente reemplazamos el método en la cuarta línea.

```python
        self.browser = webdriver.Firefox()
```

Volvemos a correr el test y notamos que la página no termina de cargar, y obtenemos un error.

```
======================================================================
FAIL: test_navbar_mobile (shopApp.tests.compatibility.test_firefox.TestFirefox.test_navbar_mobile)
Should be none by default, block when clicked.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/daniel/Documents/projects/proyecto_db/shopApp/tests/compatibility/test_firefox.py", line 50, in test_navbar_mobile
    self.assertEqual(product_dropdown.value_of_css_property("display"), 'block')
AssertionError: 'none' != 'block'
- none
+ block


----------------------------------------------------------------------
Ran 2 tests in 185.587s

FAILED (failures=2)
Destroying test database for alias 'default'...
```

El error sucede porque elenium está esperando a que el sitio termine de cargar para saltar a la siguiente línea de codigo. Al no terminar de cargar, se ejecuta un timeout a los 90 segundos, cerrando el programa y no siendo capaz de realizar las comprobaciones.

Volvemos a correr el test, verificando no sea un error de conectividad puntual y se obtienen los mismos resultados. Tras repetir varias veces llegamos a la conclusión de que trabajando con firefox en Selenium es probable que haya un error de configuración o un error de la librería que está causando comportamientos inesperados. El siguiente paso para resolverlo sería investigar y en caso de no tener solución, cambiar la libería de pruebas automatizadas.

Nuestro siguiente test verificará el comportamiento de los dropdowns en dispositivos con pantallas pequeñas. Cuando en pantallas de menor resolución, el dropdown pasará a tener el tamaño completo de la pantalla para dar al usuario una mejor usabilidad. Esto lo hacemos con css a través de media queries. 

Ejecutamos los tests y se ejecutan sin errores de forma inmediata en chrome.

## Siguientes pasos

- Solucionar el problema con Firefox y Selenium, o en su lugar, buscar un reemplazo.
- Probar en distintos sistemas operativos.
- Probar con navegadores Safari.
- Integrar la suit de tests al mecanismo de desliegue, para que el codigo se pruebe de forma automatica.

# Usability test

## Objetivo: Evaluar la experiencia del usuario al navegar y carrito de compras.

Acciones Realizadas por el Usuario:
Inicio y Exploración General:

El usuario comenzó explorando la página, navegando por las distintas secciones sin realizar acciones específicas inicialmente.
Añadir Productos al Carrito:

El usuario añadió varios productos al carrito desde las categorías disponibles.
Al intentar proceder con la compra, se le solicitó registrarse en el sistema.
Registro:

El usuario completó el proceso de registro sin problemas.
Exploración de Categorías:

El sistema cuenta con tres categorías de productos:

- Refrescos
- Gomitas
- Sabritas

El usuario navegó fácilmente entre las categorías y se sintió cómodo al buscar productos, gracias a la estructura clara de las mismas.
Interacción con el Carrito:

El usuario añadió y eliminó productos varias veces para comprobar si el sistema manejaba adecuadamente las actualizaciones en el carrito.
También salió del carrito y añadió más productos para verificar si existía algún problema al realizar varias acciones sucesivas. No se encontraron problemas en esta área.
Experiencia General del Usuario:

El usuario comentó que la navegación era fácil y fluida, gracias a la categorización de productos.
Mencionó que no había demasiados movimientos innecesarios, lo que hizo que la experiencia fuera cómoda y sencilla.

Habia un problema que era lo que las gomitas desaparecian pero era porque al comprar todo el producto de las gomitas estas desaparecian 
por lo que tienes de ir ala base de datos para agregar mas stock y este producto de gomitas vuelva aparecer.

![Prueba de usabilidad](usability.png)

![Prueba de usabilidad](usability2.png)

- [x] Ver un producto
- [x] Agregar un producto al carrito
- [ ] Comprar un producto


## Conclusiones del test de usabilidad:
Aspectos Positivos:
El usuario encontró la aplicación fácil de usar y la estructura de categorías facilitó la búsqueda de productos.
El sistema de carrito respondió bien a las múltiples acciones de añadir y eliminar productos.

Aspectos negativos:
El usuario no pudo completar la compra del produto debido a una mala configuración de la pasarela de pago.

# Link del proyecto:

[Github](https://github.com/MindSetFPS/proyecto_db)

# Referencias

Gillis, A. S. (2023, 9 marzo). performance testing. Software Quality. <https://www.techtarget.com/searchsoftwarequality/definition/performance-testing#:~:text=Performance%20testing%20is%20a%20testing,to%20identify%20performance%2Drelated%20bottlenecks>.

Chatterjee, S. (2023, August 16). What is Compatibility Testing? (Examples Included) | BrowserStack. BrowserStack. https://www.browserstack.com/guide/compatibility-testing

User-centric performance metrics. (2023, August 2). web.dev. https://web.dev/articles/user-centric-performance-metrics

Moran, K. (2024, January 12). Usability Testing 101. Nielsen Norman Group. https://www.nngroup.com/articles/usability-testing-101/

Rees, D. (2024, February 27). What is usability testing? | Experience UX. Experience UX. https://www.experienceux.co.uk/faqs/what-is-usability-testing/

R, B. (2024, September 12). What Is Performance Testing? Types, Tools & Examples. QA Touch. https://www.qatouch.com/blog/performance-testing/

Suleymanov, N. (2024, July 19). Everything you need to know about compatibility testing in 1 article. Aqua Cloud - Best Software for Testing. https://aqua-cloud.io/compatibility-testing/