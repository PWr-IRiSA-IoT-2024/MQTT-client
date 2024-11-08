# MQTT Client

## Description

An MQTT client that connects to The Things Stack application server to receive uplink messages from registered applications. Designed to be run in a Docker container.

## Installation

### Setup

> [!TIP]
> Consult [this page](https://www.thethingsindustries.com/docs/integrations/mqtt/#creating-an-api-key) for help with getting the required variables.

Create an `.env` file from provided `.env.example`. All environmental variables must be filled in before running the container.

```
APP_ID=your-app-id              # The Things Stack application ID
TENANT_ID=your-tenant-id        # The Things Stack username
MQTT_HOST=your-mqtt-host        # MQTT broker hostname
MQTT_PORT=1883                  # Port to connect to MQTT broker (default: 1883)
ACCESS_KEY=your-access-key      # Access key for The Things Stack
```

### Requirements

- Docker 26+

### Startup

```
docker-compose up --build
```

## Libraries

- [`paho-mqtt`](https://pypi.org/project/paho-mqtt/)