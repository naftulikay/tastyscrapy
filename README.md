# tastyscrapy

A Scrapy project to scrape all public and private bookmarks in a Delicious account into a local SQLite database.

## Development Workflow

This project uses [Vagrant][vagrant], [Buildout][buildout], and [virtualenv][virtualenv] to provide an
<em><strong>ULTRAGLORIOUS</em></strong> development lifecycle.

To provide operating system isolation, Vagrant is used.

### Vagrant

The following commands bring up the Vagrant virtual machine
and then shell into it:

```
vagrant up
vagrant ssh
```

All commands from here are to be executed from within the Vagrant VM. Now change directories into `/vagrant`, where
all project files live:

```
cd /vagrant
```

### virtualenv

Next, to provide Python package isolation, we use [virtualenv][virtualenv], as documented
[in the Buildout docs][buildout-virtualenv]:

```
virtualenv -p python3.4 .
source bin/activate
```

The first line initializes the Python virtual environment with the system Python 3.4, and the second _activates_ it in
the current shell.

### Buildout

We now execute Buildout's bootstrap script to set everything up for Buildout:

```
python3 bootstrap.py
```

Finally, now that everything has been set up properly, we can now execute Buildout to download and compile dependencies:

```
bin/buildout
```

The entire above workflow only needs to be executed once on project clone. After changing package versions,
`bin/buildout` will need to be run again, but nothing else.

After this is complete, there should be a number of scripts in the `bin` directory, including but not limited to:

 - `bin/test`: Executes all unit tests.
 - `bin/python`: Starts the Python interpreter.
 - `bin/ipython`: Starts the IPython advanced Python interpreter for poking around.
 - `bin/scrapy`: Invokes the Scrapy start script.


 [vagrant]: https://vagrantup.com
 [buildout]: https://pypi.python.org/pypi/zc.buildout/2.5.3
 [buildout-virtualenv]: http://www.buildout.org/en/latest/install.html
 [virtualenv]: https://virtualenv.pypa.io/en/stable/
