# practicaMongoDb
Python3 con MongoDB

## Normas
1. La realización de la práctica es obligatoria y supondrá el 50 % de la nota final de
prácticas de la asignatura.
2. La práctica se realizará en grupos de 2 a 3 personas. Excepcionalmente puede
realizarse y entregarse de forma individual, previa consulta del profesor. (En mi caso Individual)
3. La fecha límite de entrega es el domingo, 15 de mayo de 2022.
4. Se habilitará una carpeta en Teams para la entrega de la práctica. Se deberá entregar
un zip (Mongo_ApellidoAlumno1YApellidoAlumno2.zip) con las siguientes partes:
a. Un fichero con la memoria explicativa en formato pdf con el siguiente formato:
“Memoria_ApellidoAlumno1YApellidoAlumno2.pdf”
b. Una carpeta llamada “Fuente” que contendrá todos los ficheros fuente
comentados: programa de transformación de Python, código de las consultas
desarrolladas, etc. También debe incluir un fichero README adicional,
indicando los pasos a seguir para su ejecución completa.

5. En ningún caso debe enviar la fuente de datos ni completa ni parcial. En este último
caso, simplemente indicará exactamente el subconjunto del que ha partido y cómo lo
ha generado (dando los detalles para poder reproducirlo).

## Contexto
La fuente de datos es una recopilación, vía Web Scrapping, de diez mil registros
conseguidos a través de Google Play Store Apps de Android Market. La información se
almacena en https://www.kaggle.com/datasets/lava18/google-play-store-apps y consiste en
tres fuentes, de las cuales sólo nos interesarán dos (googleplaystore.csv y
googleplaystore_user_reviews.csv).

Antes de incluir los datos en MongoDB, debemos cerciorarnos de los datos que tenemos y
de las consultas.
Si nos fijamos bien, habrá campos que se deban transformar en Python para que nos
resulte más fácil a la hora de realizar las queries. Además, se tendrá que pensar si esta
información debe incluirse en una colección o en dos y explicar el porqué de esta decisión.

## Desarrollo de práctica
1. Procesamiento de los datos
Habrá que descargar el fichero de la URL anteriormente nombrada y realizar transformaciones
en Python como modificar los ‘M’ de los números para que sean millones, las comas, espacios,
etc. Se recomienda usar la librería Pandas para hacer este tipo de transformaciones.
Además, en la memoria debe incluir obligatoriamente el diseño de la/las colecciones, las
relaciones existentes e índices, así como una justificación de las decisiones tomadas.
2. Almacenamiento de datos
Una vez convertidos al formato necesario (y adecuadamente pre-procesados), los datos deben
almacenarse en una base de datos MongoDB. Debe incluir en la memoria una descripción
completa del proceso de carga realizado, describiendo todos los pasos necesarios para poder
reproducir la carga completa.
3. Análisis de los datos
En esta etapa se deben consultar los datos almacenados, usando el lenguaje de consulta
propio de MongoDB. Se pueden utilizar los medios que se deseen (pymongo o con las propias
consultas dentro de Compass) con el fin de facilitar la obtención de estas respuestas de la
manera más simple posible.
Las consultas son las siguientes:
1. ¿Cuántas User Reviews (del csv Googleplaystore_user_reviews) tienen cada una
de las Apps del CSV GooglePlayStore?
2. Del User Reviews, ¿cuántos tipos de sentimientos hay y su frecuencia? Mostrar
además, la aplicación que recibe más comentarios por tipo de sentimiento.

3. Calcular la media de Rating por categoría cuyas Reviews son mayores o iguales a
diez mil.
4. Añadir un campo nuevo (usando la función Split,
https://www.mongodb.com/docs/manual/reference/operator/aggregation/split/#:~:te
xt=Divides%20a%20string%20into%20an,only%20element%20of%20an%20array.
&text=The%20string%20to%20be%20split.) en el que se separe el año de la fecha.
5. Mostrar el número de Apps por año de actualización y la media del precio.
6. Clasificar los Ratings por grupos: 4-5, 3-4, 2-3, 1-2 con el recuento de Apps.
Defina los índices que crea necesarios para optimizar las consultas anteriores,
justificando su elección e indicando la mejora obtenida para cada una de las consultas.
