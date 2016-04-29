'use strict';

angular.module('zogkillerApp')

    .controller('IndexController', ['$scope', 'menuFactory', function($scope, menuFactory) {

        $scope.com = 'Loading ...';

    //     $scope.featuredDish = menuFactory.getDishes().get({id:0}).$promise.then(
    //         function(response){
    //             $scope.featuredDish = response;
    //             $scope.showFeatureDish = true;
    //         }, 
    //         function(response) {
    //             $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
    //         }
    //     );

    //     $scope.showPromo = false;

    //     $scope.promo = menuFactory.getPromotion().get({id:0}).$promise.then(
    //         function(response) {
    //             $scope.promo = response;
    //             $scope.showPromo = true;
    //         },
    //         function(response) {
    //             $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
    //         }
    //     );

    //     $scope.showEChef = false;

    //     $scope.eChef = corporateFactory.getLeaders().get({id:3}).$promise.then(
    //         function(response) {
    //             $scope.eChef = response;
    //             $scope.showEChef = true;
    //         },
    //         function(response) {
    //             $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
    //         }
    //     );

    }])

    // .controller('AboutController', ['$scope', '$stateParams', 'corporateFactory', function($scope, $stateParams, corporateFactory) {
        
    //     $scope.showLeaders = false;

    //     $scope.corpLeaders = corporateFactory.getLeaders().query(
    //         function(response) {
    //             $scope.corpLeaders = response;
    //             $scope.showLeaders = true;
    //         },
    //         function(response) {
    //             $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
    //         }
    //     )

    //     $scope.corpLeader = corporateFactory.getLeaders(parseInt($stateParams.id), 10);
    // }])

;