# Models go here
# from peewee import Model, Database, CharField, DecimalField, IntegerField,
# ForeignKeyField, ManyToManyField, Check
import peewee

# ---
# In conjunction with the default AutoField behaviour (where deleted record
# IDs can be reused), this can lead to subtle bugs. To avoid problems,
# I recommend that you enable foreign-key constraints
# ---
# Above taken from peewee documentation
db = peewee.SqliteDatabase(":memory:", pragmas={'foreign_keys': 1})


class BaseModel(peewee.Model):
    class Meta:
        database = db


# City and county can be set in lookup table
class Address(BaseModel):
    street = peewee.CharField()
    number = peewee.CharField(max_length=10)  # incl. supplement
    zipcode = peewee.CharField(max_length=6)  # dutch zipcodes without space
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
    name = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    price = peewee.DecimalField(max_digits=10, decimal_places=2,
                                auto_round=True)  # 00000000.00
    quantity = peewee.IntegerField(constraints=[peewee.Check('quantity >= 0')])
    tags = peewee.ManyToManyField(Tag)


class UserProduct(BaseModel):
    user_id = peewee.ForeignKeyField(User)
    product_id = peewee.ForeignKeyField(Product)


class Purchase(BaseModel):  # Transaction is a reserved SQL keyword
    user_id = peewee.ForeignKeyField(User)
    product_id = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField(constraints=[peewee.Check('quantity >= 0')])


ProductTag = Product.tags.get_through_model()


if __name__ == "__main__":
    pass
