This is a blog engine built using the Django framework.

You will need to a couple of things to get the blog up and running on your machine:

You will need to create a new database file and tell Django the path to that file is the settings.py file in the CMS folder.  You can create a new empty sqlite database in your terminal, save it (you can just save it in the same cms folder as settings.py), and type the absolute file path under the 'NAME' attribute for DATABASES in settings.py.  Then run "python manage.py syncdb" in your cms folder and Django will create the appropriate tables in your database.  You will also be prompted to add a new admin user/password combination when you set up the new database.

You will also need to change the template directories to your machine's path because it is absolute.  This is done in the settings.py file in the TEMPLATE_DIRS section.  Just add the path to where you installed the Django_Blog.

Lastly, you will likely need to add the path to your system's Python path so it can access the tagging module.  This can be done in terminal by running "export PYTHONPATH=$PYTHONPATH:/(path to Django_Blog).

