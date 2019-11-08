import os

import psycopg2

from DBConnect import DBConnect

class WorkWithUser:

    db_url = os.environ.get('DATABASE_URL')
    tab_users = DBConnect(db_url, "users")
    tab_rating = DBConnect(db_url, "rating")
    tab_users_rating = DBConnect(db_url, "{}, {}".format(tab_users.table,
            tab_rating.table))

    def create_rating_user(self, login, number_level):
        where_request = "name_user = '{}'".format(login)
        id_user = self.tab_users.req_select_db("id", where_request)
        values = """nextval('rating_id_seq'), 0, now(),
            {}, {}""".format(id_user[0][0], number_level)
        self.tab_rating.req_insert_db(values)

    def check_text_char(self, text):
        characters = """ABCDEFGHIKLMNOPQRSTVXYZ
            abcdefghiklmnopqrstvxyz1234567890"""
        for i in text:
            find = False
            for j in characters:
                if i == j:
                    find = True
                    break
            if not find:
                return False
        return True

    def check_text_len(self, text, len_text):
        if len(text) < len_text:
            return False
        else:
            return True

    def validation_of_login_password(self, login, password):
        if (self.check_text_char(login) and
                self.check_text_char(password) and
                self.check_text_len(login, 5) and
                self.check_text_len(password, 6)):
            return True

        else:
            return False

    def signup_in_game(self, login, password):
        record = self.tab_users.req_select_db("name_user",
                "name_user = '{}'".format(login))
        if not record and self.validation_of_login_password(login, 
                password):
            values = "nextval('users_id_seq'),'{}','{}'".format(login,
                 password)
            self.tab_users.req_insert_db(values)
            self.create_rating_user(login, 1)

            return True

        else:
            return False

    def signin_in_game(self, login, password):
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
            return False


    def delete_user(self, login, password):
        record = self.tab_users.req_select_db("password_user",
                "name_user = '{}'".format(login))
        try:
            if record[0][0] == password:
                self.tab_users.req_delete_db("name_user = '{}'".format(login))
                return True
         
            else:
                return False
       
        except IndexError:
            return False

    def update_score(self, login, score_user, number_level):
        set_value = "score = {}, date_add = now()".format(score_user)
        where_request = """
                id_user = (select id from users where name_user = '{}')
                and number_level = {};
                """.format(login, number_level)
        self.tab_rating.req_update_db(set_value, where_request)

    def select_top_10(self, number_level):
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

    def prevate_score(self, login, number_level):
        columns = "score"
        id_user = self.tab_users.req_select_db("id",
                "name_user = '{}'".format(login))
        try:
            where_request = """id_user = {} and
                    number_level = {}""".format(id_user[0][0], number_level)
            record = self.tab_rating.req_select_db(columns,
                    where_request)
           
            return record[0][0]

        except IndexError:
            return False

    def max_number_level(self, login):
        id_user = self.tab_users.req_select_db("id", 
                "name_user = '{}'".format(login))
        record = self.tab_rating.req_select_db("max(number_level)",
                 "id_user = {}".format(id_user[0][0]))
        return record[0][0]








