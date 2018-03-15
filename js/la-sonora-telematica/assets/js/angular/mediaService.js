sonoraserver.factory("mediaService", function($http){
    return {
	get : function() {
	    return $http.get('/media');
	},
	store : function(mediaData){
	    return $http({
		method: 'POST',
		url: '/media',
		headers: {'Content-Type': 'application/x-www-form-urlencoded' },
		data: $.param( mediaData )
	    });
	},
	destroy: function(id){
	    return $http.delete('/media/' + id);
	}
	
    }
});
