from dictionaries import MALE_DESC, MALE, FEMALE_DESC, FEMALE, map_relation, relation_str

message = "20 Мужчина Москва женат"


class MessageChecker:

    def __init__(self, vkm, db):
        self.vkm = vkm
        self.db = db

    @staticmethod
    def is_age(text):
        age = 0
        errors = []
        try:
            age = int(text)
        except Exception:
            errors.append('Возраст должен быть числом от 18 до 120')
        if age < 18 or age > 120:
            errors.append("Укажите возраст от 18 до 120")
        return {"age": age, "errors": errors}

    @staticmethod
    def is_sex(text):
        sex = None
        errors = []
        if text.lower() == MALE_DESC:
            sex = MALE
        else:
            if text.lower() == FEMALE_DESC:
                sex = FEMALE
            else:
                errors.append("Укажите пол женщина или мужчина")

        return {"sex": sex, "errors": errors}

    @staticmethod
    def is_relation(text):
        relation = None
        errors = []
        for k in map_relation.keys():
            for v in map_relation[k]:
                if text.lower().__contains__(v):
                    relation = k
                    break
            else:
                continue
            break
        if relation is None:
            errors.append("Неизвестный тип семейного положения. Возможные значения: " + relation_str)

        return {"relation": relation, "errors": errors}

    @staticmethod
    def is_hometown(text):
        errors = []
        hometown = text
        if len(hometown) > 50:
            errors.append("Максимальная длина города 50 символов")
        if len(hometown) == 0:
            errors.append("Введите значение для города")

        return {"hometown": hometown, "errors": errors}

    def check_user(self, user, text) -> bool:
        if not user.is_fulfilled():
            if not user.age_exist():
                res = self.is_age(text)
                if len(res["errors"]) == 0:
                    self.db.save_age(user, res["age"])
                else:
                    self.vkm.write_request(user.id, "возраст", res["errors"])
                    return False
            if not user.sex_exist():
                res = self.is_sex(text)
                if len(res["errors"]) == 0:
                    self.db.save_sex(user, res["sex"])
                else:
                    self.vkm.write_request(user.id, "пол", res["errors"])
                    return False
            if not user.relation_exist():
                res = self.is_relation(text)
                if len(res["errors"]) == 0:
                    self.db.save_relation(user, res["relation"])
                else:
                    self.vkm.write_request(user.id, "семейное положение", res["errors"])
                    return False
            if not user.hometown_exist():
                res = self.is_hometown(text)
                if len(res["errors"]) == 0:
                    self.db.save_hometown(user, res["hometown"])
                else:
                    self.vkm.write_request(user.id, "город", res["errors"])
                    return False
        return True


def read_message(mess):
    age = 0
    sex = '1/2'
    hometown = ''
    relation = '0..8'
    res = mess.split(" ", 2)
    print(res)
    errors = []
    # is_age(res[0])
    # is_sex(res[1])
    part_with_relation = res[2]
    for k in map_relation.keys():
        for v in map_relation[k]:
            if part_with_relation.lower().__contains__(v):
                relation = k
                hometown = part_with_relation[0:len(part_with_relation) - len(v)].strip()
                break
        else:
            continue
        break
    if len(hometown) > 50:
        errors.append("Максимальная длина города 50 символов")

    result = {'age': age, 'sex': sex, 'relation': relation, 'hometown': hometown, 'errors': errors}
    print(result)
    return result


#readMessage(message)
