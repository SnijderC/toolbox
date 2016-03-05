BOF Toolbox
===========

Introduction
------------
BOF Toolbox is a kind of index website of tools, services and advice for users that value their privacy and security.
It lists both safe options and well known unsafe options so users can quickly identify better alternatives that suits their existing workflow.

This is my first project using Python and Django. Feedback is always welcome..

Original author: Chris Snijder (https://github.com/SnijderC). See toolbox/templates/credits.md for a list of all contributors to the Toolbox and it's contents. This repository is maintained by Bits of Freedom (https://bof.nl). The Toolbox website can be found here: https://toolbox.bof.nl.

Dependencies
------------
 - Python 2.7+
 - Python header files and static library
 - Python pip
 - MySQL 5.6+ *or* any other database supported by Django.\*
 - MySQL database development files
 - JPEG runtime library

To install these dependencies in Debian/Ubuntu:

    sudo apt-get install python python-dev python-pip mysql-server-5.6 libmysqlclient-dev libjpeg-dev

\* *One thing that can be said about another database backend is that the search functionality will not work. You will need to implement a custom solution as this feature uses MySQL's.*

Installation instructions
-------------------------
 1. Make a copy of the Git repo:
    ```
    git clone https://code.bof.nl/bitsoffreedom/toolbox.git
    ```
    This should create a new directory called toolbox in the current directory.
    
 2. If you want create a virtual environment to isolate this app's dependencies (and you should) to not depend on system wide changes.

    If you have virtualenv, you can skip this:
    ```
	pip install virtualenv
    ```
    Next:
 	```
    virtualenv toolboxenv
    source ./toolboxenv/bin/activate
	```

 3. Copy the `settings/production.py.sample` file to `settings/production.py`, at a minimum supply a database host, name, username and password.
    Note: *For a development setup you should use `development.py` instead. Settings in `development.py` overrule settings in `production.py`.*

    Find these lines and fill in your database settings:

    ~~~
    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE'    : 'django.db.backends.mysql',
            'NAME'      : 'toolbox-prod',
            'HOST'      : 'localhost',
            'USER'      : 'toolbox-prod',
            'PASSWORD'  : 'banaan01'
        }
    } 
    ~~~

 4. Run the following to install the frameworks which consist mainly of Django, Django plugins and some utilities like 
    mysql-python. Then it will initialise the database with empty tables.
    ```
    pip install -r requirements.txt
    mkdir toolbox/logs
    python manage.py syncdb --noinput
    python manage.py migrate toolbox --noinput
    python manage.py collectstatic --noinput
    ```

    *If something fails, read the* ***Someone the toolbox*** *section..*

    Run this to create a superuser (admin) and set a password for said superuser:
    ```
    python manage.py createsuperuser
    ```

 5. Magic should happen and you may startup the test server by running:

    ```
    python manage.py runserver 0.0.0.0:8080 --insecure
    ```

    **NOTE the part where this says `--insecure`.** This is for testing only!

 6. Now browse to: 
      - http://server-ip-address:8080
      - http://server-ip-address:8080/admin
  
 7. You *should* setup **wsgi** in NGINX, Apache or lighthttpd for a production environment. Do not forget this alias:
      - /static should point to the toolbox/static/ directory (for all static files)
    Bits of Freedom uses nginx and uWSGI. uWSGI requires a plugin to work with Python. This plugin can be installed with one command on Debian/Ubuntu:
    ```
    sudo apt-get install uwsgi-plugin-python
    ```
    The configuration used by Bits of Freedom is available in the "examples" directory. The nginx example configuration does not have SSL configured, because all SSL connections are terminated at a forward proxy in Bits of Freedom's setup. If you don't use a forward proxy you *should* configure SSL.

### Someone the toolbox (troubleshooting)
Ok, so plans fail.. Most problems arise from missing dependencies. Try to install them with this command:

    pip install -r requirements.txt --allow-external mysql-connector-python

Also, make sure you are working inside your virtual environment.
Feel free to ask Bits of Freedom's system administrator for help: imre.jonk@bof.nl

Upgrade instructions
--------------------
**`Always make a backup before you attempt to upgrade!`**

Commands to execute inside the virtualenv:

    git pull
    pip install --upgrade -r requirements.txt
    python manage.py syncdb --noinput
    python manage.py migrate toolbox --noinput
    python manage.py collectstatic --noinput

Structure
---------
The entry point for this project is app.py.

There are currently 3 main content providing functions mapped below.
 
1. Static pages written in Jade or Markdown.

2. Dynamic pages based on the actual database content.

3. The Django admin pages.
 
The 5 entry points defined in app.py are:

1. The landing page: templates/landing.jade

2. The Django admin pages.

3. Static markdown files, these include e.g. credits and markdown documentation pages: /templates/credit.md and /templates/markdown_doc.md respectively.

4. More static pages but more specifically licenses, obviously in the license dir.

5. Dynamic pages, the actual content of the website. There are 2 index templates and a content template for displaying that content.

    1. A multi-column index page that shows all the content types.
    2. A single-column layout that shows one type of content e.g. "tools".
    3. A content page that contains only a single content item; e.g. one tool: "TOR".

Navigation
----------
The "*slugs*" – which is a loosely defined term, can be found in the settings files. There is an array that defines whether a "*slug*" can come only with or also without an argument, e.g. `/tools/` is defined as *single* but *can* actually also have an argument: `/tools/tor/`. It also defines wether it may occur more than once in the case of: `/categorie/e-mail/categorie/encryptie`; `multiple` is set to `true`. Finally the array specifies a name that corresponds to the database table in English. This way non-Dutch speakers can re-use/contribute to the code, plus in the future it can be made multi-lingual without renaming all the database tables. 

Currently these are the "*slugs*" that may be "*single*":

 - adviezen (advise)
 - tools
 - diensten (services)
 
Additionally "*single*" slugs can only occur once, if they occur twice the last one is taken into consideration, the previous ones are ignored.
In other words: `/adviezen/tools/` would lead to the tools section, not the advice section.

These slugs can be of type multiple and can be considered to be "filters":
 - categorie

Thus these can occur multiple times: 

`/categorie/e-mail/categorie/encryptie/categorie/privacy/`

These are accumulated (**AND**) so this would filter out all the tools that help you with encryption **and** privacy for your e-mail use.

Then there are some slugs that are also filters but for ux simplicity it was decided these should only allow for one selection: 

 - formfactor
 - platform

Lastly there are 2 mute slugs that are for future use:
 - licenties (licenses)
 - prijs (price)
 
Contributing
------------
*Yes please...* See CONTRIBUTING.md
