USE kspace
CREATE TABLE food_restaurant_mapping (
 review_id varchar,
 source varchar,
 business_id varchar,
 restaurant_name varchar,
 location_city varchar,
 food varchar,
 PRIMARY KEY (review_id ));

CREATE TABLE business (
 business_id varchar,
 name varchar,
 city varchar,
 state varchar,
 full_address varchar,
 latitude float,
 longitude float,
 stars float,
 PRIMARY KEY (business_id ));
