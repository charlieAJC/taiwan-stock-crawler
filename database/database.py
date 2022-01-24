import pymysql
import settings


# {Function 連線並執行給定的sql}
# {Input sql {string} 查詢的 sql 指令}
# {Return tuple|boolean 查詢成功回傳資料 tuple，寫入成功回傳空 tuple，執行失敗回傳 False}
def run_sql(sql):
    db = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        db=settings.DB_DATABASE,
        charset='utf8'
    )
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
    except Exception as err:
        print(f"run_sql error: {err}")
        print(f"sql:{sql}")
        db.rollback()
        data = False

    db.close()
    return data
# 暫時不使用 class
# class database_operation:
#     # {Function 連線並執行給定的sql}
#     # {Input sql {string} 查詢的 sql 指令}
#     # {Return tuple|boolean 查詢成功回傳資料 tuple，寫入成功回傳空 tuple，執行失敗回傳 False}
#     def run_sql(self, sql):
#         db = pymysql.connect(
#             host=settings.DB_HOST,
#             port=settings.DB_PORT,
#             user=settings.DB_USERNAME,
#             password=settings.DB_PASSWORD,
#             db=settings.DB_DATABASE,
#             charset='utf8'
#         )
#         cursor = db.cursor()
#         try:
#             cursor.execute(sql)
#             db.commit()
#             data = cursor.fetchall()
#         except:
#             db.rollback()
#             data = False

#         db.close()
#         return data
