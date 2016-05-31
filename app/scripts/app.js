'use strict';

angular.module('zogkillerApp', ['ui.router', 'ngResource'])
    .config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {

        var dir = '/static/app/';

        $locationProvider.html5Mode(true);

        $stateProvider
            // route for the home page
            .state('app', {
                url:'/',
                views: {
                    'header': {
                        templateUrl : dir + 'views/header.html',
                        controller : 'HeaderController'
                    }
                    ,
                    'content': {
                        templateUrl : dir + 'views/home.html',
                        controller  : 'HomeController'
                    }
                    // ,
                    // 'footer': {
                    //     templateUrl : 'views/footer.html',
                    // }
                }
            })

            .state('app.leagues', {
                url:'leagues',
                views: {
                    'content@': {
                        templateUrl : dir + 'views/leagues.html',
                        controller  : 'LeagueController'
                    }
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
    }])
;
