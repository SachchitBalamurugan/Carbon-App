from flask import Flask, render_template, session, request, redirect
import pyrebase

app = Flask(__name__)


config = {
    "apiKey": "AIzaSyBT1NH-JfDLGx-UwhX3_JiEx_s1uNNtl-8",
    "authDomain": "carbonapp-4f198.firebaseapp.com",
    "projectId": "carbonapp-4f198",
    "storageBucket": "carbonapp-4f198.appspot.com",
    "messagingSenderId": "581642423590",
    "appId": "1:581642423590:web:2ab9ab765a4567f04d85e7",
    "measurementId": "G-M0FJFDT20X",
    "databaseURL": "https://carbonapp-4f198-default-rtdb.firebaseio.com"  # Replace with your actual database URL
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = "secert" #change later

@app.route('/', methods=['GET', 'POST'])
def complete_profile():
    if('user' in session):
        return redirect('/dashboard')  
        # return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            session['user_id'] = user['localId']  # Store the user ID in the session
            session['id_token'] = user['idToken']  # Optionally store the idToken if needed

        except:
            return "Login failed. Check your email and password."

    return render_template('complete_profile.html')


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    
    email = session['user']
    user_id = session.get('user_id')  # Retrieve the user ID from the session
    
    username = email.split('@')[0]  # Strip off anything after '@'
    
    return render_template('dashboard.html', username=username, user_id = user_id)


#CHECK THIS
# @app.route('/dashboard')
# def dashboard():
#     if 'user' not in session:
#         return redirect('/')

#     email = session['user']
#     username = email.split('@')[0]  # Strip off anything after '@'

#     try:
#         id_token = session.get('id_token')
#         if not id_token:
#             return "ID token not found."

#         # Fetch user info using ID token
#         user_info = auth.get_account_info(id_token)
#         user_id = user_info['users'][0]['localId']
#     except Exception as e:
#         return f"Failed to fetch user ID. Error: {str(e)}"

#     return render_template('dashboard.html', username=username, user_id=user_id)

# @app.route('/dashboard')
# def dashboard():
#     if 'user' not in session:
#         return redirect('/')

#     email = session['user']
#     username = email.split('@')[0]  # Strip off anything after '@'

#     # Fetch user ID from Firebase Auth
#     user = auth.get_account_info(auth.get_account_info_by_email(email)['users'][0]['localId'])
#     user_id = user['users'][0]['localId']

#     return render_template('dashboard.html', username=username, user_id=user_id)


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    
        

    password = request.form.get('password')
    
    try:
        # Create a new user with email and password
        user = auth.create_user_with_email_and_password(email, password)
        
        # Automatically log in the user after registration
        session['user'] = email
        session['user_id'] = user['localId']  # Store the user ID in the session
        session['id_token'] = user['idToken']  # Optionally store the idToken if needed
        return redirect('/dashboard')
    except Exception as e:
        return f"Registration failed. Please try again. Error: {str(e)}"


@app.route('/signup')
def signup():
    return render_template('signup.html')  # Ensure you have a signup.html template


@app.route('/statistics')
def stats():
    return render_template('stats.html')



if __name__ == '__main__':
    app.run(debug=True)

