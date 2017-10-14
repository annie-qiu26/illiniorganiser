from flask import Flask
from flask import render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bagels'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField("Username", validators = [Required()])
    password = StringField("Password", validators = [Required()])
    login = SubmitField("Login")
@app.route('/', methods = ['GET','POST'])
def index():
    name=None
    password = None
    form = NameForm()
    if form.validate_on_submit():
        name=form.name.data
        password=form.password.data
    return render_template('index.html',form=form,name=name,password=password)

if __name__ == "__main__":
    manager.run()
