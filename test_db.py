import db_manager as db

db.create_database()
conn = db.connect()
create = db.create_tables(conn)
user_creat = db.Insert_User_info(conn,"2345","omer kemal","3234","Teacher")
user_info = db.user(conn,"omer kemal","3234","search")[0]
insert = db.insert_Teacher_info(conn,user_info[0],"m-ath","G6","omer","kemal","mathsmatics")


print(f"created user {user_creat}")
print(f"user info: {user_info}")
print(f"insert info: {insert}")
