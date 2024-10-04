# Compatibility testing

Es un tipo de testing donde nos aseguramos de que nuestro software funcione de manera esperada en multiples navegadores, dispositivos plataformas y sistemas operativos, con el fin de encontrar discrepancias de forma temprana.

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

Tras correr el test, ahora lo realizamos desde Firefox, para ello unicamente reemplazamos el metodo en la cuarta línea.

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

El error es causado porque Selenium está esperando a que el sitio termine de cargar para saltar a la siguiente línea de codigo. Al no terminar de cargar, se ejecuta un timeout a los 90 segundos, cerrando el programa y no siendo capaz de realizar las comprobaciones.

Volvemos a correr el test, verificando no sea un error de conectividad puntual y se obtienen los mismos resultados. Tras repetir varias veces llegamos a la conclusión de que trabajando con firefox en Selenium es probable que haya un error de configuración o un error de la libería que está causando comportamientos inesperados. El siguiente paso para resolverlo sería investigar y en caso de no tener solución, cambiar la libería de pruebas automatizadas.

Nuestro siguiente test verificará el comportamiento de los dropdowns en dispositivos con pantallas pequeñas. Cuando en pantallas de menor resolución, el dropdown pasará a tener el tamaño completo de la pantalla para dar al usuario una mejor usabilidad. Esto lo hacemos a través de media queries. 

Ejecutamos los tests y se ejecutan sin errores de forma inmediata.

# Siguientes pasos

- Solucionar el problema con Firefox y Selenium, o en su lugar, buscar un reemplazo.
- Probar en distintos sistemas operativos.
- Probar con navegadores Safari.
- Integrar la suit de tests al mecanismo de desliegue, para que el codigo se pruebe de forma automatica.