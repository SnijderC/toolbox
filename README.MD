===========
BOF Toolbox
===========

## Introduction
BOF Toolbox is a kind of index website of tools, services and advice for users that value their privacy and security.
It lists both safe options and well known unsafe options so users can quickly identify better alternatives that suits their existing workflow.

This is my first project using Python and Django. Feedback is always welcome..

## Dependencies

 - Python 2.7+
 - Python pip
 - MySQL 5.6+ *or* any other database supported by Django.\*
 - MySQL database development files

To install these dependencies in Debian/Ubuntu:
    ```
    sudo apt-get install python python-pip mysql-server-5.6 libmysqlclient-dev
    ```

\* *One thing that can be said about another database backend is that the search functionality will not work. You will need to implement a custom solution as this feature uses MySQL's.*

## Installation instructions

 1. Make a copy of the Git repo:
    ```
    git clone https://github.com/SnijderC/toolbox.git ./toolbox
    ```
    This should create a new directory called toolbox in the current directory.
    
 2. If you want create a virtual environment to isolate this app's dependencies (and you should) to not depend on system wide changes.

    If you have virtualenv, you can skip this:
    ```   
	pip install virtualenv
    ```
    Next:
 	```
    virtualenv toolbox
    cd toolbox/
    source ./bin/activate
	```
        
 3. Make appropriate changes to the `settings/production.py.sample` file, at a minimum supply a database backend, username and password.
    Then rename it to `settings/production.py`
    Note: *For a development setup you should use `development.py` instead. Settings in `development.py` overrule settings in `production.py`.*

    At a minimum find these lines and fill in your database settings:

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
    
    Fill in the database settings (host, username, password, etc.), then **uncomment the lines**. 
   
 4. Run the following to install the frameworks which consist mainly of Django, Django plugins and some utilities like 
    mysql-python. Then it will initialise the database with empty tables and ask you to make an administrator account for Django.
   
    ```
    pip install -r requirements.txt
    mkdir toolbox/logs
    python manage.py syncdb --noinput
    python migrate toolbox --noinput
    python collectstatic --noinput
    ```

And, if applicable, import fixtures (database dumps) into the database:
   
    ```
    python manage.py loaddata setup_db_content.json
    ```
   
    *If something fails, read the* ***Someone the toolbox*** *section..*
        
 5. Magic should happen and you may startup the test server by running:
   
    ```
    python manage.py runserver 0.0.0.0:8080 --insecure
    ```
   
    **NOTE the part where this says `--insecure`.** This is for testing only!
     
 6. Now browse to: 
      - http://server-ip-address:8080
      - http://server-ip-address:8080/admin
  
 7. You *should* setup **wsgi** in NGINX, Apache or lighthttpd for a production environment. Directories to map: 
      - toolbox/ (the application)
      - toolbox/static/ (static files: css, js, django & plugins)

### Someone the toolbox (troubleshooting)
Ok, so plans fail.. for documentation purposes this is a listing of what should have happened when you ran `setup.py install`.

    pip install -r requirements.txt --allow-external mysql-connector-python
    ./manage.py syncdb
    ./manage.py migrate toolbox
    ./manage.py collectstatic
    ./manage.py loaddata setup_db_content.json

Try running the commands one by one and see where – if any – errors occur.
    
## Structure

The entry point for this project is app.py.

There are currently 3 main content providing functions mapped below.
 
1. Static pages written in Jade or Markdown.

2. Dynamic pages based on the actual database content.

3. The Django admin pages.
 
The 5 entry points defined in app.py are:

1. The landing page: templates/landing.jade

2. The Django admin pages.

3. Static markdown files, these include e.g. credits and markdown documenatation
    pages: /templates/credit.md and /templates/markdown_doc.md respectively.

4. More static pages but more specifically licenses, obviously in the license dir.

5. Dynamic pages, the actual content of the website.
    There are 2 index templates and a content template for displaying that content.
    
    1. A multi-column index page that shows all the content types.
    2. A single-column layout that shows one type of content e.g. "tools".
    3. A content page that contains only a single content item; e.g. one tool: "TOR".
    
## Navigation

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
 
## Contributing

*Yes please..*

### "Style guide"

1. Use 4 spaces for indentation, not 3 or 5: 4, no tabs.
2. Please align your equal signs if you have a list of variables to assign..
   
   **BAD**:
   
        x = 1
        index = true
       
   ***GOOD***:
   
        x     = 1
        index = true

3. Please follow MVC with separate Templates.
4. Even though Python's documentation tells us to do so, there are some places where more than 80 chars wide code is used..
   It may not be convenient for the *vi(m)* user but who want to use *vi(m)* anyway..

**TL;DR:** Use the .editorconfig

### Technologies used

#### Backend
 - Python
 - Django
 - A Django compatible database (preferably MySQL for it's more advanced search options (to be implemented)).
 - Jade (to generate HTML, please use it..)
 - Jinja (actually not primarily used but the Jade interpretor is based on it and there are a few advanced features here and there that do use it).
 - Various plugins for Django, see requirements.txt and the installation instructions.
 
#### Frontend

 - HTML obviously.. (generated from Jade)
 - CSS3 (written in Less)
 - Javascript but really I mean: jQuery
 - Bootstrap 3
 
#### Building from source

All CSS and HTML are generated from LESS and Jade. This allows for more semantic writing as well as making smaller more compressed payloads and fewer HTTP(S) requests. This also gives a better mobile experience which is a major advantage.

There are various ways to *preprocess* or *compile* these "languages" but the following strategy was chosen:

- Jade is preprocessed by a Django/Python plugin, don't worry about it. The compiled files are **not** cached, either use NGINX/Apache caching or implement caching in Django (everything is highly cacheable, nothing is very dynamic).
- Bower is used to download dependencies for modifying the source. You may want to run `bower install` to automatically download them, they will show up in the `vendors` directory.
- Grunt is used to compile LESS files and combine the necessary Javascripts and compress everything into a single CSS and a single JS file. The Gruntfile.js is already set to go, workflows as follows:
 - `npm install` to install all Grunt's dependencies in `package.json`.
 - `grunt server`
 	Runs a server that monitors changes in LESS and/or JS files in the source directories and compiles them on the fly in mere seconds. It does **not** compress files.
 - `grunt build` compiles the files and compresses them i.e.: concat/compile (JS/LESS resp.), uglify, YUI compress and then tells you the compression ratio.
 - Coffeescript is possible but **not** configured.
 
 - Only Bootstrap components that are required are included. Variables are overwritten but the Bootstrap source is not to be modified, you *can* overwrite functionality in the `index.less` file or if you want to create something a bit bigger and specific make a new `*.less` file and include it from the `index.less` file, it will be included in the `grunt server` after you restart Grunt.
 - Provides a live reload server, use a script or plugin for your browser to live-reload when you save a source file.

For the python modules you can use the setup script that is detailed in the installation section. It's based on the `requirements.txt` file and runs the database migrations afterwards, which means that you should **first** setup a MySQL database and enter the details into the settings file.

You may want to use the test server built-in into Django:

    python manage.py runserver 0.0.0.0:8080
