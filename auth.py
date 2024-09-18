import pyrebase

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

email = 'test@gmail.com'
password = '123456'

# Create test User
# user = auth.create_user_with_email_and_password(email, password)
# print(user)

#Sign In
user = auth.sign_in_with_email_and_password(email, password)

#Get Account Info of signed in account
info = auth.get_account_info(user["idToken"])
print(info)

user_info = info['users'][0]  # Grab the first user info from the list
user_id = user_info['localId']
email = user_info['email']
email_verified = user_info['emailVerified']
creation_time = user_info['createdAt']

print(user_id)

#email Verification
# auth.send_email_verification(user["idToken"])

#Send Password Reset
# auth.send_password_reset_email(email)