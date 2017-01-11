USE kspace;

// For business
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( '5UmKMjUEUNdYWqANhGckJw','Mr Hoagie','Dravosburg','PA','4734 Lebanon Church Rd Dravosburg, PA 15034',40.3543266,-79.9007057,3.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'UsFtqoBl7naz8AVUBZMjQQ','Clancy''s Pub','Dravosburg','PA','202 McClure St Dravosburg, PA 15034',40.3505527,-79.8868138,3.0);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'cE27W9VPgO88Qxe4ol6y_g','Cool Springs Golf Center','Bethel Park','PA','1530 Hamilton Rd Bethel Park, PA 15234',40.3541155,-80.0146597,2.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'mVHrayjG3uZ_RLHkLj-AMg','Emil''s Lounge','Braddock','PA','414 Hawkins Ave Braddock, PA 15104',40.4088301,-79.8662107,4.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'mYSpR_SLPgUVymYOvTQd_Q','Grand View Golf Club','Braddock','PA','1000 Clubhouse Dr Braddock, PA 15104',40.4034049,-79.8557821,5.0);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'KayYbHCt-RkbGcPdGOThNg','Alexion''s Bar & Grill','Carnegie','PA','141 Hawthorne St Greentree Carnegie, PA 15106',40.4154859,-80.0675491,4.0);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'b12U9TFESStdy7CsTtcOeg','Flynn''s Tire & Auto Service','Carnegie','PA','718A Hope Hollow Rd Carnegie, PA 15106',40.394588,-80.0844539,2.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'Sktj1eHQFuVa-M4bgnEh8g','Forsythe Miniature Golf & Snacks','Carnegie','PA','920 Forsythe Rd Carnegie Carnegie, PA 15106',40.4054039,-80.0762665,4.0);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( '3ZVKmuK2l7uXPE6lXY4Dbg','Quaker State Construction','Carnegie','PA','8 Logan St Carnegie Carnegie, PA 15106',40.4062805,-80.0903905,2.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'QoDa50dc7g62xciFygXB9w','Greentree Animal Clinic','Pittsburgh','PA','2080 Greentree Rd Pittsburgh, PA 15220',40.3922071,-80.0691338,4.0);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( '1_lU0-eSWJCRvNGk78Zh9Q','Carnegie Free Library','Carnegie','PA','300 Beechwood Ave Carnegie Carnegie, PA 15106',40.4068423,-80.0858661,4.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( '_qopVQ6_Mz6W7-Pmbi56GQ','Advance Auto Parts','Carnegie','PA','1011 Washington Ave Carnegie, PA 15106',40.3983526,-80.0824517,3.5);
INSERT INTO business(business_id,name,city,state,full_address,latitude,longitude,stars) VALUES ( 'wJr6kSA5dchdgOdwH6dZ2w','Kings Family Restaurant','Carnegie','PA','2100 Washington Pike Carnegie, PA 15106',40.3875124,-80.0932152,3.5);



//From

//review_id | source | restaurant_name | location_city | food | business_id |

  INSERT INTO food_restaurant_mapping (review_id ,source , restaurant_name ,location_city ,food , business_id) VALUES('5UmKMjU','yelp','Mr Hoagie','Dravosburg','Biryani','5UmKMjUEUNdYWqANhGckJw');

INSERT INTO food_restaurant_mapping (review_id ,source , restaurant_name ,location_city ,food , business_id) VALUES('5UmKMjM','yelp','Mr Hoagie','Dravosburg','Biryani','5UmKMjUEUNdYWqANhGckJw');
INSERT INTO food_restaurant_mapping (review_id ,source , restaurant_name ,location_city ,food , business_id) VALUES('5UmKMjT','google','Mr Hoagie','Dravosburg','Biryani','5UmKMjUEUNdYWqANhGckJw');
INSERT INTO food_restaurant_mapping (review_id ,source , restaurant_name ,location_city ,food , business_id) VALUES('5UmKMjf','google','Mr Hoagie','Dravosburg','Nachos','5UmKMjUEUNdYWqANhGckJw');

INSERT INTO food_restaurant_mapping (review_id ,source , restaurant_name ,location_city ,food , business_id) VALUES('5UmKMjs','yelp','Kings Family Restaurant','Carnegie','Biryani','wJr6kSA5dchdgOdwH6dZ2w');
INSERT INTO food_restaurant_mapping (review_id ,source , restaurant_name ,location_city ,food , business_id) VALUES('5UmKMjj','yelp','Kings Family Restaurant','Carnegie','Nachos','wJr6kSA5dchdgOdwH6dZ2w');



UPDATE food_restaurant_mapping
 SET counter_value = counter_value + 1
 WHERE review_id='5UmKMjU' AND source='yelp' AND restaurant_name='Mr Hoagie' AND location_city='Dravosburg' AND food='Biryani' AND business_id='5UmKMjUEUNdYWqANhGckJw';

 db.users.insert({
   user_id: 'bcd001',
   age: 45,
   status: 'A'
 })INSERT INTO users (user_id, age, status)
VALUES ('bcd001', 45, 'A')

db.users.find();SELECT * FROM users

db.users.update(
  { age: { $gt: 25 } },
  { $set: { status: 'C' } },
  { multi: true }
)UPDATE users SET status = 'C'
WHERE age > 25



#INSERET
db.food_restaurant_mapping.insert( {review_id :"5UmKMjU",source:"yelp", restaurant_name:"Mr Hoagie" ,location_city:"Dravosburg" ,food:"Biryani", business_id:"5UmKMjUEUNdYWqANhGckJw"})
db.food_restaurant_mapping.insert( {review_id :"5UmKMjM",source:"yelp", restaurant_name:"Mr Hoagie" ,location_city:"Dravosburg" ,food:"Biryani", business_id:"5UmKMjUEUNdYWqANhGckJw"})
db.food_restaurant_mapping.insert( {review_id :"5UmKMjT",source:"yelp", restaurant_name:"Mr Hoagie" ,location_city:"Dravosburg" ,food:"Biryani", business_id:"5UmKMjUEUNdYWqANhGckJw"})
db.food_restaurant_mapping.insert( {review_id :"5UmKMjl",source:"yelp", restaurant_name:"Mr Hoagie" ,location_city:"Dravosburg" ,food:"Nachos", business_id:"5UmKMjUEUNdYWqANhGckJw"})
db.food_restaurant_mapping.insert( {review_id :"5UmKMjU",source:"yelp", restaurant_name:"Mr Hoagie" ,location_city:"Dravosburg" ,food:"Biryani", business_id:"5UmKMjUEUNdYWqANhGckJw"})
db.food_restaurant_mapping.insert( {review_id :"5UmKMjU",source:"yelp", restaurant_name:"Kings Family Restaurant" ,location_city:"Carnegie" ,food:"Biryani", business_id:"wJr6kSA5dchdgOdwH6dZ2w"})
db.food_restaurant_mapping.insert( {review_id :"5UmKMjU",source:"yelp", restaurant_name:"Kings Family Restaurant" ,location_city:"Carnegie" ,food:"Nachos", business_id:"wJr6kSA5dchdgOdwH6dZ2w"})

db.food_restaurant_mapping.insert( {review_id :"5UmKMjSU",source:"google", restaurant_name:"Clancy's Pub" ,location_city:"Dravosburg" ,food:"Nachos", business_id:"UsFtqoBl7naz8AVUBZMjQQ"})

db.food_restaurant_mapping.insert( {review_id :'5UddmKMjl',source:'yelp', restaurant_name:'Mr Hoagie' ,location_city:'Dravosburg' ,food:'Nachos', business_id:'5UmKMjUEUNdYWqANhGckJw'})
db.food_restaurant_mapping.insert( {review_id :'5UddmdsdKMjl',source:'yelp', restaurant_name:'Mr Hoagie' ,location_city:'Dravosburg' ,food:'Nachos', business_id:'5UmKMjUEUNdYWqANhGckJw'})



db.food_restaurant_mapping.group({     "key": {         "food": true,         "restaurant_name": true     },     "initial": {         "countfood": 0     },     "reduce": function(obj, prev) {         if (obj.food != null) if (obj.food instanceof Array) prev.countfood += obj.food.length;         else prev.countfood++;     },     "cond": {         "location_city": "Dravosburg"  , "food":"Nachos"  } });
