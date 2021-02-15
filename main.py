__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models

def search(term):
    return (models.Product.select()
            .where(models.Product.name == term))


def list_user_products(user_id):
    products_query =  (models.UserProduct.select(models.Product)
                       .join(models.Product, on=(models.UserProduct.product_id == models.Product.id))
                       .join(models.User, on=(models.UserProduct.user_id == models.User.id))
                       .where(models.UserProduct.user_id == user_id)
                       )
    return [item for item in products_query.namedtuples()]


def list_products_per_tag(tag_id):
    return (models.ProductTag.select())


def add_product_to_catalog(user_id, product):
    pass


def update_stock(product_id, new_quantity):
    pass


def purchase_product(product_id, buyer_id, quantity):
    pass


def remove_product(product_id):
    pass

if __name__ == "__main__":
    #result = search("Bloempot")
    print('### STARTING ###')
    result = list_user_products(1)
    
    print('--- PRINTING ---')
    print(result)
    for i in result:
        print(i.name)
    print('--- END PRINTING ---')
        
    
    print('### ENDING ###')
  