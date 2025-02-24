cd ..
git pull
docker build --pull --rm -f "Dockerfile" -t rava-docker "."
pause