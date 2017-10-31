# illiniorganizer

Recommended IDE: [PyCharm](https://www.jetbrains.com/pycharm/) by JetBrains. 
Go to [this link](https://www.jetbrains.com/student/) and sign up with your illinois.edu email address to get the professional version for free. 

Framework: [Django](https://www.djangoproject.com)
Go to [this link](https://docs.djangoproject.com/en/1.11/topics/install/) for steps on how to install Django. Try and go through [this guide](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) to understand how Django works. 

Frontend: [Bootstrap](https://getbootstrap.com/docs/3.3/components/#navbar) and [Semantic-UI](https://semantic-ui.com/elements/button.html). 
DO NOT REINVENT THE WHEEL. These two are pretty popular front-end libraries and relatively easy to implement. They have every component we could possibly need. You do not need to install or download either of the libraries. I have included the [cdn](https://www.webopedia.com/TERM/C/CDN.html) links to both these libraries in the `base.html` file under the templates directory. 

Running Django:
Once you have installed Django and cloned the repo, run the following commands in your terminal:
1. `python manage.py makemigrations`
2. `python manage.py migrate`
3. `python manage.py createsuperuser`. At this point it will prompt you to enter your desired username, email and password. The email field is not required; you can leave it blank and press enter. When you're typing in your password in the terminal the characters will NOT appear so keep typing and press enter. 
4. `python manage.py runserver`. 
5. Open a web browser and go to [this link](http://127.0.0.1:8000/app/#) to open the web app. 
6. Go to [this link](http://127.0.0.1:8000/admin/) to go to the admin site and log in with the username and password you created earlier. 
