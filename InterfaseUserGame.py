import os

import psycopg2

from DBConnect import DBConnect

class WorkWithUser:

    # db_url = {
    #     "dbname":"sdbgDB",
    #     "user":"admin",
    #     "password" : "147753",
    #     "host":"localhost"
    #     }
    db_url = os.environ.get('DATABASE_URL')
    tab_users = DBConnect(db_url, "users")
    tab_rating = DBConnect(db_url, "rating")
    tab_users_rating = DBConnect(db_url, "{}, {}".format(tab_users.table,
            tab_rating.table))

    def create_rating_user(self, login:str, number_level:int):
        where_request = "name_user = '{}'".format(login)
        id_user = self.tab_users.req_select_db("id", where_request)
        values = """nextval('rating_id_seq'), 0, now(),
            {}, {}""".format(id_user[0][0], number_level)
        self.tab_rating.req_insert_db(values)

    def signin_in_game(self, login:str, password:str):
        record = self.tab_users.req_select_db("name_user",
                "name_user = '{}'".format(login))
        if record:
            record = self.tab_users.req_select_db("password_user",
                    "name_user = '{}' and password_user = '{}'".format(
                    login, password))
            try:
                if record[0][0] == password:
                    return True

            except IndexError:
                return False

        else:
            return "Login don`t exist"

    def signup_in_game(self, login:str, password:str):
        record = self.tab_users.req_select_db("name_user",
                "name_user = '{}'".format(login))
        if not record:
            values = "nextval('users_id_seq'),'{}','{}'".format(login,
                 password)
            self.tab_users.req_insert_db(values)
            self.create_rating_user(login, 1)

            return True

        else:
            return False

    def delete_user(self, login:str, password:str):
        record = self.tab_users.req_select_db("password_user",
                "name_user = '{}'".format(login))
        if record[0][0] == password:
            self.tab_users.req_delete_db("name_user = '{}'".format(login))
            return True
        else:
            return "Don`t right password"

    def update_score(self, login:str, score_user:int, number_level:int):
        set_value = "score = {}, date_add = now()".format(score_user)
        where_request = """
                id_user = (select id from users where name_user = '{}')
                and number_level = {};
                """.format(login, number_level)
        self.tab_rating.req_update_db(set_value, where_request)

    def select_top_10(self, number_level:int):
        columns = "name_user, score, date_add"
        where_request = """users.id = rating.id_user and
         rating.number_level = {} order by score desc
         limit 10""".format(number_level)
        select_val = self.tab_users_rating.req_select_db(columns,
                where_request)
        for i in range(len(select_val)):
            select_val[i] = list(select_val[i])
            select_val[i][2] = str(select_val[i][2])

        return select_val

    def prevate_score(self, login:str, number_level:int):
        columns = "score"
        id_user = self.tab_users.req_select_db("id",
                "name_user = '{}'".format(login))
        where_request = """id_user = {} and
                number_level = {}""".format(id_user[0][0], number_level)
        record = self.tab_rating.req_select_db(columns,
                where_request)
        return record[0][0]
