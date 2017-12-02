# illiniorganizer

Illini Organizer is a home for everything student-run at UIUC.

## Tools

**Recommended IDE**: [PyCharm](https://www.jetbrains.com/pycharm/) by JetBrains.
Go to [this link](https://www.jetbrains.com/student/) and sign up with your illinois.edu email address to get the professional version for free.

**Framework**: [Django](https://www.djangoproject.com) is a modern Python Web framework that makes web development cool.
Try and go through [this guide](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) to understand how Django works.

**Frontend**: [Bootstrap](https://getbootstrap.com/docs/3.3/components/#navbar) and [Semantic-UI](https://semantic-ui.com/elements/button.html). 
These two are pretty popular front-end libraries and relatively easy to implement. They have every component we could possibly need. You do not need to install or download either of the libraries. I have included the [cdn](https://www.webopedia.com/TERM/C/CDN.html) links to both these libraries in the `base.html` file under the templates directory.

## Setup

First, clone this repo and `cd` to your local copy in your terminal.

### Installing packages
Packages are all the third party Python modules we need to run our app, such as Django. Packaging tools exist to streamline the package installation process. [Pipenv](https://docs.pipenv.org) is the best Python packaging tool out there. Pip is required to install Pipenv; if you don't have it already, check out [this link](https://pip.pypa.io/en/stable/installing/) to set it up. Once you have Pip installed, run the following commands in your terminal:
1. `pip install pipenv` Installs pipenv itself
2. `pipenv install` Creates a virtual environment, installs the packages listed in Pipfile into the virtual environment

### Running Django
Once you have installed the packages with Pipenv, run these commands to get the server going:
1. `python manage.py makemigrations`
2. `python manage.py migrate`
3. `python manage.py createsuperuser`. At this point it will prompt you to enter your desired username, email and password. The email field is not required; you can leave it blank and press enter. When you're typing in your password in the terminal the characters will NOT appear so keep typing and press enter. 
4. `python manage.py runserver`. 
5. Open a web browser and go to [this link](http://127.0.0.1:8000/app/#) to open the web app.** 
6. Go to [this link](http://127.0.0.1:8000/admin/) to go to the admin site and log in with the username and password you created earlier. 

### Adding data
Nothing will appear on the webapp the first time you open it because there's no data. To get a feel for how the database works, follow the following steps to make an organization:
1. Go to [the admin page](http://127.0.0.1:8000/admin/). 
2. Click on RSO and create a new RSO. 
3. Reload the [web app](http://127.0.0.1:8000/app/#).
4. You can click on the name of the RSO which will send you to a "detail" page of the organization. (The link is working if a webpage with just the name of the RSO appears).

Creating all of the organizations and other data manually would take forever, so I wrote some scripts in `app/scripts/` to generate all of the initial data automatically. Check out their comments to understand how they work. To run a script, type `execfile('app/scripts/script_name.py')` into the Django console.
