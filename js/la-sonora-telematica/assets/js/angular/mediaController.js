sonoraserver.controller(
    "mediaController",
    function($scope, $http, mediaService){
	
	$scope.mediaData = {};
	
	mediaService.get()
	    .success(function(data){
		$scope.media = data;
	    })
            .error(function(data){
		console.log(data);
	    });
	
	$scope.submitMedia = function( mediaData ) {
	    mediaService.store( mediaData )
                .success(function(data){
                    mediaService.get()
                        .success(function(Data){
                            $scope.media = Data;
                        });
                })
                .error(function(data){
                    console.log(data);
                });
	};
	$scope.deleteMedia = function(id){
	    mediaService.destroy(id)
		.success(function(data){
		    mediaService.get()
			.success(function(Data){
			    $scope.media = Data;
			});
		});
	};

        $scope.filter = function( mediaData ) {
            mediaService.store( mediaData )
                .success(function(data){
                    mediaService.get()
                        .success(function(Data){
                            $scope.media = Data;
                        });
                })
                .error(function(data){
                    console.log(data);
                });
        };



        $scope.waterTypes= [
            { group: "Stage 1",  value: "stagnant" },
	    { group: "Stage 1",  value: "frozen" },
	    
	    { group: "Stage 2",  value: "drop" },
	    { group: "Stage 2",  value: "trickle" },
	    { group: "Stage 2",  value: "tide" },

            { group: "Stage 3",  value: "flowing" },
	    { group: "Stage 3",  value: "pouring" },

            { group: "Stage 4",  value: "rushing" },
	    { group: "Stage 4",  value: "waterfall" },

            { group: "Stage 5",  value: "gush" },
	    { group: "Stage 5",  value: "wave" },
	    { group: "Stage 5",  value: "whirpool" },
	    { group: "Stage 5",  value: "surge" },

            { group: "Stage 6",  value: "torrent" },
	    { group: "Stage 6",  value: "boil" },
	    { group: "Stage 6",  value: "flood" },

	    { group: "Stage 7",  value: "evaporated" },
	    { group: "Stage 7",  value: "gas" },
	    { group: "Stage 7",  value: "cloud" }
	];
	var countries = Array();
        $scope.countries  = [];
        $.getJSON( "/js/countries/countries.json", function( data ) {
	    for(i in data) {
                countries.push({code: data[i].alpha3, name: data[i].name });
	    }

            function compare(a,b) {
                if (a.name < b.name)
                    return -1;
                if (a.name > b.name)
                    return 1;
                return 0;
            }

            countries.sort(compare);

	    
            $scope.$apply(function () {
                $scope.countries  = countries;
            });
            
	});

        $scope.master= {};

        $scope.reset = function() {
            $scope.mediaData = angular.copy($scope.master);
        };
        
/*
	$scope.waterTypes= [
	    ["stagnant","frozen"],
            ["drop","trickle","tide"],
            ["flowing","pouring"],
            ["rushing","waterfall"],
            ["gush","wave","whirpool","surge"],
            ["torrent","boil","flood"],
            ["evaporated","gas","cloud"]
	];
*/
	/*
        $scope.checkAll = function() {
            $scope.mediaData.waterType = angular.copy($scope.waterTypes);
        };
        $scope.uncheckAll = function() {
            $scope.mediaData.waterType = [];
        };
        $scope.checkFirst = function() {
            $scope.mediaData.waterType.splice(0, $scope.mediaData.waterType.length);
            $scope.mediaData.waterType.push($scope.waterTypes[0]);
        };
	*/
	
    });
