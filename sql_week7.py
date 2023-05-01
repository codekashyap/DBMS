import os
import psycopg2
import sys

database = sys.argv[1]
user = os.environ.get('PGUSER')
password = os.environ.get('PGPASSWORD')
host = os.environ.get('PGHOST')
port = os.environ.get('PGPORT')
f = open('date.txt', 'r')
string = f.read()
try:
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)

    cursor = connection.cursor()
    postgreSQL_select_Query = "select name from matches inner join match_referees on matches.match_num = match_referees.match_num  inner join referees on match_referees.referee = referees.referee_id where match_date = %s"
    cursor.execute(postgreSQL_select_Query, (string,))
    refree_records = cursor.fetchall()

    for row in refree_records:
        refree_name = row[0]

        if len(refree_name.split()) == 2:
            rname_split = refree_name.split()
            fname = rname_split[1] + " " + rname_split[0][0] + "."

        if len(refree_name.split()) == 3:
            rname_split = refree_name.split()
            fname = rname_split[2] + " " + rname_split[0][0] + ". " + rname_split[1][0] + "."

        print(fname)

except (Exception, psycopg2.Error) as error:
    print("Error fetching data from PostgreSQL table", error)
finally:
    # closing database connection
    if connection:
        cursor.close()
        connection.close()
