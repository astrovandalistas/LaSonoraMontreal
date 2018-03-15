module.exports = {
    
    attributes: {
        title: {
            type: 'STRING',
            required: true
        },
        filename: {
            type: 'STRING'/*,
            required: true*/
        },
	country: {
            type: 'STRING'/* ,
            required: true*/
	},
	event: {
            type: 'STRING'
            /*    , required: true*/
	},
        topic: {
            type: 'STRING'
            /*    , required: true*/
	},
        keywords: {
            type: 'STRING'/*,
                required: true*/
        },
	contentType: {
            type: 'STRING'            
        },
	mediaType: {
	    type: 'STRING'
            /*, required: true*/
	},
	hasSound: {
	    type: 'STRING'
	},
	waterType: {
            type: 'STRING'
            /*, required: true*/
	},
	date: {
            type: 'DATETIME'/*,
            required: true*/
	},

	contentText: {
	    type: 'STRING'
	}
	
	
	
    },

    beforeDestroy: function(values, next) {
	media.findOne(values.where.id).done(function(err, user) {
	    if(err) {
		console.log(err);
	    }
	    else {
		var filename = user.filename;
		var fs = require('fs');

		fs.unlink('assets/uploads/'+filename, function (err) {
                    if (err) console.log( err );
                    console.log('successfully deleted /assets/uploads/'+filename);                    
		});
		
	    }
            
	});
	console.log("beforedestroy1 ", values);
	next();
    }

};



/*

 2 requests en visualizacion

 1 - dominio/words
 2 - 

 */
