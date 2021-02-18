__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from peewee import fn


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
    return ((models.Product.select()
            .where((fn.Lower(models.Product.name.contains(fn.Lower(term)))) |
            fn.Lower(models.Product.description
                     .contains(fn.Lower(term))))))


def list_user_products(user_id):
    '''
    Get a list with products that belongs to a user

    Arguments:
    user_id -- integer

    Returns:
    list of named tuples Product columns.
    '''
    products_query = (models.UserProduct.select(models.Product)
                      .join(models.Product,
                            on=(models.UserProduct
                                .product_id == models.Product.id))
                      .join(models.User,
                            on=(models.UserProduct.user_id == models.User.id))
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
    query = (models.ProductTag.select(models.Tag.name.alias('tag_name'),
                                      models.Product.name.alias('product_name')
                                      )
             .join(models.Tag, on=(models.Tag.id == models.ProductTag.tag_id))
             .join(models.Product,
                   on=models.Product.id == models.ProductTag.product_id)
             .where(models.ProductTag.tag_id == tag_id))

    return [item for item in query.dicts()]


def add_product_to_catalog(user_id, product):
    '''
    Add a product to the Product table
    Add the product ID to to the UserProduct table

    Arguments:
    user_id -- int
    product -- string

    Returns:
    int -- product_id
    '''

    product = models.Product.create(name=product,
                                    description='',
                                    price=25.236,
                                    quantity=1,
                                    )
    models.UserProduct.create(user_id=user_id, product_id=product)

    return product


def update_stock(product_id, new_quantity):
    '''
    Update quantity at product_id

    returns number of rows affected. Supposed to be one
    '''
    result = (models.Product.update(quantity=new_quantity)
              .where(models.Product.id == product_id)
              .execute())
    return result


def purchase_product(product_id, buyer_id, quantity):
    '''
    registers a purchase from a product by a buyer

    Returns:
    int -- id of inserted row
    '''
    result = (models.Purchase.insert(product_id=product_id, user_id=buyer_id,
                                     quantity=quantity)
              .execute())
    return result


def remove_product(product_id):
    '''
    removes products form userproduct table where product_id = product_id

    Returns:
    int -- number of rows affected
    '''
    result = (models.UserProduct.delete()
              .where(models.UserProduct.product_id == product_id)
              .execute())
    return result

def did_you_mean(term):
    '''searches for string that look like term'''
    p = models.Product
    query = (p.select(p.name, p.description))
    words = []
    for index, value in enumerate(query):
        words.append(value.name.lower().split(' '))
        for item in value.description.lower().split(' '):
            words[index].append(item)

    unique_letters = list(set(term))
    unique_letters.sort()
    

if __name__ == "__main__":
    print('### STARTING ###')
    #result = search("bloempot")
    # result = list_products_per_tag(1)
    # result = list_user_products(1)
    # result = add_product_to_catalog(1, "TV")
    # add_product_to_catalog(1, "TV")
    # update_stock(4, 4)
    # purchase_product(2,8,100)
    # remove_product(4)
    print(type(result))
    try:
        if result:
            print('--- PRINTING ---')
            # print(result)
            for i in result:
                print(i.name)
            print('--- END PRINTING ---')
    except NameError:
        print("'result' doesn't exists")

    print('### ENDING ###')
