from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def complete_profile():
    return render_template('complete_profile.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/statistics')
def stats():
    return render_template('stats.html')

if __name__ == '__main__':
    app.run(debug=True)
