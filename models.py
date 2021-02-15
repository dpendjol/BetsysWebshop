# Models go here
from peewee import Model, Database, CharField, DecimalField, IntegerField, ForeignKeyField, ManyToManyField

db = Database()

class User(Model):
    name = CharField()
    street = CharField()
    housenumber = CharField()
    zipcode = CharField()
    city = CharField()
    country = CharField()

    class Meta:
        database = db


class Product(Model):
    name = CharField()
    description = CharField()
    price = DecimalField(max_digits=10, decimal_places=2, auto_round=True)  # 00000000.00
    quantity = IntegerField()
    tags = ManyToManyField()

    class Meta:
        databse = db

class Tag(Model):
    name = CharField(unique=True)

    class Meta:
        database = db

class Transaction(Model):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
    quantity = IntegerField()
    
    class Meta:
        database = db
        
def create_tables():
    with db:
        db.create_tables([User,
                          Product,
                          Tag,
                          Transaction])