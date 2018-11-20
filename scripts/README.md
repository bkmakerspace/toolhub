Developer Workflow Scripts
===========================================

The scripts in this directory are intended to improve developer workflow when working with the
Docker toolchain. All scripts contain a help message outlining the purpose and usage of each
script, which can be accessed using the `--help` flag. The Docker ecosystem is vast and can be
quite complex, and these scripts are intended to get you kickstarted, but you likely will need to
use the `docker` and `docker-compose` commands directly at some point in the near future. The
[Docker docs](https://docs.docker.com/reference/) are your friend.


setup
-----

This is the script intended to prepare your system by installing the Docker toolchain and building
the images and restoring a fresh database for the project. Due to the installation process for Mac,
you should run `setup_docker` first.

setup_docker
------------

This script will install Docker and docker-compose. On Linux systems this is called as part of the
`setup` script and does not need to be run separately. For Mac, this script should be run before
running `setup`.

start
-----

This script should be used to launch the services to run the project. The output of the command for
each service will be output together in the resulting screen. Pressing `ctrl-c` will cause all the
services here to be stopped.

You may, optionally, provide service names to only launch specific services.

If you provide the `-d` flag to detach from the services and run them in the background and you'll
be returned to your shell. You can use the `attach` script to connect to all or specific services
at any time. You will need to use the `stop` script to stop services that are detached.

stop
----

This script will stop all or specfic services, whether they are detached or attached in another
terminal.

update
------

This script is intended to be run when pulling down a large changeset, i.e. pulling a new branch or
latest master. It will rebuild your images and containers, installing new requirements, and run
migrations.

install
-------

This is intended to abstract away a large number of complexities when working with the project. You
should specify whether you installing a Python or System (apt) package and this script will
take the appropriate steps to make sure the package is installed and added to the correct
requirements file (pyproject.toml or package.json). You can provide the `--dev` and `--no-save`
flags to modify this functionality as needed.

migrate
-------

Use this script to abstract some complexities in managing migrations within Docker. When run
directly, the `run` command is assumed and migrations will be run, but you can also use the `make`
and `show` commands to create and list migrations. Most options for equivalent Django commands
should translate directly, when provided after the command.

test
----

This will run the appropriate unittesting suite. While it currently only supports Python/Django
tests, it is intended that in the future javascript tests will be decoupled from the build process
allowing this to manage those as well.

coverage
----

This will run the appropriate Django/Python unittesting suite, generating a test
coverage report. The report can be viewed by opening `htmlcov\index.html` in a
browser

console
-------

This will allow you to connect to the services via the appropriate interactive console. Currently
supported are `bash` to use bash on the primary web service, `sudo` to use bash as sudo, `python`
to use Django's shell_plus command, and `mysql` to get a MySQL console.

attach
------

This can be used to attach to a specific service's output console. Whether it's running in detached
mode or you simply want to see that services output by itself in a separate terminal.

restore_db
----------

This will destroy any existing database container you have running and restore it using restore
files located in `docker/init/db`. The restore files **must** exist for this script to run.

All migrations in your current checkout of the codebase will be run at the end of the restore
unless using the `--no-migrate` flag.

cleanup
-------

This can be used to cleanup a working environment. It will delete any cache files (.pyc) and drop
the static build and Redis cache volumes, in an attempt to remove anything that may be causing odd
behavior. It's generally better to just run `update` which includes this script, but this can
sometimes be a quick fix for weirdness.

Docker also will also create new images and volumes relatively often. Generally you want to keep
these around for a little so that rebuilding between branches is quicker due to Docker using this
cache. However, this takes up a large amount of space on your system and it's recommended to
occasionally run `cleanup --docker` to also remove any Docker artifacts that are no longer used,
freeing up space on your system

teardown
--------

This will utterly and completely destroy your Docker environment, including all build files and
database volumes. There should never be any side affects outside of that environment, which can be
rebuilt using `setup`, but you will be waiting a while for it to rebuild.

tools
-----

This contains several utility functions which are used in most of the other scripts. Nothing of
practical use otherwise.

run_util
--------

This script will allow you to run certain, short lived, utilities that are not strictly needed for
running or developing the application, but can sometimes come in handy. See the help text of this
command to see all available utilities.

### pgadmin

pgAdmin4 is a web-based tool for monitoring and managing Postgres databases. You will need to
configure a server connection the first time you run it (and anytime it's volume gets deleted). Use
the network alias and default Postgres username and password found in the docker-compose file for
the db service.

### pgdump

This will dump the contents of the database to a file. By default it only dumps the `toolhub`
database to a gzipped file.
