import os

import psycopg2


# DB_URL = os.environ.get("DATABASE_URL")

# #conn = psycopg2.connect(dbname="sdbgDB",user="admin",password = "147753",host="localhost")


# def request_DB(insert:bool,sql_request:str):
#     conn = psycopg2.connect(dbname="sdbgDB",user="admin",password = "147753",host="localhost")
#     cursor = conn.cursor()
#     if insert:
#         cursor.execute(sql_request)
#         curosr.commit()
#         cursor.close()
#         conn.close()
#         return
#     else:
#         cursor.execute(sql_request)
#         records = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return records
 
#     pass

# def get_login_in_DB(login:str,password:str):
#     sql_req = "select name_user from users where name_user = '{}'".format(login)
#     answer = request_DB(False,sql_req)
#     if not answer:
#         return "this login is not."
#     else:
#         sql_req = "select password_user from users where name_user = '{}'".format(login)
#         answer = request_DB(False,sql_req)
#         if answer == password:
#             return "Sign up"
#         else:
#             return "password is not right"
    
#     pass

# def set_login_in_DB(login:str,password:str):
#     sql_req = "select name_user from users where name_user = '{}'".format(login)
#     answer = request_DB(False,sql_req)
#     if not(answer == ""):
#         return "this login alredy is."

#     else:
#         sql_req = "insert into users values(nextval('users_id_seq'),'{0}','{1}'')".format(login,password)
#         answer = request_DB(True,sql_req)
#         return "new user"
#     pass


class WorkWithDB:

    def __init__(self, DATABASE_URL):
        if type(DATABASE_URL) == str:            
            self.DB_URL = DATABASE_URL

        elif type(DATABASE_URL) == dict:
            self.dbname = DATABASE_URL["dbname"]
            self.user = DATABASE_URL["user"]
            self.password = DATABASE_URL["password"]
            self.host = DATABASE_URL["host"]

        else:         
            raise TypeError("arument DATABASE_URL is`t dict or str.")
    
    def connect_db(self):
        try:        
            return psycopg2.connect(self.DB_URL)

        except AttributeError:
            return psycopg2.connect(dbname=self.dbname, user=self.user,
                    password=self.password, host=self.host)

    def req_select_db(self, select_columns:str, select_table:str,
            select_where:str):
        conn = self.connect_db()
        cursor = conn.cursor()
        if select_where != "": 
            select_where = "where {}".format(select_where)

        sql_request = "select {} from {} {}".format(select_columns,
                select_table, select_where)
        cursor.execute(sql_request)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return records
        

    def req_insert_db(self, name_table:str, values:str, into:str="into"):
        conn = self.connect_db()
        cursor = conn.cursor()
        sql_request = "insert {} {} values({})".format(into,
                name_table, values)
        cursor.execute(sql_request)
        conn.commit()
        cursor.close()
        conn.close()

    def req_update_db(self, name_table:str, set_value:str,
             where_update:str):
        conn = self.connect_db()
        cursor = conn.cursor()
        sql_request = "update {} set {} where {}".format(name_table, 
                set_value, where_update)
        cursor.execute(sql_request)
        conn.commit()
        cursor.close()
        conn.close()        

        pass

    def req_delete_db(self, name_table:str, where_request:str):
        conn = self.connect_db()
        cursor = conn.cursor()
        sql_request = "delete from {} where {}".format(name_table,
                where_request)
        cursor.execute(sql_request)
        conn.commit()
        cursor.close()
        conn.close()      

    def check_log_and_pass_user(self, login:str, password:str):
        record = self.req_select_db("name_user", "users",
                "name_user = '{}'".format(login))
        if record:
            record = self.req_select_db("password_user", "users",
                    "name_user = '{}' and password_user = '{}'".format(
                    login, password))
            try:
                if record[0][0] == password:
                    return True

            except IndexError:
                return False

        else:
            return "Login don`t exist"

    def create_rating_user(self, login:str, number_level:int):
        where_request = "name_user = '{}'".format(login)
        id_user = self.req_select_db("id", "users", where_request)
        values = """nextval('rating_id_seq'), 0, now(),
            {}, {}""".format(id_user[0][0], number_level)
        self.req_insert_db("rating", values)

    def signup_in_game(self, login:str, password:str):
        record = self.req_select_db("name_user", "users",
                "name_user = '{}'".format(login))
        if not record:
            values = "nextval('users_id_seq'),'{}','{}'".format(login,
                 password)
            self.req_insert_db("users", values)
            self.create_rating_user(login, 1)

            return True

        else:
            return False

    def delete_user(self, login:str, password:str):
        record = self.req_select_db("password_user", "users",
                "name_user = '{}'".format(login))
        if record[0][0] == password:
            self.req_delete_db("users", "name_user = '{}'".format(login))
            return True
        else:
            return "Don`t right password"

    def update_score(self, login:str, score_user:int, number_level:int):
        set_value = "score = {}".format(score_user)
        where_request = """
                id_user = (select id from users where name_user = '{}')
                and number_level = {};
                """.format(login, number_level)
        self.req_update_db("rating", set_value, where_request)

    def select_top_10(self, number_level:int):
        columns = "name_user, score, date_add"
        tables = "users, rating"
        where_request = """users.id = rating.id_user and
         rating.number_level = {} order by score desc
         limit 10""".format(number_level)
        return_val = self.req_select_db(columns, tables, where_request)
        for i in range(len(return_val)):
            return_val[i][2] = str(return_val[i][2])

        return return_val

    def prevate_score(self, login:str, number_level:int):
        columns = "score"
        tables = "rating, users"
        where_request = """users.name_user = '{}' and
         rating.number_level = {}""".format(login, number_level)
        record = self.req_select_db(columns,tables,where_request)
        return record
