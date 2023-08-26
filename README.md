# ChannelsDB 2

The project consinsts of three parts: Python API (`/api`), main page (`/frontpage`) and the results page (`/results`).

## Running

Two setups are available, a local development version and a production version meant to be run in Openstack cloud. 

### Development

To run the development version of ChannelsDB 2, use the following commands:

```bash
$ docker-compose -f docker/docker-compose.devel.yaml build
$ docker-compose -f docker/docker-compose.devel.yaml up
```

By default, the application runs on port `80` and uses `/data` as the data directory. To change this behaviour,
set the following environment variables before running `docker-compose up`. For example:

```bash
export CHANNELSDB_PORT=8080
export CHANNELSDB_DATA=/home/channelsdb/data
```

### Production

The production version has to use `docker/docker-compose.production.yaml` file. No further setup is allowed.
