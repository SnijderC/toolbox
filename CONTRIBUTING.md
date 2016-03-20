Contributing to the Toolbox
===========================

So you know something about Git and Python (and maybe even Django) and you want to help? AWESOME! Please read on...

Quickly get started with Vagrant
--------------------------------

Vagrant allow you to control a virtual machine from a script. This project includes a Vagrant file, which describes how the virtual machine should be configures in order to run a basic test environment.

If you already have [Vagrant](https://www.vagrantup.com/) installed, you can skip the first 2 steps.

1. Install [Vagrant](https://www.vagrantup.com/)
2. Install [Virtualbox](https://www.virtualbox.org/)
3. Clone the project into a local directory.
   
    ```console
    $ git clone git@code.bof.nl/bitsoffreedom/toolbox.git
    ```

4. Install the `hostmanager` for vagrant, this allow us map `toolbox.local` to the IP address of the virtual host. Also install the `vagrant-vbguest` plugin for, which installs the *VirtualBox Guest Additions* to the virtual machine (required for mounting the local source code directory on the virtual host).
    ```console
    $ vagrant plugin install hostmanager
    $ vagrant plugin install vagrant-vbguest
    ```

5. Run `vagrant up` to start the virtual machine, it will automatically be configured, after configuration it will host a test environment at `toolbox.local` (`192.168.33.101`). The project directory will be mounted at the `/toolbox` in the virtual machine automatically as well. So any changes you make in the project directory should be reflected by the virtual machine. 

__Note:__ Running `vagrant up` will cause the hostmanager to try to change your *hosts* file, which requires your admin password.

Continous Integration
---------------------

All code pushed to the *develop* and *master* branches will be automatically build and tested by our GitLab runners. The build from *develop* will end up on https://toolbox-dev.bof.nl, the build from *master* on https://toolbox.bof.nl (the production site). That's another reason why the *master* branch is protected. The build script can be found in .gitlab-ci.yml. GitLab CI has excellent official documentation available [here](http://doc.gitlab.com/ce/ci/).

It is also possible to use a GitLab runner on your own computer and let it build the branch you are working on whenever you push new code. The installation manual can be found [here](https://gitlab.com/gitlab-org/gitlab-ci-multi-runner/#installation).

Git workflow
------------

The *master* branch is considered stable. The code in the *develop* branch is obviously not. Developers working on a specific feature should create and use a feature branch (called *feature/X*, where X is a name for the feature) and merge this branch into the *develop* branch when their work is done. This is where the testing begins. If the automated build succeeds and the [development website](https://toolbox-dev.bof.nl) functions normally, a release branch (*release/v2.X.0*) is created to 'freeze' the code in the *develop* branch. The code is tested some more and maybe someone finds and patches one or more bugs. Those bugfixes from the release branch may be merged back into *develop*. When the code is stable enough, it will be merged into master, build by the 'toolbox.bof.nl' runner and automatically deployed to the production site. A new release is tagged.

Hotfixes after a release are in the *hotfixes* branch and may be merged directly into master and develop. A hotfix after a release is always tagged as a point release.

Style guide
-----------

1. Use 4 spaces for indentation, not 3 or 5: 4, no tabs.
2. Please align your equal signs if you have a list of variables to assign..
   
   **BAD**:
   
        x = 1
        index = true
       
   ***GOOD***:
   
        x     = 1
        index = true

3. Please follow MVC with separate Templates.
4. Try to limit yourself to a width of 80 characters when possible.

**TL;DR:** Use the .editorconfig

Technologies used
-----------------

### Backend
 - Python
 - Django
 - A Django compatible database (preferably MySQL for it's more advanced search options (to be implemented)).
 - Jade (to generate HTML, please use it..)
 - Jinja (actually not primarily used but the Jade interpretor is based on it and there are a few advanced features here and there that do use it).
 - Various plugins for Django, see requirements.txt and the installation instructions.
 
### Frontend

 - HTML obviously.. (generated from Jade)
 - CSS3 (written in Less)
 - Javascript but really I mean: jQuery
 - Bootstrap 3
 
### Building from source

All CSS and HTML are generated from LESS and Jade. This allows for more semantic writing as well as making smaller more compressed payloads and fewer HTTP(S) requests. This also gives a better mobile experience which is a major advantage.

There are various ways to *preprocess* or *compile* these "languages" but the following strategy was chosen:

- Jade is preprocessed by a Django/Python plugin, don't worry about it. The compiled files are **not** cached, either use NGINX/Apache caching or implement caching in Django (everything is highly cacheable, nothing is very dynamic). Depending on the configuration of Django, the compiled *templates* may be cached for speed.
- Bower is used to download dependencies for modifying the source. You may want to run `bower install` to automatically download them, they will show up in the `vendors` directory.
- Grunt is used to compile LESS files and combine the necessary Javascripts and compress everything into a single CSS and a single JS file. The Gruntfile.js is already set to go, workflows as follows:
 - Run `npm install -g grunt-cli` to install Grunt globally on your computer.
 - `npm install` to install all Grunt's dependencies in `package.json`.
 - `grunt server`
    Runs a server that monitors changes in LESS and/or JS files in the source directories and compiles them on the fly in mere seconds. It does **not** compress files.
 - `grunt build` compiles the files and compresses them i.e.: concat/compile (JS/LESS resp.), uglify, YUI compress and then tells you the compression ratio.
 - Coffeescript is possible but **not** configured.
 
 - Only Bootstrap components that are required are included. Variables are overwritten but the Bootstrap source is not to be modified, you *can* overwrite functionality in the `index.less` file or if you want to create something a bit bigger and specific make a new `*.less` file and include it from the `index.less` file, it will be included in the `grunt server` after you restart Grunt.
 - Provides a live reload server, use a script or plugin for your browser to live-reload when you save a source file.

You may want to use the test server built-in into Django:

    python manage.py runserver 0.0.0.0:8080 --insecure
