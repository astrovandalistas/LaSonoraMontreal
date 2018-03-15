/**
 * Bootstrap
 *
 * An asynchronous boostrap function that runs before your Sails app gets lifted.
 * This gives you an opportunity to set up your data model, run jobs, or perform some special logic.
 *
 * For more information on bootstrapping your app, check out:
 * http://sailsjs.org/#documentation
 */

module.exports.bootstrap = function (cb) {

    var express = require('express');
    sails.express.app.use(express.static(process.cwd() + '/uploads'));
    
  // It's very important to trigger this callack method when you are finished 
  // with the bootstrap!  (otherwise your server will never lift, since it's waiting on the bootstrap)
/*
    console.log("aha!");
    
    var contar = function (){
        sails.config.clock.clock+=1;
        if( sails.config.clock.clock > 10000 )
            sails.config.clock.clock = 0;
        console.log(sails.config.clock.clock);
    }
    setInterval(function(){contar();},100);
 */
    
    cb();
};
