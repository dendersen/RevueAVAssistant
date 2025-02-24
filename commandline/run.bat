cd ..
docker remove rava
docker run -dit -m 2g --name rava rava-docker
docker attach rava
pause