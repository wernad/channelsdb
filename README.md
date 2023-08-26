# ChannelsDB 2

The project consinsts of three parts: Python API (`/api`), main page (`/frontpage`) and the results page (`/results`).

## Running

To run the ChannelsDB 2, use the following commands:

```bash
$ docker-compose build
$ docker-compose up
```

By default, the application runs on port `80` and uses `/data` as the data directory. To change this behaviour,
set the following environment variables before running `docker-compose up`. For example:

```bash
export CHANNELSDB_PORT=8080
export CHANNELSDB_DATA=/home/channelsdb/data
```
