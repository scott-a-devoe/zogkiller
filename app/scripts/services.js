'use strict';

angular.module('zogkillerApp')
  .constant('baseURL', 'http://localhost:3000/')
	.service('menuFactory', ['$resource', 'baseURL', function($resource, baseURL){

    	var menufac = {};

        // debugger;
        menufac.getDishes = function(){
            //return $http.get(baseURL+'dishes');
            return $resource(baseURL + 'dishes/:id', null, {'update':{method:'PUT'}});
        };
        //menufac.getDish = function (index) {
        //    return $http.get(baseURL+'dishes/'+index);
        //};

        // implement a function named getPromotion
        // that returns a selected promotion.
        menufac.getPromotion = function() {
            //return promotions;
            return $resource(baseURL + 'promotions/:id', null, {'update':{method:'GET'}});
        }

        return menufac;

	}])

  .factory('corporateFactory', ['$resource', 'baseURL', function($resource, baseURL) {

        var corpfac = {};

        // Implement two functions, one named getLeaders,
        // the other named getLeader(index)
        // Remember this is a factory not a service
        corpfac.getLeaders = function() {
          //return leadership;
          return $resource(baseURL + 'leadership/:id', null, {'update':{method:'GET'}});
        }
        // corpfac.getLeader = function(index) {
        //   return leadership[index];
        // }

        return corpfac;
    
  }])

  .factory('feedbackFactory', ['$resource', 'baseURL', function($resource, baseURL) {
        var feedfac = {};

        feedfac.getFeedbacks = function(){
            return $resource(baseURL + 'feedback/:id', null, {'update':{method:'PUT'}});
        }

        return feedfac;
  }])
;
