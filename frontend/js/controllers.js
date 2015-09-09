'use strict';

/* Controllers */

var metadataEditorApp = angular.module('metadataEditor', ['ui.date']);

// track whether an existing record

// for minification, explicitly declare dependencies $scope and $http
metadataEditorApp.controller('MetadataCtrl', ['$scope', '$http', '$log', 
  function($scope, $http, $log) {

    // initialize list of existing metadata records
    displayAllRecords();

    $scope.standards = {'eml': true, 'ddi': true};

    /**
     * Search for metadata records
     */
    $scope.searchStr = "";
    $scope.search = function()
    { 
      var title_search_str = 
        $scope.searchStr === '' ? '' : '&title=' + $scope.searchStr;

      var url = 'https://mt.northwestknowledge.net/lidd/api/metadata/search?' +
                'eml=' + $scope.standards.eml + 
                '&ddi=' + $scope.standards.ddi +
                title_search_str;

      $http.get(url)
           .success(function(data) {
             data = prepareData(data);
             $scope.recordsList = data.results; 
             $scope.resultCount = data.count;
           });
    };

    function displayAllRecords()
    {
      $http.get('https://mt.northwestknowledge.net/lidd/api/metadata')
           .success(function(data){ 
             data = prepareData(data);
             $scope.recordsList = data.results; 
             $scope.resultCount = data.count;
           });
    }
    function prepareData(data)
    {
      var results = data.results;
      for (var i=0; i < results.length; i++) 
      {
        var r = results[i];
        if (r.metadata_standards[0].name === 'DDI')
        {
          r.originalLink = 
            'http://www.icpsr.umich.edu/icpsrweb/ICPSR/studies/' +
            r.native_identifier;
        }
      }

      data.results = results;

      return data;
    }
  } // end of callback for controller initialization
]);
