import collections

FEMALE = 1
MALE = 2
MALE_DESC = "мужчина"
FEMALE_DESC = "женщина"

relation = {
    1: ['не женат', 'не замужем'],
    2: ['есть друг', 'есть подруга'],
    3: ['помолвлен', 'помолвлена'],
    4: ['женат', 'замужем'],
    5: ['всё сложно'],
    6: ['в активном поиске'],
    7: ['влюблён', 'влюблена'],
    8: ['в гражданском браке']
}

map_relation = collections.ChainMap(relation)

relation_str = ", ".join(sum([*map_relation.values()], []))

actions = ["возраст", "пол", "город", "статус"]