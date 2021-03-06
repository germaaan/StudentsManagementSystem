// app.js
var routerApp = angular.module('routerApp', ['ui.router']);

routerApp.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/home');

    $stateProvider

       .state('#',{
         url:'/',
         template:'HomePage'
       })


        // HOME STATES AND NESTED VIEWS ========================================
        .state('estudiantes', {
            url: '/estudiantes',
            templateUrl: 'estudiantes.html'
        })

        .state('estudiantes.main', {
            url: '/main',
            templateUrl: 'estudiantes-main.html',
        })

              // nested list with custom controller
         .state('estudiantes.list', {
             url: '/list',
             templateUrl: 'estudiantes-lista.html',
             controller: 'ControladorEjemplo'
             /*
             controller: function($scope) {
                 $scope.dogs = ['Bernese', 'Husky', 'Goldendoodle'];
             }
             */
         })




         .state('estudiantes.detalles-estudiante',{
           url: '/detalle/:estudianteID',
           templateUrl: 'estudiantes-detalle.html',
           controller: 'ControladorDetallesEstudiante'
         })

         // nested list with just some random string data
         .state('estudiantes.nuevo', {
             url: '/nuevo',
             //Podemos meter directamente texto desde aquí
             //template: 'I could sure use a drink right now.'
             templateUrl: 'estudiantes-nuevo.html',
             controller: 'ControladorNuevoEstudiante'
         })

        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('about', {
            // we'll get to this in a bit
            url:'/about',
            template: 'This is an another page'
        });

});


/*
Controlador que manejará los datos del formulario enviándolos al servidor.
*/
routerApp.controller('ControladorNuevoEstudiante', function ($scope) {
  $scope.addAlumno = function(){
    //console.log("lamando a addAlumno()");
    //console.log($scope.alumno);
    //console.log($scope.alumno.nombre)

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.greetings.insertaralumno({'nombre':$scope.alumno.nombre,'dni':$scope.alumno.dni}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log(resp.message);
      $scope.respuesta=resp.message;
      $scope.$apply();
    });

  };


});

routerApp.controller('ControladorDetallesEstudiante', function($scope, $stateParams){

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.estudianteID;


  var ROOT = 'http://localhost:8001/_ah/api';
  gapi.client.load('helloworld', 'v1', null, ROOT);
  gapi.client.helloworld.alumnos.getAlumno({'dni':$stateParams.estudianteID}).execute(function(resp) {


    console.log(resp);
    $scope.alumno = resp;
    console.log(resp.nombre);
    $scope.$apply();
    /*
    $scope.es=resp.alumno;
    //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
    $scope.$apply();
    */
  });


  //Mockearemos un poco:
  /*
  var Estudiante = new Object();
  Estudiante.edad = "15";
  Estudiante.nombre = "Eduardo Manos Tijeras";
  Estudiante.localidad = "Granada";
  Estudiante.curso = "2º ESO";
  Estudiante.telefono="999-99-99-99"
  Estudiante.link_foto="http://maitegarcianieto.com/Fotos/Cine/Eduardo%20Manostijeras/Eduardo%20Manostijeras-7.jpg"

  //En realidad debería de llamarse a la api para conseguir todos los datos del usuario.
  $scope.es = Estudiante;
  */

  //Implementación de las acciones que se producen cuando el BOTÓN ELIMINAR se pulsa.
  $scope.ButtonClick = function(){
    console.log("Pulsado boton de eliminar")
    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.greetings.eliminaralumno({'dni':'sf'}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log(resp.message);
      $scope.respuesta=resp.message;
      $scope.$apply();
    });
  }


})

routerApp.controller('ControladorEjemplo', function ($scope) {


    console.log("holla");

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

 //service.greetings().listGreeting().execute()
        // Get the list of previous scores

    gapi.client.helloworld.alumnos.getAlumnos().execute(function(resp) {
      //console.log(resp);
      //console.log("after");
      //console.log(resp.alumnos);

      /*Usar los datos que nos proporciona nuestra API es muy sencillo, sólo tenemos que extraer del JSON que se
      encuentra en "resp" los datos que nos interesan. En este caso es un array de alumnos, por tanto
      solo tenemos que hacer resp.alumnos. ¡Ya está! Ya tenemos cargado el array y dentro de este todos los
      items a los que podemos acceder a sus atributos fácilmente.
      */

      $scope.alumnos=resp.alumnos;
      //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
      $scope.$apply();
    });

    var empleados = ['Empleado 1', 'Empleado 2', 'Empleado 3', 'Empleado4'];
    $scope.nuestrosEmpleados = empleados;
    //$scope.salidaAPI="adios";
    }
);
