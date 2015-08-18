#!/usr/bin/env python
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto import dynamodb2
from boto.dynamodb2.table import Table

class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = "dynamodb-user"
        host = "http://localhost:8000"
    email = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute(range_key=True)
    last_name = UnicodeAttribute(hash_key=True)


def create_table():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1)

    UserModel.dump("test.json")

def add_table():
    #user_item = UserModel("Jack", "Oph")
    user_item = UserModel(first_name="Jack", last_name="Oph")
    user_item.save()

def query_table():
    users = UserModel.scan()
    for u in users:
        print "LOLOL"
        #print u['first_name']
        print u.first_name
    
def dump():
    content = UserModel.dumps()
    print content

if __name__ == "__main__":
    #add_table()
    query_table()
    dump()
