import psycopg2
import os


DB_URL = os.environ.get("DATABASE_URL")

#conn = psycopg2.connect(dbname="sdbgDB",user="admin",password = "147753",host="localhost")


def request_DB(insert:bool,sql_request:str):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    if insert:
        cursor.execute(sql_request)
        curosr.commit()
        cursor.close()
        conn.close()
        return
    else:
        cursor.execute(sql_request)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
 
    pass

def get_login_in_DB(login:str,password:str):
    sql_req = "select user_name from users where user_name = {}".format(login)
    answer = request_DB(False,sql_req)
    if answer == "":
        return "this login is not."
    else:
        sql_req = "select password from users where user_name = {}".format(login)
        answer = request_DB(False,sql_req)
        if answer == password:
            return "Sign up"
        else:
            return "password is not right"
    
    pass

def set_login_in_DB(login:str,password:str):
    sql_req = "select user_name from users where user_name = {}".format(login)
    answer = request_DB(False,sql_req)
    if not(answer == ""):
        return "this login alredy is."

    else:
        sql_req = "insert into users values(nextval('users_id_seq'){0},{1})".format(login,password)
        answer = request_DB(True,sql_req)
        return "new user"
    pass










