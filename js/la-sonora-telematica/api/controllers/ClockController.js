/**
 * ClockController
 *
 * @module      :: Controller
 * @description	:: A set of functions called `actions`.
 *
 *                 Actions contain code telling Sails how to respond to a certain type of request.
 *                 (i.e. do stuff, then send some JSON, show an HTML page, or redirect to another URL)
 *
 *                 You can configure the blueprint URLs which trigger these actions (`config/controllers.js`)
 *                 and/or override them with custom routes (`config/routes.js`)
 *
 *                 NOTE: The code you write here supports both HTTP and Socket.io automatically.
 *
 * @docs        :: http://sailsjs.org/#!documentation/controllers
 */
var clockctl = {
    
    formattedDate: function (date) {
        var d = new Date(date || Date.now()),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [day, month, year].join('/');
    },

    dates: Array(),
    datesIndex: 0,
    currentDate: function (req, res) {
        var indx = clockctl.datesIndex;
	var data = clockctl.dates[ indx ];
        return res.json( data );      
    },
    
    currentddmmyy: function (req, res) {
        var indx = clockctl.datesIndex;
        var date = clockctl.dates[ indx ];
        var data = clockctl.formattedDate( date );
        return res.json( data );      
    },
    
    ddmmyyyy: function (req, res) {
        var tmparr = Array();
        for(i in clockctl.dates ) {
            tmparr.push( clockctl.formattedDate( clockctl.dates[i] ));
        }
        return res.json( tmparr );      
    },
    
    
    
    ddmmyyyy: function (req, res) {
	var tmparr = Array();
	for(i in clockctl.dates ) {
            tmparr.push( clockctl.formattedDate( clockctl.dates[i] ));
	}
        return res.json( tmparr );	
    },
    
    init: function (req, res) {
       // open db and obtain dates from it

       var media;
       var tmparr = Array();
       
	var request = require('request');
        var host = "http://"+document.location.host
;
       request(host+'media', function (error, response, body) {
           if (!error && response.statusCode == 200) {
	       console.log(body);
	       media = JSON.parse(body);
	       console.log("media:", media);
	   }
	   for(i in media) {
               var datestr = new Date( media[i].date );
               //var datestr = clockctl.formattedDate( media[i].date );
               //var datestr = date.toString("MMMM yyyy");
	       
               tmparr.push( datestr );
	   }
           
           clockctl.dates = tmparr.sort(function(a,b){return a-b});
	   return res.json( clockctl.dates );
       });


        setInterval( function(){
	    clockctl.datesIndex++;
	    console.log( clockctl.datesIndex );
            var l = clockctl.dates.length ;
	    
            if( clockctl.datesIndex > l ) {
                clockctl.datesIndex = 0;
	    }
	    
	}, 1000 );
	

	

  },


  /**
   * Action blueprints:
   *    `/clock/fwd`
   */
   fwd: function (req, res) {
    
    // Send a JSON response
    return res.json({
      hello: 'world'
    });
  },


  /**
   * Action blueprints:
   *    `/clock/getDate`
   */
   getDate: function (req, res) {
    
    // Send a JSON response
    return res.json({
      hello: 'world'
    });
  },


  /**
   * Action blueprints:
   *    `/clock/reset`
   */
   reset: function (req, res) {
    
    // Send a JSON response
    return res.json({
      hello: 'world'
    });
  },


  /**
   * Action blueprints:
   *    `/clock/setSpeed`
   */
   setSpeed: function (req, res) {
    
    // Send a JSON response
    return res.json({
      hello: 'world'
    });
  },


  /**
   * Action blueprints:
   *    `/clock/getSpeed`
   */
   getSpeed: function (req, res) {
    
    // Send a JSON response
    return res.json({
      hello: 'world'
    });
  },




  /**
   * Overrides for the settings in `config/controllers.js`
   * (specific to ClockController)
   */
  _config: {}

  
};



module.exports = clockctl;
