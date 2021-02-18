__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from models import Product, UserProduct, User, ProductTag
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
                               Product.name.alias('product_name'))
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
    product -- string

    Returns:
    int -- product_id
    '''

    product = Product.create(name=product,
                             description='',
                             price=25.236,
                             quantity=1,
                             )
    UserProduct.create(user_id=user_id, product_id=product)

    return product


def update_stock(product_id, new_quantity):
    '''
    Update quantity at product_id

    returns number of rows affected. Supposed to be one
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
