from flask import Blueprint, render_template, request, current_app

registerL_bp = Blueprint('registerL', __name__)

@registerL_bp.route('/registerL', methods=['GET', 'POST'])
def registerL():
    message = ''
    mysql = current_app.config.get('mysql', None)
    if request.method == 'POST' and 'full_name' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'nationality' in request.form and 'bdate' in request.form and 'learning_style' in request.form and 'learning_objective' in request.form:
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nationality = request.form['nationality']
        bdate = request.form['bdate']
        learning_style = request.form['learning_style']
        learning_objective = request.form['learning_objective']

        # Check if the username is unique
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM User WHERE U_id = %s', (username,))
        account = cursor.fetchone()
        if account:
            message = 'Username already exists. Please choose a different username.'
        else:
            # Insert into User table with U_id equal to username
            cursor.execute(
                'INSERT INTO user (U_id, full_name, email, password, nationality, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)',
                (username, full_name, email, password, nationality, bdate)
            )
            mysql.connection.commit()

            # Insert into Learner table
            cursor.execute(
                'INSERT INTO learner (U_id, learning_style, learning_objective) VALUES (%s, %s, %s)',
                (username, learning_style, learning_objective)
            )
            mysql.connection.commit()

            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('registerL.html', message=message)
