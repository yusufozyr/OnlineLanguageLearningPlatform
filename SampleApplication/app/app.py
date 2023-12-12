
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from views.home import home_bp
from views.login import login_bp
from views.registerL import registerL_bp





app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'
  
mysql = MySQL(app)  




app.register_blueprint(home_bp, mysql=mysql)
app.register_blueprint(login_bp, mysql=mysql)
app.register_blueprint(registerL_bp, mysql=mysql)






# @app.route('/tasks', methods=['GET', 'POST'])
# def tasks():
#     if 'loggedin' in session:
#         student_id = session['userid']
        
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT c.cid, c.cname, c.quota, c.gpa_threshold FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s', (student_id,))
#         internship_applications = cursor.fetchall()
        
#         cursor.execute('SELECT COUNT(*) AS count FROM apply WHERE sid = %s', (student_id,))
#         application_count = cursor.fetchone()
        
#         return render_template('tasks.html', internship_applications=internship_applications, application_count=application_count)
#     return redirect(url_for('login'))
# @app.route('/apply_internship', methods=['GET', 'POST'])
# def apply_internship():
#     success_message = None
#     error_message = None

#     if request.method == 'POST':
#         student_id = session['userid']
#         company_id = request.form['company_id']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         query = """
#         SELECT c.cid
#         FROM company c
#         LEFT JOIN apply a ON c.cid = a.cid AND a.sid = %s
#         WHERE a.sid IS NULL
#             AND (c.quota > (SELECT COUNT(*) FROM apply ap WHERE ap.cid = c.cid) OR c.quota IS NULL)
#             AND (c.gpa_threshold <= (SELECT gpa FROM student s WHERE s.sid = %s) OR c.gpa_threshold IS NULL)
#         """
#         cursor.execute(query, (student_id, student_id))
#         applicable_companies = [result['cid'] for result in cursor.fetchall()]

#         if company_id not in applicable_companies:
#             error_message = f'Company ID {company_id} is not applicable for you.'
#         else:
#             insert_query = "INSERT INTO apply (sid, cid) VALUES (%s, %s)"
#             cursor.execute(insert_query, (student_id, company_id))
#             mysql.connection.commit()

#             success_message = 'Application submitted successfully!'
#             return redirect(url_for('tasks'))
#     student_id = session['userid']
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     query = """
#     SELECT c.cid, c.cname
#     FROM company c
#     LEFT JOIN apply a ON c.cid = a.cid AND a.sid = %s
#     WHERE a.sid IS NULL
#         AND (c.quota > (SELECT COUNT(*) FROM apply ap WHERE ap.cid = c.cid) OR c.quota IS NULL)
#         AND (c.gpa_threshold <= (SELECT gpa FROM student s WHERE s.sid = %s) OR c.gpa_threshold IS NULL)
#     """
#     cursor.execute(query, (student_id, student_id))
#     available_companies = cursor.fetchall()

#     return render_template('application_form.html', available_companies=available_companies, success_message=success_message, error_message=error_message)


# @app.route('/cancel_application/<cid>', methods=['GET'])
# def cancel_application(cid):
#     if 'loggedin' in session:
#         student_id = session['userid']
        
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('DELETE FROM apply WHERE sid = %s AND cid = %s', (student_id, cid))
#         mysql.connection.commit()
        
#         if cursor.rowcount > 0:
#             return redirect(url_for('tasks', success_message='Application canceled successfully'))
#         else:
#             return redirect(url_for('tasks', error_message='Failed to cancel the application'))

#     return redirect(url_for('login'))

# @app.route('/application_summary', methods=['GET'])
# def application_summary():
#     if 'loggedin' in session:

#         student_id = session['userid']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT c.cid, c.cname, c.quota, c.gpa_threshold FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s ORDER BY c.quota DESC', (student_id,))
#         desc = cursor.fetchall()

#         cursor.execute('SELECT MAX(c.gpa_threshold) AS max_gpa_threshold, MIN(c.gpa_threshold) AS min_gpa_threshold '
#                        'FROM company c JOIN apply a ON c.cid = a.cid WHERE a.sid = %s', (student_id,))
#         gpa_thresholds = cursor.fetchone()

#         cursor.execute('SELECT c.cid, c.cname '
#                        'FROM company c JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s AND c.gpa_threshold = %s', (student_id, gpa_thresholds['max_gpa_threshold']))
#         max_threshold_company = cursor.fetchone()

#         cursor.execute('SELECT c.cid, c.cname '
#                        'FROM company c JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s AND c.gpa_threshold = %s', (student_id, gpa_thresholds['min_gpa_threshold']))
#         min_threshold_company = cursor.fetchone()

#         cursor.execute('SELECT c.city, COUNT(c.cid) AS application_count '
#                        'FROM company c JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s GROUP BY c.city', (student_id,))
#         city_count = cursor.fetchall()

#         cursor.execute('SELECT c.cname FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s ORDER BY c.quota DESC LIMIT 1', (student_id,))
#         company_with_max_quota = cursor.fetchone()

#         # Fetch the company with the minimum quota
#         cursor.execute('SELECT c.cname FROM company c '
#                        'JOIN apply a ON c.cid = a.cid '
#                        'WHERE a.sid = %s ORDER BY c.quota ASC LIMIT 1', (student_id,))
#         company_with_min_quota = cursor.fetchone()
        
#         return render_template('application_summary.html',
#                                desc=desc,
#                                gpa_thresholds=gpa_thresholds,
#                                max_threshold_company=max_threshold_company,
#                                min_threshold_company=min_threshold_company,
#                                city_count=city_count,
#                                company_with_max_quota=company_with_max_quota,
#                                company_with_min_quota=company_with_min_quota)
#     return redirect(url_for('login'))


# @app.route('/logout')
# def logout():
#     if 'loggedin' in session:
#         session.pop('loggedin', None)
#         session.pop('userid', None)
#         session.pop('username', None)
#         session.pop('email', None)
#     return redirect(url_for('login'))
# @app.route('/analysis', methods =['GET', 'POST'])


# def analysis():
#     return "Analysis page"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
