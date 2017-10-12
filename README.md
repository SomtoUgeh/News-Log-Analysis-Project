# Newspaper Analysis Project
This is a reporting tool that prints out reports (in plain text) based on the data in the NEWS database. This reporting tool is a Python program using the psycopg2 module to connect to the database.  The program is run using  `python3 LogAnalysis.py`  in the terminal.


## Requirement for the Project
* The Project makes use of [Vagrant](vagrantup.com/downloads.html) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads) for the database setup
* After downloading Vagrant and Virtual Box, a setup folder can be downloaded from [HERE](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
* Download the setup folder and Unzip its content 
* In the terminal, cd into the folder and  type `vagrant up` to set up vagrant 
* Once the setup is done, type `vagrant ssh` to access the working environment
* A shared folder than accessed can be accessed using  `cd /vagrant`
* You would also need to download the [DATA](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)containing newsdata.sql 
* Move the newsdata.sql file to the vagrant folder 
* In your terminal, type `psql -d news -f newsdata.sql`

**psql** — the PostgreSQL command line program

**-d news** — connect to the database named news which has been set up for you

**-f newsdata.sql** — run the SQL statements in the file newsdata.sql

* In the terminal, type `psql -d news` to access the database 
* `\d` can be used to navigate the tables available in the database 


## Questions
1. **What are the most popular three articles of all time?** Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

      Example:
        "Princess Shellfish Marries Prince Handsome" — 1201 views

2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

      Example:
        Ursula La Multa — 2304 views

3. **On which days did more than 1% of requests lead to errors?** 

      Example:
        July 29, 2016 — 2.5% errors


## Tables Used In Project 
1. Articles
2. Log
3. Authors


**VIEWS** were used to store composition of tables in the Database 

1. **Finally** from the articles and authors table, this will be used for the second question:

* create view finally as select title, slug, name from articles, authors
where articles.author = authors.id;

```
              "select finally.name, count(log.path) as num "
              "from finally left join log on log.path = concat( '/article/', finally.slug) "
              "group by finally.name "
              "order by num desc;
```

2. **Total_views** from the log table, this will output all the views per day 

```
create view total_views as select date(time) as date, count(*) as total_view from log group by date(time);
```

3. **error_views** from the log table, this will output all the error (‘404 NOT FOUND’) per day 

```
create view error_views as select date(time) as date, count(*) as errors from log where status != '200 OK' group by date(time);
```

4. **Final_error** from total_view and error_views for the third question

```
create view final_error as select total_views.date, error_views.errors, total_views.total_view from total_views, error_views where total_views.date=error_views.date order by total_views.date;
```

5. **Answers** from final_error, this performs the mathematic calculation for the percentage error in the third question.

```
create view answer as select 100 - ((total_view - errors)/total_view::float)*100 as error_perc, date from final_error;
```





