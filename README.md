<a href="https://www.gotoiot.com/">
    <img src="_doc/gotoiot-logo.png" alt="logo" title="Goto IoT" align="right" width="60" height="60" />
</a>

Service HTTP CoAP Interface
===========================

*Ayudaría mucho si apoyaras este proyecto con una ⭐ en Github!*

`CoAP` es un protocolo de capa de aplicación de internet especializado para dispositivos restringidos. Permite que los dispositivos - llamados nodos - se comuniquen con internet a través de un protocolo simple que hace foco en varios aspectos propios de IoT. Si querés conocer más al respecto de CoAP podés leer el documento de [Introducción a CoAP](https://www.gotoiot.com/pages/articles/mqtt_intro/index.html) que se encuentra en nuestra web.

Este proyecto es una interfaz que sirve para interactuar con un servidor CoAP desde un cliente HTTP como puede ser un navegador web, o cualquier otro tipo de cliente. Tiene una `HTTP REST API` como interfaz que te permite enviar requests CoAP hacia un servidor y devuelve la respuesta del servidor formateada adecuadamente en JSON para que la puedas interpretar. Está desarrollado en `Python` y se ejecuta sobre un contenedor de `Docker`. 

> Es importante que sepas que este servicio no es un proxy. Un proxy es un servicio que transcribe literalmente los requests HTTP a CoAP y sus correspondientes respuestas. Este servicio es una interfaz, que permite interactuar con cualquier servidor CoAP pero sin actuar como un proxy.

## Instalar las dependencias 🔩

Para correr este proyecto es necesario que instales `Docker` y `Docker Compose`. 

<details><summary><b>Mira cómo instalar las dependencias</b></summary><br>

En [este artículo](https://www.gotoiot.com/pages/articles/docker_installation_linux/) publicado en nuestra web están los detalles para instalar Docker y Docker Compose en una máquina Linux. Si querés instalar ambas herramientas en una Raspberry Pi podés seguir [este artículo](https://www.gotoiot.com/pages/articles/rpi_docker_installation) de nuestra web que te muestra todos los pasos necesarios.

En caso que quieras instalar las herramientas en otra plataforma o tengas algún incoveniente, podes leer la documentación oficial de [Docker](https://docs.docker.com/get-docker/) y también la de [Docker Compose](https://docs.docker.com/compose/install/).

Continua con la descarga del código cuando tengas las dependencias instaladas y funcionando.

</details>

## Descargar el código 💾

Para descargar el código, lo más conveniente es que realices un `fork` de este proyecto a tu cuenta personal haciendo click en [este link](https://github.com/gotoiot/service-http-coap-interface/fork). Una vez que ya tengas el fork a tu cuenta, descargalo con este comando (acordate de poner tu usuario en el link):

```
git clone https://github.com/USER/service-http-coap-interface.git
```

> En caso que no tengas una cuenta en Github podes clonar directamente este repo.

## Ejecutar la aplicación 🚀

Cuando tengas el código descargado, desde una terminal en la raíz del proyecto ejecuta el comando `docker-compose build http-coap-interface` que se va encargar de compilar la imagen de la interfaz en tu máquina (este proceso puede durar unos minutos dependiento tu conexión a internet). 

Una vez que haya compilado, ejecutá el comando `docker-compose up` para poner en funcionamiento el servicio. En la terminal (entre un log inicial y las configuraciones) deberías ver una salida similar a la siguiente:

```
...
...
      /$$$$$$            /$$                    /$$$$$$      /$$$$$$$$
     /$$__  $$          | $$                   |_  $$_/     |__  $$__/
    | $$  \__/ /$$$$$$ /$$$$$$   /$$$$$$         | $$   /$$$$$$| $$   
    | $$ /$$$$/$$__  $|_  $$_/  /$$__  $$        | $$  /$$__  $| $$   
    | $$|_  $| $$  \ $$ | $$   | $$  \ $$        | $$ | $$  \ $| $$   
    | $$  \ $| $$  | $$ | $$ /$| $$  | $$        | $$ | $$  | $| $$   
    |  $$$$$$|  $$$$$$/ |  $$$$|  $$$$$$/       /$$$$$|  $$$$$$| $$   
     \______/ \______/   \___/  \______/       |______/\______/|__/   

                      SERVICE HTTP-COAP INTERFACE
                      ---------------------------
...
...
```

Si ves esta salida significa que el servicio se encuentra corriendo adecuadamente. Podés leer la información útil para tener un mejor entendimiento de la aplicación.

## Información útil 🔍

En esta sección vas a encontrar información que te va a servir para tener un mayor contexto.

<details><summary><b>Mira todos los detalles</b></summary>

### Funcionamiento de la aplicación

El objetivo de la aplicación es recibir un request HTTP, convertirlo en un request CoAP, ejecutarlo y devolver una respuesta. Yendo más a detalle, los pasos que realiza el servicio para la ejecución de un request son los siguientes:

1. El servicio comienza su ejecución a través del comando `docker-compose up` y pone a disposición los endpoints para recibir request. Podés ver más información sobre los endpoints disponibles en el apartado `Interfaz HTTP`.
2. El usuario realiza un request hacia este servicio indicando la IP del servidor CoAP al cual desea ejecutar un request, el puerto, el método y un payload si es necesario. Para conocer más al respecto podés consultar el archivo de test requests.http que muestra cómo deben ejecutarse los requests.
3. Este servicio recibe el request HTTP del usuario, lo analiza, y genera un comando para ejecutar un request CoAP a través de la herramienta libcoap.
4. Una vez que el comando está armado lo ejecuta y se queda esperando la respuesta del server CoAP.
5. Cuando el server CoAP responde, analiza la respuesta y la convierte a JSON.
6. Finalmente con la respuesta armada la devuelve al cliente HTTP.

Para que puedas correr adecuadamente los requests hacia el server CoAP es necesario que este servicio se encuentre dentro de la misma red que el server CoAP.

Si querés realizar alguna modificación o agregar tus propias configuraciones, podés editar el archivo `_storage/settings.json`.

### Configuración de la aplicación

La configuración de toda la aplicación está alojada en el archivo `_storage/settings.json`. Podés cambiarla escribiendo en este archivo directamente. Si por casualidad llegás a borrar la configuración, podés copiar y modificar esta:

```json
{
    "API_PREFIX": "http_coap",
    "EVENTS_TO_OMIT": "HttpCoapRequest, CoapHttpResponse"
}
```

Los parámetros de configuración significan lo siguiente:

* **API_PREFIX**: El prefijo que tendrá la API de la interfaz HTTP-CoAP. Podés dejarlo con la opción por defecto o poner otra.
* **EVENTS_TO_OMIT**: La lista de eventos que no se publicaran en caso que sucedan.

### Variables de entorno

Si querés modificar algúna configuración como variable de entorno podés modificar el archivo `env`. Por lo general la configuración por defecto funciona sin necesidad que la modifiques.

### Interfaz HTTP

A través de la interfaz HTTP podés acceder a todos los recursos del servicio. A continuación están los detalles de cada uno de los endpoints con los métodos que acepta.

Obtener el estado del servicio
* **URL**: http://localhost:5000/status
* **METHOD**: GET

Testear un request HTTP enviado por el cliente.
* **URL**: http://localhost:5000/http_coap/test
* **METHOD**: PUT
* **EXAMPLE BODY**: {"message": "Hello World!"}

Ejecutar un request a un server CoAP que tiene asignada la IP 192.168.0.103, en el puerto 5683, usando el metodo GET, en un recurso llamado button.
* **URL**: http://localhost:5000/http_coap/interface
* **METHOD**: PUT
* **EXAMPLE BODY**: {
    "coap_server_ip" : "192.168.0.103",
    "coap_server_port" : 5683,
    "coap_server_resource" : "button",
    "coap_method" : "get"
    }

Ejecutar un request a un server CoAP que tiene asignada la IP 192.168.0.103, en el puerto 5683, usando el metodo PUT, en un recurso llamado light.
* **URL**: http://localhost:5000/http_coap/interface
* **METHOD**: PUT
* **EXAMPLE BODY**: {
    "coap_server_ip" : "192.168.0.103",
    "coap_server_port" : 5683,
    "coap_server_resource" : "button",
    "coap_method" : "get",
    "coap_payload" : {
            "light": true
        }
    }

### Pruebas

La mejor forma de probar el servicio es a través de un cliente HTTP. En el directorio `test/other/requests.http` tenés un archivo para probar todas las funcionalidades provistas. Para correr estos requests es necesario que los ejecutes dentro de Visual Studio Code y que instales la extensión REST Client. Sino, podés correr los requests desde Postman, CURL o cualquier otro.

</details>

## Tecnologías utilizadas 🛠️

<details><summary><b>Mira la lista de tecnologías usadas en el proyecto</b></summary><br>

* [Docker](https://www.docker.com/) - Ecosistema que permite la ejecución de contenedores de software.
* [Docker Compose](https://docs.docker.com/compose/) - Herramienta que permite administrar múltiples contenedores de Docker.
* [Python](https://www.python.org/) - Lenguaje en el que están realizados los servicios.

</details>

## Contribuir 🖇️

Si estás interesado en el proyecto y te gustaría sumar fuerzas para que siga creciendo y mejorando, podés abrir un hilo de discusión para charlar tus propuestas en [este link](https://github.com/gotoiot/service-http-coap-interface/issues/new). Así mismo podés leer el archivo [Contribuir.md](https://github.com/gotoiot/gotoiot-doc/wiki/Contribuir) de nuestra Wiki donde están bien explicados los pasos para que puedas enviarnos pull requests.

## Sobre Goto IoT 📖

Goto IoT es una plataforma que publica material y proyectos de código abierto bien documentados junto a una comunidad libre que colabora y promueve el conocimiento sobre IoT entre sus miembros. Acá podés ver los links más importantes:

* **[Sitio web](https://www.gotoiot.com/):** Donde se publican los artículos y proyectos sobre IoT. 
* **[Github de Goto IoT:](https://github.com/gotoiot)** Donde están alojados los proyectos para descargar y utilizar. 
* **[Comunidad de Goto IoT:](https://groups.google.com/g/gotoiot)** Donde los miembros de la comunidad intercambian información e ideas, realizan consultas, solucionan problemas y comparten novedades.
* **[Twitter de Goto IoT:](https://twitter.com/gotoiot)** Donde se publican las novedades del sitio y temas relacionados con IoT.
* **[Wiki de Goto IoT:](https://github.com/gotoiot/doc/wiki)** Donde hay información de desarrollo complementaria para ampliar el contexto.

## Muestas de agradecimiento 🎁

Si te gustó este proyecto y quisieras apoyarlo, cualquiera de estas acciones estaría más que bien para nosotros:

* Apoyar este proyecto con una ⭐ en Github para llegar a más personas.
* Sumarte a [nuestra comunidad](https://groups.google.com/g/gotoiot) abierta y dejar un feedback sobre qué te pareció el proyecto.
* [Seguirnos en twitter](https://github.com/gotoiot/doc/wiki) y dejar algún comentario o like.
* Compartir este proyecto con otras personas.

## Autores 👥

Las colaboraciones principales fueron realizadas por:

* **[Agustin Bassi](https://github.com/agustinBassi)**: Ideación, puesta en marcha y mantenimiento del proyecto.

También podés mirar todas las personas que han participado en la [lista completa de contribuyentes](https://github.com/gotoiot/service-http-coap-interface/contributors).

## Licencia 📄

Este proyecto está bajo Licencia ([MIT](https://choosealicense.com/licenses/mit/)). Podés ver el archivo [LICENSE.md](LICENSE.md) para más detalles sobre el uso de este material.

---

**Copyright © Goto IoT 2021** - [**Website**](https://www.gotoiot.com) - [**Group**](https://groups.google.com/g/gotoiot) - [**Github**](https://www.github.com/gotoiot) - [**Twitter**](https://www.twitter.com/gotoiot) - [**Wiki**](https://github.com/gotoiot/doc/wiki)
