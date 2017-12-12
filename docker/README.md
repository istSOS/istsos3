# istSOS3 with docker

## Build docker image

Open a terminal and run this command to pull the image

`docker pull mdillon/postgis`

To create and start the container:

`docker run --name istsos-postgres -e POSTGRES_PASSWORD=postgres -d mdillon/postgis`

To start after the first run:

`docker start istsos-postgres`

To stop:

`docker stop istsos-postgres`

Inspect:

`docker inspect istsos-postgres`

List running:

`docker ps`


## Run docker as a non-root user:

sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
