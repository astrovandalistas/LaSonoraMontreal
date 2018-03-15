/**
 * FileController
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

module.exports = {
    
    


    /**
     * Overrides for the settings in `config/controllers.js`
     * (specific to FileController)
     */
    _config: {},
    zip: function(req,res){

        var path = __dirname + "/../../assets/uploads/";
        var zipPath = __dirname + "/../../assets/zip/";
        var filename = "uploads.zip";
        var outputPath = zipPath + filename;
	
        var fs = require('fs');
        var archiver = require('archiver');

        var output = fs.createWriteStream(outputPath);
        var zipArchive = archiver('zip');

        output.on('close', function() {
            console.log('done with the zip', outputPath);
        });

        zipArchive.pipe(output);

        zipArchive.bulk([
            { src: [ '**/*' ], cwd: path, expand: true }
        ]);

        zipArchive.finalize(function(err, bytes) {

            if(err) {
                throw err;
            }

            console.log('done:', base, bytes);

	});

        var fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;
        
	
	/*
        var path = require('path'),
            appDir = path.dirname(require.main.filename);

        var express = require('express');

        console.log(express.static(process.cwd()));
	 */
	/*

        var Zip = require("adm-zip");
        var zip = new Zip();

        function basename(path) {
            return path.replace(/\\/g,'/').replace( /.*\//, '' );
	}

	
        //zip.addLocalFolder( path );
        zip.addLocalFolder( path );
        zip.writeZip( zippath + "uploads.zip");
	 */
	


	/*
         var rzip = new Zip( path + "uploads.zip"); 
	console.log(rzip);
	res.send(rzip);
	 */

	
	res.send( '<a href="' + fullUrl + '/' + filename +'">Zip OK</a>');
	
    },
    
    upload : function(req, res) {
         
        var fs = require('fs');

        fs.readFile(req.files.myFile.path, function (err, data) {
            // ...
            var filename = req.files.myFile.name;
            var newPath = __dirname + "/../../assets/uploads/"+filename;
            fs.writeFile(newPath, data, function (err) {
                var dt = {filename: filename};
		res.send(dt);
		//res.redirect('/');
            });
         });


    }
    
};
