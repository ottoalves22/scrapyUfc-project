from mongoengine import *

class Fighter(Document):
    nickname = StringField()
    real_name = StringField()
    category_position = StringField()
    strike_prec = IntField()
    grap_prec = IntField()
    height = FloatField()
    armWingspan = FloatField()
    legWingspan = FloatField()

    meta ={'collection': 'fighters'}