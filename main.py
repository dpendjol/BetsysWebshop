__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from os import path as ospath
from models import Product, UserProduct, User, ProductTag, Tag
from peewee import fn, SqliteDatabase


def main():
    new_product = {
        'name': 'Televisie',
        'description': 'dit is een nieuw product',
        'price': 20.20,
        'quantity': 230.5,
        'tags': [
            'visual',
            'big screen',
            'flatscreen',
            '32inch'
        ]
    }
    
    print("###", "-"*50, "###\n")
    
    result = search("bloempot")
    print("--> Search for bloempot: ")
    print("###", "-"*50, "###")
    for i in result:
        print(i.name)
    
    print("###", "-"*50, "###\n")
    
    result = list_products_per_tag(1)
    print("--> List products of containing tag_id 1:")
    print("###", "-"*50, "###")
    for i in result:
        print(i['name'])
    
    print("###", "-"*50, "###\n")
          
    result = list_user_products(2)
    print("--> List products from user with user_id 2:")
    print("###", "-"*50, "###")
    for i in result:
        print(i['name'])
    
    print("###", "-"*50, "###\n")
    
    result = add_product_to_catalog(1, new_product)
    print("--> Added a product to the catalog:")
    print("###", "-"*50, "###")
    print("Produdct id: ", result)
    
    print("###", "-"*50, "###\n")
    
    result = update_stock(4, 4)
    print("--> Change quanty from product 4 to 4")
    print("###", "-"*50, "###")
    print("Number of rows affected: ", result)
    
    print("###", "-"*50, "###\n")
    
    result = purchase_product(2,3,100)
    print("--> User with id 2 purchased 100 product with id 3")
    print("###", "-"*50, "###")
    print("Id of inserted row: ", result)
    
    print("###", "-"*50, "###\n")
    
    result = remove_product(4)
    print("--> Remove product with id 4:")
    print("###", "-"*50, "###")
    print("Number of rows deleted: ", result)

def search(term: str):
    '''
    Search for a string in the name-column and the description column
    of the product table. Name has to contain term (case-insentitive)
    or description has to.

    Arguments:
    term -- str - search term

    Returns:
    peewee.ModelSelect
    '''
    return (Product.select()
            .where(
                fn.Lower(Product.name.contains(fn.Lower(term))) |
                fn.Lower(Product.description.contains(fn.Lower(term)))
            ))


def list_user_products(user_id):
    '''
    Get a list with products that belongs to a user

    Arguments:
    user_id -- integer

    Returns:
    list of dictionaries -- keys are table column headers
    '''
    products_query = (UserProduct.select(Product)
                      .join(Product,
                            on=(UserProduct.product_id == Product.id))
                      .join(User,
                            on=(UserProduct.user_id == User.id))
                      .where(UserProduct.user_id == user_id)
                      )
    return [item for item in products_query.dicts()]


def list_products_per_tag(tag_id):
    '''
    Get a list with products that belongs to a user

    Arguments:
    user_id -- integer

    Returns:
    list of dictionaries containing tag_name and product_name.
    '''
    query = (ProductTag.select(models.Tag.name.alias('tag_name'),
                               Product.name.alias('name'))
             .join(models.Tag,
                   on=(models.Tag.id == ProductTag.tag_id))
             .join(Product,
                   on=Product.id == ProductTag.product_id)
             .where(ProductTag.tag_id == tag_id))

    return [item for item in query.dicts()]


def add_product_to_catalog(user_id, product):
    '''
    Add a product to the Product table
    Add the product ID to to the UserProduct table

    Arguments:
    user_id -- int
    product -- dictionary containing keys's:
               name str
               description str
               price float
               quantity int
               tags liust of strings

    Returns:
    int -- product_id
    '''

    newproduct = Product.create(name=product['name'],
                             description=product['description'],
                             price=product['price'],
                             quantity=product['quantity'],
                             )
    
    tags_to_add = []
    for tag in product['tags']:
        newtag, _ = Tag.get_or_create(name=tag)
        tags_to_add.append(newtag)
        
    newproduct.tags.add(tags_to_add)
    
    UserProduct.create(user_id=user_id, product_id=newproduct)
    
    return newproduct.id


def update_stock(product_id, new_quantity):
    '''
    Update quantity at product_id

    Returns 
    int -- number of rows affected. Supposed to be one
    '''
    return (Product.update(quantity=new_quantity)
              .where(Product.id == product_id)
              .execute())


def purchase_product(product_id, buyer_id, quantity):
    '''
    registers a purchase from a product by a buyer

    Returns:
    int -- id of inserted row
    '''
    return (models.Purchase.insert(product_id=product_id,
                                   user_id=buyer_id,
                                   quantity=quantity)
            .execute())


def remove_product(product_id):
    '''
    removes products form userproduct table where product_id = product_id

    Returns:
    int -- number of rows affected
    '''
    return (UserProduct.delete()
              .where(UserProduct.product_id == product_id)
              .execute())

def create_tables():
    db = SqliteDatabase(":memory:", pragmas={'foreign_keys': 1})
    with db:
        db.create_tables([models.User,
                          models.Product,
                          models.Address,
                          models.Tag,
                          models.ProductTag,
                          models.UserProduct,
                          models.Purchase,
                          ])


def populate_data():
    user_data = [
        ["Henk", "Vriezer", 1, 1],
        ["Kees", "Herrie", 2, 1],
        ["Piet", "Oelle", 3, 1],
    ]

    product_data = [
        ["Bloempot", "Pot om bloemen in te zetten", 10, 25],
        ["Kussensloop", "Sloop om kussen te beschermen", 2.5, 10],
        ["Lamp", "Leuke verlichting voor in huis", 15.5, 15],
    ]

    address_data = [
        ["straat 1", 'h1', "1111aa", "city 1", "country 1"],
        ["straat 2", 'h2', "2222aa", "city 2", "country 2"],
        ["straat 3", 'h3', "3333aa", "city 3", "country 3"]
    ]

    tag_data = [
        ["tag 1"],
        ["tag 2"],
        ["tag 3"]
    ]

    user_product_data = [
        [1, 1],
        [1, 2],
        [2, 2]
    ]

    transaction_data = [
        [1, 1, 5],
        [1, 2, 6],
        [2, 3, 4]
    ]

    product_tag_data = [
        [1, 1],
        [2, 1],
        [3, 3]
    ]

    for item in product_data:
        Product.create(
            name=item[0],
            description=item[1],
            price=item[2],
            quantity=item[3]
        )

    for item in address_data:
        models.Address.create(
            street=item[0],
            number=item[1],
            zipcode=item[2],
            city=item[3],
            country=item[4]
        )

    for item in user_data:
        models.User.create(
            first_name=item[0],
            last_name=item[1],
            address=item[2],
            billing_address=item[3]
        )

    for item in tag_data:
        models.Tag.create(
            name=item[0]
        )

    for item in transaction_data:
        models.Purchase.create(
            user_id=item[0],
            product_id=item[1],
            quantity=item[2]
        )

    for item in user_product_data:
        models.UserProduct.create(
            user_id=item[0],
            product_id=item[1]
        )

    for item in product_tag_data:
        models.ProductTag.create(
            product_id=item[0],
            tag_id=item[1]
        )


if __name__ == "__main__":    
    

    print("Creating database and tables")
    create_tables()
    print("Populating tables")
    populate_data()

    print("mydatabase.db exists, good to go")
    
    main()
