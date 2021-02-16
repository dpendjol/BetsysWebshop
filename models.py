# Models go here
#from peewee import Model, Database, CharField, DecimalField, IntegerField, ForeignKeyField, ManyToManyField, Check
import peewee

# In conjunction with the default AutoField behaviour (where deleted record IDs can be reused), 
# this can lead to subtle bugs. To avoid problems, I recommend that you enable foreign-key constraints
db = peewee.SqliteDatabase("mydatabase.db", pragmas={'foreign_keys': 1})

class BaseModel(peewee.Model):
    class Meta:
        database = db
        
# City and county can be set in lookup table
class Address(BaseModel):
    street = peewee.CharField()
    housenumber = peewee.CharField(max_length=10) # incl. supplement
    zipcode = peewee.CharField(max_length=6) #dutch zipcodes without space
    city = peewee.CharField()
    country = peewee.CharField()
class User(BaseModel):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    address = peewee.ForeignKeyField(Address)
    billing_address = peewee.ForeignKeyField(Address)
    
class Tag(BaseModel):
    name = peewee.CharField(unique=True)

class Product(BaseModel):
    name = peewee.CharField()
    description = peewee.CharField()
    price = peewee.DecimalField(max_digits=10, decimal_places=2, auto_round=True)  # 00000000.00
    quantity = peewee.IntegerField(constraints=[peewee.Check('quantity >= 0')])
    tags = peewee.ManyToManyField(Tag)

class UserProduct(BaseModel):
    user_id = peewee.ForeignKeyField(User)
    product_id = peewee.ForeignKeyField(Product)

class Purchase(BaseModel): # Transaction is a reserved SQL keyword
    user_id = peewee.ForeignKeyField(User)
    product_id = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField(constraints=[peewee.Check('quantity >= 0')])

ProductTag = Product.tags.get_through_model()
        
def create_tables():
    with db as dbase:
        db.drop_tables([User,
                          Product,
                          Tag,
                          ProductTag,
                          Purchase,
                          ])
        db.create_tables([User,
                          Product,
                          Address,
                          Tag,
                          ProductTag,
                          UserProduct,
                          Purchase,
                          ])
        
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
        Address.create(
            street=item[0],
            housenumber=item[1],
            zipcode=item[2],
            city=item[3],
            country=item[4]
        )

    for item in user_data:
        User.create(
            first_name=item[0],
            last_name=item[1],
            address=item[2],
            billing_address=item[3]
        )

    for item in tag_data:
        Tag.create(
            name=item[0]
        )

    for item in transaction_data:
        Purchase.create(
            user_id=item[0],
            product_id=item[1],
            quantity=item[2]
        )

    for item in user_product_data:
        UserProduct.create(
            user_id=item[0],
            product_id=item[1]
        )
    
    for item in product_tag_data:
        ProductTag.create(
            product_id=item[0],
            tag_id=item[1]
        )
        


if __name__ == "__main__":
    create_tables()
