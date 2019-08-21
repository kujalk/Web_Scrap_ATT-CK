/*
 *Developer - Janarthanan
 *Purpose - RestFul API for MITRE ATTACK
 */ 

var express = require('express');
var app = express();
var cors= require('cors');
var path = require('path');
var bodyParser = require('body-parser');
var MongoClient = require('mongodb').MongoClient
var db;

app.use(cors());
//Establish Connection
MongoClient.connect('mongodb://localhost:27017', function (err, client) {
   if (err) 
   	throw err
   else
   {
	db = client.db('mitre');
	console.log('Connected to MongoDB');
	//Start app only after connection is ready
	app.listen(4300,'193.168.3.194');
        console.log('I am now listening....')
   }
 });

app.use(bodyParser.json())

app.post('/data', function(req, res) {
   // Insert JSON straight into MongoDB
  db.collection('attack_technique').insert(req.body, function (err, result) {
      if (err)
         res.send('Error');
      else
        res.send('Success');

  });
});

app.get('/all_indicators', function(req, res) {
  //Get the unique signatures

  db.collection('attack_technique').distinct("Techniques_Used",function(err, result) {

   if (err){
      res.send('Error');
      console.log("Error in retrieving all indicators");
   }
   else{
      res.send(result)
       console.log("Response send via ->/all_indicators API");
     }
});
});


app.get('/malware_type', function(req, res) {
  //Get the attack techniques that are matching particular attack pattern
  //Parameter is passed with URL

  //Extracting the parameter
  var parameter=req.query.type

  //Adding the pattern as like 
  var pat="/"+parameter+"/"

  //converting string to object
  var pattern=eval(pat);

  console.log(typeof pattern)
  var query="db.runCommand({distinct: 'attack_technique',key: 'Techniques_Used',query: { 'Information':"+pattern+" }})"
  console.log("Parameter is ->"+pattern);
  
   db.eval('function(){ return ' + query + '; }', function(err, result) {
  
   if (err){
      res.send('Error');
      console.log("Error is :"+err);
   }
   else{
      
      res.send(JSON.stringify(result));
      console.log("Response send via ->/malware_type API for the parameter "+parameter);
    }
  
  });
  });


app.get('/search_attack', function(req, res) {
  // search attack to obtain their features
  // Parameter is passed with URL
  
  //Extracting the parameter
    var name=req.query.attack
 
  //Adding the pattern as like
    var pat="/"+name+"/"
 
  //converting string to object
    var pattern=eval(pat);
  
    console.log(typeof pattern)
    var query={};
    console.log("Parameter is ->"+pattern);
    query['Attack'] = pattern
                  
  
    db.collection('attack_technique').find(query,{_id: 0}).toArray(function(err, result) {
  
    if (err){
         res.send('Error');
         console.log("Error in retrieving information related to the attack");
     }
    else{
  
         res.send(JSON.stringify(result));
         console.log("Response send via ->/search_attack API for the parameter "+name);
        }
  
   });
   });



