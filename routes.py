from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from models import db, User
from forms import SignupForm, SigninForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = 'development-key'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/home')
def home():
  if 'email' not in session:
    return redirect(url_for('signin'))
  else:
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      session['email'] = newuser.email

      return redirect(url_for('home'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      email = form.email.data
      password = form.password.data

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = email
        return redirect(url_for('home'))
      else:
        message='Incorrect credentials'
        return render_template('signin.html', form=form, incorrect_credentials=message)

  elif request.method == 'GET':
    if 'email' in session:
      return redirect(url_for('home'))
    else:
      return render_template('signin.html', form=form)

@app.route('/signout', methods=['GET', 'POST'])
def signout():
  session.pop('email', None)
  return redirect(url_for('index'))


@app.route('/api/test', methods=['GET'])
def test():
  return jsonify({'tasks': {'lol': 'my bad'}})


if __name__ == '__main__':
  app.run(debug=True)
