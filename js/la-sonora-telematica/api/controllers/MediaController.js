/**
 * MediaController
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

var mediactl = {

    _config: {},
    
    create: function(req,res){
        
        
        media.create( req.params.all() ).exec(function(err, result){
            if (err) {
                //Handle Error
            }
            // return res.send(req.query);
            res.redirect('/clock/init');
            //return res.send("chingesumare"); //res.redirect('/somewhere')
        });
        
        
    }

};


module.exports = mediactl;
