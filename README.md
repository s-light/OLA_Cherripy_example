# OLA_Cherripy_example
simple example for combining OLA and Cherrypy

needed to run this:
* [OLA](https://www.openlighting.org/ola/)  
* [Cherrypy](http://cherrypy.org/)

steps to run this demo:
* install both tools
* download or clone this repository to your computer
* open up a terminal and start ola: `olad -l 3`
* open up a second terminal
* navigate to the cloned folder
* start the server: `python server/main.py`
* navigate in your webbrowser to http://localhost:8080/
* there you can choose one of the two example GUIs:
    * [basic](http://localhost:8080/index_basic.html) (just plain html css and js)
    * [extended](http://localhost:8080/index_angularjs.html) (framework: angularjs)
* alternative you can test the api directly by going to http://localhost:8080/api/   

i have tested/developed this example under
* Kubuntu 15.10
* Firefox 43.0.4
* Python Version: 2.7.10
* cherrypy version: 3.7.0

this example is licensed under The MIT License (MIT)  (see [LICENSE](LICENSE) file)
