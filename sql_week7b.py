import sys, os, psycopg2, math

database = sys.argv[1]
user = os.environ.get('PGUSER')
password = os.environ.get('PGPASSWORD')
host = os.environ.get('PGHOST')
port = os.environ.get('PGPORT')
f = open('parameter.txt', 'r')
namestring = f.read() + '%'

try:
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)

    cursor = connection.cursor()
    postgreSQL_select_Query = "select sum(host_team_score) from matches inner join match_referees on matches.match_num = match_referees.match_num inner join referees on match_referees.referee = referees.referee_id inner join teams on host_team_id = teams.team_id where host_team_score > guest_team_score and teams.name like %s"
    cursor.execute(postgreSQL_select_Query, (namestring,))
    host_team_score_sum = cursor.fetchone()

    if host_team_score_sum is not None:
        score = host_team_score_sum[0]

    print(round(math.cos(score * 10 * (math.pi / 180)), 2))


except (Exception, psycopg2.Error) as error:
    print("Error fetching data from PostgreSQL table", error)
finally:
    # closing database connection
    if connection:
        cursor.close()
        connection.close()

