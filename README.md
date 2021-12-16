# simple-django-website
This is a django web project I did in 2019 to get to know/learn django\
It is a very simple social media site which allows you to:
 - create an account(email confirmation using PasswordResetTokenGenerator)
 - write posts
 - read others' posts
 - comment on your/others' posts
 
UI is minimal, it doesn't have any css-styling and pages are not responsive

## Installation/usage
install Django v3.2 `pip install django==3.2`\
clone rep `git clone https://github.com/samutoljamo/simple-django-website.git && cd simple-django-website`\
run the development server `python manage.py runserver`\
Go to `http://127.0.0.1:8000/` on a browser\
Email confirmation is disabled by default in `settings.py` since it needs an email account it can use

