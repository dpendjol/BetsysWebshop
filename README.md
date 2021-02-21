# Betsy's Webshop

![insert image](img/ERD.png)  
ER diagram of database

## Modeling choices made

- Choose for billing adress information, in 
- The tag-name field has to be unique
- Choose to index the product-name field and product-description field for quick querying
- I put a constraint on the quantity fields so that the value is always 0 or higher. Negative amounts are not possible.
- To make sure the prices are stored good I used a decimal field, with 2 decimal places. Also set the auto_found to true to round off numbers with more then 2 decimal places.

## Querying

- The search function is case-insensitive and will search the name and the description field of the product table.
- When adding a product the assumption is made that the product doesn't yet exists for that user.