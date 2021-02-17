__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models

def search(term):
    return (models.Product.select()
            .where(models.Product.name == term))


def list_user_products(user_id):
    '''
    Get a list with products that belongs to a user
    
    Arguments:
    user_id -- integer
    
    Returns:
    list of named tuples Product columns.
    '''
    products_query = (models.UserProduct.select(models.Product)
                      .join(models.Product, on=(models.UserProduct.product_id == models.Product.id))
                      .join(models.User, on=(models.UserProduct.user_id == models.User.id))
                      .where(models.UserProduct.user_id == user_id)
                      )
    return [item for item in products_query.dicts()]


def list_products_per_tag(tag_id):
    '''
    Get a list with products that belongs to a user

    Arguments:
    user_id -- integer

    Returns:
    list of named tuples containing tag_name and product_name.
    '''
    query = (models.ProductTag.select(models.Tag.name.alias('tag_name'), models.Product.name.alias('product_name'))
             .join(models.Tag, on=(models.Tag.id == models.ProductTag.tag_id))
             .join(models.Product, on=models.Product.id == models.ProductTag.product_id)
             .where(models.ProductTag.tag_id == tag_id))

    
    return [item for item in query.dicts()]


def add_product_to_catalog(user_id, product):
    '''
    Add a product to the Product table if it doesn't exist
    Add the product ID to to the UserProduct table
    '''
    product, create = models.Product.get_or_create(name=product,
                                                 defaults={'name': product,
                                                           'description': '',
                                                           'price': 0,
                                                           'quantity': 1,
                                                           })
    if create:
        user = models.UserProduct.create(user_id=user_id, product_id=product)

    query = (models.UserProduct.select(models.UserProduct.product_id)
             .where(models.UserProduct.user_id == user_id))
    
    #print([item for item in query.dicts()])


def update_stock(product_id, new_quantity):
    pass


def purchase_product(product_id, buyer_id, quantity):
    pass


def remove_product(product_id):
    pass

if __name__ == "__main__":
    print('### STARTING ###')
    #result = search("Bloempot")
    #result = list_user_products(1)
    #result = list_products_per_tag(1)
    #result = add_product_to_catalog(1, "TV")
    add_product_to_catalog(1, "TV")
    
    try:
        if result:
            print('--- PRINTING ---')
            print(result)
            for i in result:
                print(i)
            print('--- END PRINTING ---')
    except NameError:
        print(f"'result' doesn't exists")  
    
    print('### ENDING ###')
  