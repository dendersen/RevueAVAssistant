cd ..
docker rm rava
docker run -dit -m 4g --name rava rava-docker
docker attach rava