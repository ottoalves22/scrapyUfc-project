from mongoengine import *

class Fighter(Document):
    nickname = StringField()
    real_name = StringField()
    category_position = StringField()
    win_streak = IntField()
    win_ko = IntField()
    win_subm = IntField()
    strike_prec = IntField()
    grap_prec = IntField()
    height = FloatField()
    armWingspan = FloatField()
    legWingspan = FloatField()