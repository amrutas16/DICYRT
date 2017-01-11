var http = require('http');
var fs = require('fs');
var formidable = require("formidable");
var util = require('util');
//lets require/import the mongodb native drivers.
var mongodb = require('mongodb');

//We need to work with "MongoClient" interface in order to connect to a mongodb server.
var MongoClient = mongodb.MongoClient;

// Connection URL. This is where your mongodb server is running.
var url = 'mongodb://152.46.19.234:27017/test';

// Use connect method to connect to the Server
MongoClient.connect(url, function (err, db) {
  if (err) {
    console.log('Unable to connect to the mongoDB server. Error:', err);
  } else {
    //HURRAY!! We are connected. :)
    console.log('Connection established to', url);
     var collection = db.collection('business');

    // do some work here with the database.

    collection.find({name:"Rocky's Lounge"}).toArray(function (err, result) {
     if (err) {
       console.log(err);
     } else if (result.length) {
       console.log('Found:', result);
     } else {
       console.log('No document(s) found with defined "find" criteria!');
     }
   });
   //Group By query
   /*var query ={
	"key" : {
		"food" : true,
		"restaurant_name" : true
	},
	"initial" : {
		"countfood" : 0
	},
	"reduce" : function (obj, prev) {         if (obj.food != null) if (obj.food instanceof Array) prev.countfood += obj.food.length;         else prev.countfood++;     },
	"cond" : {
		"location_city" : "Dravosburg",
		"food" : "Nachos"
	}
}*/

var keys ={
 "food" : true,
 "restaurant_name" : true
}
var condition={
 "location_city" : "Dravosburg",
 "food" : "Nachos"
}
var initial={
 "countfood" : 0
}

  //  collection.group(keys,condition,initial,function (obj, prev) {   
  //        if (obj.food != null) if (obj.food instanceof Array) prev.countfood += obj.food.length;         else prev.countfood++;     }),(function (err, result) {
  //   if (err) {
  //     console.log(err);
  //   } else if (result.length) {
  //     console.log('Found:', result);
  //   } else {
  //     console.log('No document(s) found with defined "find" criteria!');
  //   }
  // });

    //Close connection
    db.close();
  }
});


const query = 'SELECT * from business';

var server = http.createServer(function (req, res) {
    if (req.method.toLowerCase() == 'get') {
        displayForm(res);
    } else if (req.method.toLowerCase() == 'post') {
        processAllFieldsOfTheForm(req, res);
    }

});

function displayForm(res) {
    fs.readFile('form.html', function (err, data) {
        res.writeHead(200, {
            'Content-Type': 'text/html',
                'Content-Length': data.length
        });
        res.write(data);
        res.end();
    });
}

function processAllFieldsOfTheForm(req, res) {
    var form = new formidable.IncomingForm();

    form.parse(req, function (err, fields, files) {
        //Store the data from the fields in your data store.
        //The data store could be a file or database or any other store based
        //on your application.
        client.execute(query, function (err, result) {
  		var user = result.first();
  		//The row is an Object with column names as property keys.
  		// res.write(user.business_id);
    //     res.write(user.name);
    //     res.write(user.city);
    //     res.write(user.full_address);
    	console.log(user);
  		});
        res.writeHead(200, {
            'content-type': 'text/plain'
        });
        res.write('received the data:\n\n');

        res.end(util.inspect({
            fields: fields,
            files: files
        }));
    });
}

server.listen(1185);
console.log("server listening on 1185");
