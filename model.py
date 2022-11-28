
class VKUser:

    def __init__(self, id, age, sex, hometown, relation):
        self.id = id
        self.age = age
        self.sex = sex
        self.hometown = hometown
        self.relation = relation

    def is_fulfilled(self) -> bool:
        return self.age is not None \
               and self.sex is not None \
               and self.hometown is not None \
               and self.relation is not None

    def age_exist(self) -> bool:
        return self.age is not None

    def sex_exist(self) -> bool:
        return self.sex is not None

    def relation_exist(self) -> bool:
        return self.relation is not None

    def hometown_exist(self) -> bool:
        return self.hometown is not None