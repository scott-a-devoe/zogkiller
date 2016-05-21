'use strict';

angular.module('zogkillerApp')
    .constant('baseURL', 'url for when requesting stuff from server')


    .service('homeFactory', ['baseURL', '$http', function(baseURL, $http){
        var homefac = {};

        return homefac;
    }])



    .service('leagueFactory', ['baseURL', '$http', function(baseURL, $http){
        var leagfac = {};

        leagfac.getLeagues = function(){
            return $http.get('api/leagues/volleyball/open');
        }

        leagfac.formatResponse = function(response){
            var fmt = [];
            response = JSON.parse(response.data);
            for (var i = 0; i < response.length; i++) {
                fmt.push(response[i].fields);
            }
            return fmt;
        }

        return leagfac;
    }])
;
