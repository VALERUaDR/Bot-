import sqlite3

from model import VKUser

CREATE_VK_USER = 'CREATE TABLE IF NOT EXISTS VKUSER' \
                 '(id integer primary key ,' \
                 'age integer,' \
                 'sex boolean,' \
                 'hometown VARCHAR(100),' \
                 'relation integer )'

CREATE_VKUSER_MATCH = 'CREATE TABLE IF NOT EXISTS VKUSER_MATCH' \
                      '(vkuser_id integer,' \
                      'match_id integer  )'
MATCH_INDEX = 'CREATE INDEX IF NOT EXISTS MATCHES ON VKUSER_MATCH (vkuser_id, match_id)'

DATABASE = "vkinder.db"


class KinderDatabase:

    def __init__(self):
        global con
        try:
            con = sqlite3.connect(DATABASE)
            con.execute(CREATE_VK_USER)
            con.execute(CREATE_VKUSER_MATCH)
            con.execute(MATCH_INDEX)
            # print('Database initialized')
        except sqlite3.Error as error:
            print('Error while connecting to sqlite', error)
        finally:
            if con:
                con.close()
                # print('The SQLite connection is closed')

    def find_user(self, user_id: int) -> [VKUser, None]:
        global con
        try:
            con = sqlite3.connect(DATABASE)
            args = (user_id,)
            res = con.execute("SELECT id, age, sex, hometown, relation from VKUSER where id = ?", args)
            row = res.fetchone()
            if row is None:
                return None
            else:
                return VKUser(row[0], row[1], row[2], row[3], row[4])
        except sqlite3.Error as error:
            print('Error while connecting to sqlite', error)
        finally:
            if con:
                con.close()
                # print('The SQLite connection is closed')

    def execute_change(self, sql, args):
        global con
        try:
            con = sqlite3.connect(DATABASE)
            res = con.execute(sql, args)
            con.commit()
            return res
        except sqlite3.Error as error:
            print('Error while connecting to sqlite', error)
        finally:
            if con:
                con.close()

    def create_user(self, user: VKUser):
        self.execute_change("INSERT INTO VKUSER(id, age, sex, hometown, relation) VALUES (?,?,?,?,?)",
                            (user.id, user.age, user.sex, user.hometown, user.relation))

    def save_age(self, user, age):
        self.execute_change("UPDATE VKUSER SET age = ? where id = ?", (age, user.id))

    def save_sex(self, user, sex):
        self.execute_change("UPDATE VKUSER SET sex = ? where id = ?", (sex, user.id))

    def save_relation(self, user, relation):
        self.execute_change("UPDATE VKUSER SET relation = ? where id = ?", (relation, user.id))

    def save_hometown(self, user, hometown):
        self.execute_change("UPDATE VKUSER SET hometown = ? where id = ?", (hometown, user.id))

    def has_match(self, id, match_id):
        global con
        try:
            con = sqlite3.connect(DATABASE)
            args = (id, match_id)
            res = con.execute("SELECT count() FROM VKUSER_MATCH WHERE vkuser_id = ? and match_id = ?", args)
            row = res.fetchone()
            if row[0] == 0:
                return False
            else:
                return True
        except sqlite3.Error as error:
            print('Error while connecting to sqlite', error)
        finally:
            if con:
                con.close()

    def save_match(self, id, match_id):
        self.execute_change("INSERT INTO VKUSER_MATCH (vkuser_id, match_id) VALUES ( ?, ? )", (id, match_id))

    def reset_field(self, user, action):
        updt = "UPDATE VKUSER SET {field} = NULL where id = ?"
        if action == "возраст":
            updt = updt.replace("{field}", "age")
        if action == "пол":
            updt = updt.replace("{field}", "sex")
        if action == "город":
            updt = updt.replace("{field}", "hometown")
        if action == "статус":
            updt = updt.replace("{field}", "relation")
        self.execute_change(updt, (user.id,))
