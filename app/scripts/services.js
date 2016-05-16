'use strict';

angular.module('zogkillerApp')
  .constant('baseURL', 'url for when requesting stuff from server')
	.service('homeFactory', ['$resource', 'baseURL', function($resource, baseURL){

    	var homefac = {};

  }])
;
