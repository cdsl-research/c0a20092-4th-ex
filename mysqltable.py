import os
import mysql.connector
import subprocess

command = "kubectl get pod | grep mysql | awk '{print $1}'"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
pod_name = stdout.decode("utf-8").strip()

describe_command = f'kubectl describe pod {pod_name} | grep IP:'
describe_process = subprocess.Popen(describe_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
describe_stdout, describe_stderr = describe_process.communicate()

pod_ip = describe_stdout.decode("utf-8").strip().split(" ")[-1]
print(pod_ip)

# MySQLに接続
conn = mysql.connector.connect(
        host=pod_ip,
        port=3306,
        user="Your_User",
        password="Your_Password",
        database="Your_Database"
        )
cursor = conn.cursor(dictionary=True)  # カラム名を含む辞書形式の結果を取得

# ①: "show tables" の出力結果をファイルに保存
cursor.execute("SHOW TABLES")
tables = [table["Tables_in_Your_Database"] for table in cursor.fetchall()]
with open("tables.txt", "w") as file:
    for table in tables:
        file.write(table + "\n")

# ②: テーブル名とカラム情報を辞書に登録
table_column_dict = {}
for table in tables:
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    columns = cursor.fetchall()
    column_info = {}
    for column in columns:
        if 'text' in column['Type'].lower() or 'varchar' in column['Type'].lower():
            column_info[column['Field']] = column['Type']
    table_column_dict[table] = column_info

# ③ and ④: テーブルから検索と文字列の置換
search_string = "Your_old_link"
replacement_string = "Your_new_link"

for table, columns in table_column_dict.items():
    for column, column_type in columns.items():
        update_query = f"UPDATE {table} SET {column} = REPLACE({column}, %s, %s) WHERE {column} LIKE %s"
        cursor.execute(update_query, (search_string, replacement_string, f'%{search_string}%'))
        conn.commit()

# MySQL接続をクローズ
cursor.close()
conn.close()
