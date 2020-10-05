# Web scrapping

En este repositorio se incluye un ejemplo de web scrapping sobre una web externa, de la que extraeremos automáticamente la información que nos interesa.

El ejemplo realizado toma los datos de la web española de automóviles www.km77.com. En ella, existe un apartado en el que se encuentran todas las marcas del mercado español, que a su vez acceden a otras páginas que tienen los modelos actuales de cada marca, y a su vez las versiones de cada uno de los modelos. Por último, existe una página por versión con información técnica detallada. Nuestro objetivo es ir accediendo al árbol desde la página principal de marcas hasta tener la información técnica de cada versión.

En relación al notebook, se debe tener en cuenta lo siguiente:
<ul>
  <li>El funcionamiento del notebook se basa por completo en una clase, la cual puede ser perfectamente extraída a un fichero .py para operar fuera de notebooks.</li>
  <li>En las pruebas realizadas, a la hora de obtener los datos técnicos de cada vesión, se ha limitado los resultados a 25 búsquedas para no generar un volumen de datos excesivo. El propósito en este caso es mostrar el funcionamiento, no generar una copia exacta de todos los datos de la web.</li>
  <li>Todos los datos recopilados en este ejemplo son propiedad de la web de la que han sido extraídos. Cualquier duda sobre su uso debe ser consultada en sus condiciones legales. Por tanto, queda prohíbido emplear este código para obtener los datos con fines comerciales, ya que el propósito de la creación de <b>este código fuente es meramente didáctico</b>.</li>
</ul>
