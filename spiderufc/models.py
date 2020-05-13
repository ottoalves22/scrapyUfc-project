from mongoengine import *

class Fighter(Document):
    nickname = StringField()
    real_name = StringField()
    category_position = StringField()
    strike_prec = IntField()
    grap_prec = IntField()
    height = FloatField()
    arm_wingspan = FloatField()
    leg_wingspan = FloatField()

    meta ={'collection': 'fighters'}