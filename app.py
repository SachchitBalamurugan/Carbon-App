from flask import Flask, render_template, session, request, redirect, jsonify
import pyrebase
import google.generativeai as genai

app = Flask(__name__)

def get_activities_data(user_id):
    db = firebase.database()
    activities_ref = db.child("users").child(user_id).child("activities")
    activities = activities_ref.get()
    
    activity_list = []
    for activity in activities.each():
        data = activity.val()
        activity_list.append(data)
    
    return activity_list


def get_ai_response(prompt):
    api_key = "AIzaSyDKkSMAEHiDUgYx3gwyLbbmhsQaflxSGrI"
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(prompt)
    return response.text

@app.route('/get_ai_advice', methods=['POST'])
def get_ai_advice():
    if 'user' not in session:
        return jsonify({'response': 'User not logged in.'}), 401

    data = request.get_json()
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({'response': 'No input provided.'}), 400

    try:
        ai_response = get_ai_response(user_input)
        return jsonify({'response': ai_response})
    except Exception as e:
        return jsonify({'response': f"Error occurred: {str(e)}"}), 500

@app.route('/get_user_activities', methods=['GET'])
def get_user_activities():
    if 'user' not in session:
        return jsonify({'response': 'User not logged in.'}), 401

    user_id = session.get('user_id')  # Get the user ID from the session

    try:
        # Fetch activities data for the user
        activities = get_activities_data(user_id)

        if not activities:
            return jsonify({'activities': []})  # Return empty list if no activities found

        return jsonify({'activities': activities})

    except Exception as e:
        return jsonify({'response': f"Error occurred while fetching activities: {str(e)}"}), 500

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
    user_id = session.get('user_id')  # Retrieve the user ID from the session
    
    return render_template('stats.html', user_id = user_id)



if __name__ == '__main__':
    app.run(debug=True)

