'use strict';

angular.module('zogkillerApp', ['ui.router', 'ngResource'])
    .config(function($stateProvider, $urlRouterProvider) {
        $stateProvider
            // route for the home page
            .state('app', {
                url:'/',
                views: {
                    // 'header': {
                    //     templateUrl : 'views/header/.html',
                    // }
                    // ,
                    'content': {
                        templateUrl : '/static/app/views/home.html',
                        controller  : 'IndexController'
                    }
                    // ,
                    // 'footer': {
                    //     templateUrl : 'views/footer.html',
                    // }
                }
            })
        
            // // route for the aboutus page
            // .state('app.aboutus', {
            //     url:'aboutus',
            //     views: {
            //         'content@': {
            //             templateUrl : 'views/aboutus.html',
            //             controller  : 'AboutController'                  
            //         }
            //     }
            // })
        
            // // route for the contactus page
            // .state('app.contactus', {
            //     url:'contactus',
            //     views: {
            //         'content@': {
            //             templateUrl : 'views/contactus.html',
            //             controller  : 'ContactController'                  
            //         }
            //     }
            // })

        ;
        $urlRouterProvider.otherwise('/');
    })
;
