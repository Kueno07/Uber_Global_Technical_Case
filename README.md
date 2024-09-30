# Uber_Global_Technical_Case

Cornershop provides an integral service to stores where they can upload their catalog data and it will be reflected on the Cornershop app according to Cornershop standards. Historically, the data stores send to Cornershop system has a lot of noise and require extensive treatment to be cleaned, therefore, Cornershop found the need to create the Catalog Quality Team for this purpose. This team, among many other tasks, must ensure that the catalog being displayed has a high quality in content and also has no duplicated products. In other words, if you are browsing in a certain store in the app, we don’t want the customer to see duplicated products. 
The unique identifier for each product on Cornershop database is the PRODUCT_ID attribute. In the next problem we need to build a logic to estimate all products that are duplicated, ie, they have different product_ids but they share the same content. 
You will work with a database with the following attributes: 
- product_id: unique identifier for each product 
- product_name: name of the product 
- buy_unit: how the product can be bought, by KG or UN. For example, banana’s can be bought by KG because the price in the store is by KG. On the other hand, a pencil is bought by UN, because the price is per each unit. 
- package: format of the product, for example if it’s sold by bulk, or by units of 200 gr each, etc. 
- brand: name of the brand for the product 
- parent_category_id: parent category id of the product. For example if the product is on the aisle Alcohol > Beers, this would be the ID for Alcohol category 
- category_id: category id of the product. On previous example, the ID would correspond to Beers category 
- parent_category_name: name of the parent category 
- category_name: name of the category 
- orders: number of orders the product had in the last 30 days 
Tip: products that are duplicated might not necessarily have exactly the same content, some characters may differ from one to another 
What do you need to prepare? 
- A brief document with: 
- Any challenge you found in the way and how did you approach it 
- The main assumptions taken and rough numbers 
- Any interesting insight you found
-YourpythoncodewithaREADMEdocument
