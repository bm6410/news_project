import psycopg2

# #!/usr/bin/env python3

"""news_project.py: Runs some reports against a psql news database."""

__author__ = "Bijan Marashi (bm6410@att.com)"

# the db we're using for this
DBNAME = "news"

# Views
total_logs = "CREATE VIEW total_logs AS SELECT " + \
    "date_trunc('day', log.time) \"day\", COUNT(*) FROM log GROUP BY day;"
total_errors = "CREATE VIEW total_errors AS SELECT " + \
    "date_trunc('day', log.time) \"day\", COUNT(*) AS errors FROM log " + \
    "WHERE status NOT LIKE '%200%' GROUP BY day ORDER BY day;"
error_rates = "CREATE VIEW error_rates AS SELECT " + \
    "to_char(total_logs.day, 'Mon DD, YYYY') AS \"day\", " + \
    "round((total_errors.errors * 100.0) / total_logs.count, 2) AS rate " + \
    "FROM total_logs, total_errors WHERE total_logs.day = total_errors.day;"

# SELECT statements
select_popular_articles = \
    "SELECT quote_ident(title), COUNT(*) AS views FROM log, articles " + \
    "WHERE log.path LIKE '%' || articles.slug GROUP BY articles.title " + \
    "ORDER BY views DESC LIMIT 3;"
select_popular_authors = \
    "SELECT name, COUNT(*) AS views FROM log, articles, authors WHERE " + \
    "log.path LIKE '%' || articles.slug and articles.author = authors.id " + \
    "GROUP BY authors.name ORDER BY views DESC;"
select_error_rates = \
    "SELECT day, rate AS errors FROM error_rates WHERE rate > 1.0;"

# db connection stuff
db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# question #1 - get the popular articles, then format the output
c.execute(select_popular_articles)
# Heading
print("\n1. What are the most popular three articles of all time?\n")
rows = c.fetchall()
for item in rows:
    print(item[0] + " - " + str(item[1]) + " views")

# question #2 - get the most popular authors, then format the output
c.execute(select_popular_authors)
# Heading
print("\n2. Who are the most popular article authors of all time?\n")
rows = c.fetchall()

for item in rows:
    print(item[0] + " - " + str(item[1]) + " views")

# question #3 - get the days with more the 1% errors, then format the output
# Since this is complicated, we'll create some views, then query against those

# Create the views for the report
c.execute(total_logs)
c.execute(total_errors)
c.execute(error_rates)

print("\n3. On which days did more than 1% of requests lead to errors?\n")
c.execute(select_error_rates)
rows = c.fetchall()
for item in rows:
    print(item[0] + " - " + str(item[1]) + "% errors")

# close up shop - we're done
db.close()
