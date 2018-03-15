//var sonoraserver = angular.module('sonoraserver',[ 'ui.bootstrap' ]);
var sonoraserver = angular.module('sonoraserver',[ 'ui.bootstrap.datetimepicker', 'angularFileUpload','d3']).filter('unique', function () {

    return function (items, filterOn) {

        if (filterOn === false) {
            return items;
        }

        if ((filterOn || angular.isUndefined(filterOn)) && angular.isArray(items)) {
            var hashCheck = {}, newItems = [];

            var extractValueToCompare = function (item) {
                if (angular.isObject(item) && angular.isString(filterOn)) {
                    return item[filterOn];
                } else {
                    return item;
                }
            };

            angular.forEach(items, function (item) {
                var valueToCheck, isDuplicate = false;

                for (var i = 0; i < newItems.length; i++) {
                    if (angular.equals(extractValueToCompare(newItems[i]), extractValueToCompare(item))) {
                        isDuplicate = true;
                        break;
                    }
                }
                if (!isDuplicate) {
                    newItems.push(item);
                }

            });
            items = newItems;
        }
        return items;
    };
});


var UploadCtrl = [ '$scope', '$http', '$timeout', '$upload',  function($scope, $http, $timeout, $upload) {
    $scope.mediaData.filename ="filename";
    $scope.fileReaderSupported = window.FileReader != null;
    $scope.uploadRightAway = true;
    $scope.changeAngularVersion = function() {
	window.location.hash = $scope.angularVersion;
	window.location.reload(true);
    };
    $scope.hasUploader = function(index) {
	return $scope.upload[index] != null;
    };
    $scope.abort = function(index) {
	$scope.upload[index].abort(); 
	$scope.upload[index] = null;
    };
    $scope.angularVersion = window.location.hash.length > 1 ? window.location.hash.substring(1) : '1.2.0';
    $scope.onFileSelect = function($files) {
	
	$scope.selectedFiles = [];
	$scope.progress = [];
	if ($scope.upload && $scope.upload.length > 0) {
	    for (var i = 0; i < $scope.upload.length; i++) {
		if ($scope.upload[i] != null) {
		    $scope.upload[i].abort();
		}
	    }
	}
	$scope.upload = [];
	$scope.uploadResult = [];
	$scope.selectedFiles = $files;
	$scope.dataUrls = [];
	for ( var i = 0; i < $files.length; i++) {
	    var $file = $files[i];
	    if (window.FileReader && $file.type.indexOf('image') > -1) {
		var fileReader = new FileReader();
		fileReader.readAsDataURL($files[i]);
		var loadFile = function(fileReader, index) {
		    fileReader.onload = function(e) {
			$timeout(function() {
			    $scope.dataUrls[index] = e.target.result;
			});
		    }
		}(fileReader, i);
	    }
	    $scope.progress[i] = -1;
	    if ($scope.uploadRightAway) {
		$scope.start(i);
	    }
	}
    };

    $scope.start = function(index) {
	$scope.progress[index] = 0;
	$scope.errorMsg = null;
	//if ($scope.howToSend == 1) {
	$scope.upload[index] = $upload.upload({
	    url : 'upload',
	    method: $scope.httpMethod,
            headers: {'Content-Type': undefined },
	    data : {
		myModel : $scope.myModel
	    },
	    /* formDataAppender: function(fd, key, val) {
	     if (angular.isArray(val)) {
             angular.forEach(val, function(v) {
             fd.append(key, v);
             });
             } else {
             fd.append(key, val);
             }
	     }, */
	    /* transformRequest: [function(val, h) {
	     console.log(val, h('my-header')); return val + 'aaaaa';
	     }], */
	    file: $scope.selectedFiles[index],
	    fileFormDataName: 'myFile'
	}).then(function(response) {
	    // ACTUALIZAR VISTA:
	    $scope.mediaData.filename = response.data.filename;
	}, function(response) {
	    if (response.status > 0) $scope.errorMsg = response.status + ': ' + response.data;
	}, function(evt) {
	    // Math.min is to fix IE which reports 200% sometimes
	    $scope.progress[index] = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
	}).xhr(function(xhr){
	    xhr.upload.addEventListener('abort', function() {console.log('abort complete')}, false);
	});
	/*} else {
	 var fileReader = new FileReader();
         fileReader.onload = function(e) {
	 $scope.upload[index] = $upload.http({
	 url: 'upload',
	 headers: {'Content-Type': $scope.selectedFiles[index].type},
	 data: e.target.result
	 }).then(function(response) {
	 $scope.uploadResult.push(response.data);
	 }, function(response) {
	 if (response.status > 0) $scope.errorMsg = response.status + ': ' + response.data;
	 }, function(evt) {
	 // Math.min is to fix IE which reports 200% sometimes
	 $scope.progress[index] = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
	 });
         }
	 fileReader.readAsArrayBuffer($scope.selectedFiles[index]);
	 }
	 */
    };

    $scope.resetInputFile = function() {
	var elems = document.getElementsByTagName('input');
	for (var i = 0; i < elems.length; i++) {
	    if (elems[i].type == 'file') {
		elems[i].value = null;
	    }
	}
    };
} ];




sonoraserver.controller('VisualizationCtrl',function($scope,mediaService) {

    var host = "http://"+document.location.host;
    
    $scope.selectedWord = "frozen";
    $scope.media = [];
    var wordArray = Array();


    //var request = require('request');
    setInterval(function() {

	$.get( host + '/word/currentWord', function (data) {
	    
	    $scope.$apply(function(){
		$scope.selectedWord = data;
	    });
	});
    }, 1000);


    mediaService.get()
        .success(function(data){
            var waterTypes= [
		{ words: [
                    { array: Array(),  value: "stagnant" },
                    { array: Array(),  value: "frozen" },
                ]},
                { words: [                    
                    { array: Array(),  value: "drop" },
                    { array: Array(),  value: "trickle" },
                    { array: Array(),  value: "tide" },
		]},
		{ words: [
		    { array: Array(),  value: "flowing" },
		    { array: Array(),  value: "pouring" },
		]},
		{ words: [
                    { array: Array(),  value: "rushing" },
		    { array: Array(),  value: "waterfall" },
		]},
		{ words: [
                    { array: Array(),  value: "gush" },
		    { array: Array(),  value: "wave" },
		    { array: Array(),  value: "whirpool" },
		    { array: Array(),  value: "surge" },
		]},
		{ words: [
                    { array: Array(),  value: "torrent" },
		    { array: Array(),  value: "boil" },
		    { array: Array(),  value: "flood" },
		]},
		{ words: [
		    { array: Array(),  value: "evaporated" },
                    { array: Array(),  value: "gas" },
                    { array: Array(),  value: "cloud" }

		]}
	    ];

	    
            var lookup = {};
            for(i in data){
                
                var wt = data[i].waterType;
		
		var exists = false;

                //var keywords = data[i].keywords.split(",");
                var keywords = data[i].keywords.split(",");

		for(j in waterTypes) {
		    for(k in waterTypes[j].words) {
                        if( waterTypes[j].words[k].value == wt ) {
			    for(l in keywords ) {
                                var index = waterTypes[j].words[k].array.indexOf( keywords[l] );
				if( index < 0 ) {
				    waterTypes[j].words[k].array.push( keywords[l] );

				}
			    }
			}
		    }
		}
		/*
		if( typeof(lookup[wt])=="undefined" ) {
		    var obj = { waterType: wt, keywords: keywords };
		    
		    lookup[ wt ] = obj;
		    //console.log( "lookjp", obj, lookup[wt]);
		    
		}

		else {
                    lookup[ wt ].keywords = lookup[ wt ].keywords.concat( keywords );
		}
*/
            }
	    //$scope.words = lookup;
	    
            $scope.wordsArray = waterTypes;
        })
        .error(function(data){
            console.log(data);
        });
    
    $scope.words=[{v:'a'},{v:'b'}];

});

