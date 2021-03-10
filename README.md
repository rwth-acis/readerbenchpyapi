
<h1 align="center">readerbenchpyapi for German</h1>



[Source of the original Project](https://git.readerbench.com/ReaderBench/readerbenchpyapi)

Please follow the instructions of this ReadMe to setup your basic service development environment.  

## Docker Setup

Assuming that the docker is available on the machine, after cloning the project navigate to its folder and run:
    > docker-compose up

This will begin building the container, and it will take a while. There might appear some incompatibility issues
between libraries, but the project should work regardless.
After the installation is finished a python server should start. If this point is reached, we can exit the 
container by pressing CTRL+C and restart it as a daemon with:
    > docker-compose up -d

To stop the container use:
    > docker-compose down


## API endpoints

The server runs on the 6006 port. In order to see the list of available endpoints the "rb_api_server.py" file can
be inspected.

