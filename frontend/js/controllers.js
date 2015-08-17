'use strict';

/* Controllers */

var metadataEditorApp = angular.module('metadataEditor', ['ui.date']);

// track whether an existing record
//
var EMPTY_CONTACT = {};

// for minification, explicitly declare dependencies $scope and $http
metadataEditorApp.controller('MetadataCtrl', ['$scope', '$http', '$log', 
  function($scope, $http, $log) {

    // initialize list of existing metadata records
    displayCurrentRecords();

    function displayCurrentRecords()
    {
      $http.get('http://localhost:4000/api/metadata')
           .success(function(data){ 
             $scope.allRecords = data.results; 
           });
    }

    var addedContacts = 
    {
      'access': 0,
      'citation': 0
    };

    $scope.addContact = function(accessOrCitation)
    {
      $scope.currentRecord[accessOrCitation]
            .push(JSON.parse(JSON.stringify(EMPTY_CONTACT)));

      addedContacts[accessOrCitation] += 1;
    };

    $scope.cancelAddContact = function(accessOrCitation)
    {
      if (addedContacts[accessOrCitation] > 0)
      {
        $scope.currentRecord[accessOrCitation].pop();
        addedContacts[accessOrCitation] -= 1;
      }
    };

    $scope.removeOnlineResource = function(resourceIndex)
    {
      if ($scope.currentRecord.online.length === 1)
      {
        $scope.currentRecord.online[0] = "";
      }
      else
      {
        $scope.currentRecord.online.splice(resourceIndex, 1);
      }
    };

    $scope.addOnlineResource = function()
    {
      $scope.currentRecord.online.push("");    
    };
  } // end of callback for controller initialization
]);
