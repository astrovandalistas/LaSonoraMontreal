var lastChosenWord = 'frozen';

Array.prototype.contains = function ( needle ) {
    
    var type = Object.prototype.toString.call(this);
    var typen = Object.prototype.toString.call(needle);
    //console.log( type, typen );

    
    if( type === '[object Array]' && typeof(needle) != "undefined" ) {
	if( this.length > 0 ) {
	    for (i in this) {
		if (this[i] == needle) return true;
	    }
	    return false;

	}
    }
}


var wordctl = {
    usedWords: Array(),

    waterTypes: [
        ["stagnant","frozen"],
        ["drop","trickle","tide"],
        ["flowing","pouring"],
        ["rushing","waterfall"],
        ["gush","wave","whirpool","surge"],
        ["torrent","boil","flood"],
        ["evaporated","gas","cloud"]
    ],
    waterTypesIndex: 0,

    init: function (req, res) {
       // open db and obtain waterTypes from it

       var media;
	
       
       var request = require('request');
       request('http://localhost:1337/media', function (error, response, body) {
           if (!error && response.statusCode == 200) {
	       //console.log(body);
	       media = JSON.parse(body);
	       //console.log("media:", media);
	   }
	   for(i in media) {
               var waterTypestr = media[i].waterType;
               
               wordctl.usedWords.push( waterTypestr );
	   }
           

	   return res.json( wordctl.waterTypes );
       });


        setInterval( function(){
	    wordctl.waterTypesIndex++;
	    
            var l = wordctl.waterTypes.length ;
	    
            if( wordctl.waterTypesIndex > l ) {
                wordctl.waterTypesIndex = 0;
	    }
	    
            wordctl.chooseWord();
	}, 20000 );
	

	

    },
    currentWordJson: function (req, res) {
        var origin = (req.headers.origin || "*");
	res.writeHead(
            "204",
            "No Content",
            {
                "access-control-allow-origin": origin,
                "access-control-allow-methods": "GET, POST, PUT, DELETE, OPTIONS",
                "access-control-allow-headers": "content-type, accept",
                "access-control-max-age": 10, // Seconds.
                "content-length": 0
            }
        );

        res.end("huvos");
    },
    currentWord: function (req, res) {

        res.send(lastChosenWord);
    },
    chooseRandomWord: function(arr){
        
        var wordIndex = Math.floor(Math.random() * arr.length );

        if( wordIndex < 0 ) wordIndex = 0;
        lastChosenWord = arr[ wordIndex ];

        //console.log( "chose:", wordctl.waterTypesIndex, " - ",  lastChosenWord );
	
    },
    
    chooseWord: function(){
        
        var tmparr = wordctl.waterTypes[ wordctl.waterTypesIndex ];


        if( Object.prototype.toString.call(tmparr) === '[object Array]') {



            //console.log( "----", lastChosenWord, wordctl.waterTypes[ wordctl.waterTypesIndex ] );

            var typearr = Object.prototype.toString.call( wordctl.usedWords );

            wordctl.chooseRandomWord(tmparr);
            
            if( typeof(lastChosenWord)!="undefined"
		&&
		typearr === '[object Array]' ) {

                    //if( wordctl.usedWords.length > 0 ) {
                        //if( ! wordctl.usedWords.indexOf( lastChosenWord ) > -1 ) {
                    var nochecks = 0;
		    while( ! wordctl.usedWords.contains( lastChosenWord ) && nochecks < tmparr.length ) {
                        wordctl.chooseRandomWord(tmparr);
			nochecks++;			    
		    }
                    if( nochecks == tmparr.length && ! wordctl.usedWords.contains( lastChosenWord ) ) {
			wordctl.waterTypesIndex++;
                        wordctl.chooseWord();
		    }

		
	    }

	} else {
	    //console.log("UNDFND");
	}
    },
  _config: {}

  
};



module.exports = wordctl;
