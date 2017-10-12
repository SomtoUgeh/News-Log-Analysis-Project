#!/usr/bin/env python3 LogAnalysis.py

import psycopg2

DBNAME = 'news'


def popular_article():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select articles.title, count(*) as views "
              "from log join articles "
              "on log.path = concat('/article/', articles.slug) "
              "group by articles.title "
              "order by views desc "
              "limit 3;")
    answer1 = c.fetchall()
    db.close()
    return answer1


def popular_author():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select finally.name, count(log.path) as num "
              "from finally left join log "
              "on log.path = concat( '/article/', finally.slug) "
              "group by finally.name "
              "order by num desc;")
    answer2 = c.fetchall()
    db.close()
    return answer2


def error_date():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('select * from answer where error_perc > 1;')
    answer3 = c.fetchall()
    db.close()
    return answer3


if __name__ == "__main__":

    print("\nWhat are the three most popular articles?\n")
    popular_articles = popular_article()
    for article in popular_articles:
        print(" {} -- {} views".format(article[0], article[1]))

    print("\nWhat are the three most popular authors of all time?\n")
    popular_author = popular_author()
    for author in popular_author:
        print(" {} -- {} views".format(author[0], author[1]))

    print("\nOn which days did more than 1% of requests lead to errors?\n")
    error_percentage = error_date()
    for error in error_percentage:
        print(" {} -- {} % errors".format(
            error[1].strftime('%B %d, %Y'), "%.2f" % error[0]))
