# **Logs Analysis Project**
### by Bijan Marashi (bm6410@att.com)

This project is my attempt at completing the Logs Analysis project.


### **Installation**

Just copy the news_project.py file to your local.  

### **Usage**

To launch the app, run the news_project.py file in any python shell.  

The app will display the following report data:

1. The three most popular articles of all time, based on number of page views
2. A ranking of the most popular authors of all time, based on the number of
views their articles have gotten
3. Which day had more than 1% error requests

The code makes use of views for the final report.  The views are created as
follows:

CREATE VIEW total_logs AS SELECT date_trunc('day', log.time) "day", COUNT(\*)
  FROM log GROUP BY day;
CREATE VIEW total_errors AS SELECT date_trunc('day', log.time) "day",
  COUNT(\*) AS errors FROM log WHERE status NOT LIKE '%200%' GROUP BY day
  ORDER BY day;
CREATE VIEW error_rates AS SELECT to_char(total_logs.day, 'Mon DD, YYYY')
  AS "day", round((total_errors.errors * 100.0) / total_logs.count, 2)
  AS rate FROM total_logs, total_errors WHERE total_logs.day = total_errors.day;"


## **HAVE FUN!**
