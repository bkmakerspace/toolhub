Toolhub
=======

[![CodeFactor](https://www.codefactor.io/repository/github/bkmakerspace/toolhub/badge)](https://www.codefactor.io/repository/github/bkmakerspace/toolhub) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Build Status](https://travis-ci.com/bkmakerspace/toolhub.svg?branch=master)](https://travis-ci.com/bkmakerspace/toolhub)

A service for tool awareness and organization.

Setting up the project
----------------------

Developing on unix based systems is only supported at this moment.

Run the setup script and follow the instructions.

1. Clone this repository
2. Copy `.dockerenv-dist` to `.dockerenv` and populate uncommented variables with real values,
do not commit this file.
3. If available, download a copy of the a recent database dump and copy to `./docker/init/db/`
5. Run `./scripts/setup` and follow the instructions in any dialogs
6. Run `./scripts/start`

You can now find the server running at `http://localhost:8000`.

Press `ctlr+c` to stop the docker containers.

See `./scripts/README.md` for details on other work-flow scripts.

Exposing Ports
--------------

By default database ports are exposed on the host machine dynamically. You can easily see
what ports each is forwarded to using `docker-compose ps` and see the details in the "Ports"
column.

If you would like to choose the ports a service uses, you can set the `<service>_PORT`
environment variables in your shell's environment in a `.env` file.
