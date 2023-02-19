FROM python:3.8-slim-buster

RUN useradd app
RUN apt-get update && apt-get install libreoffice -y
RUN apt-get update && apt-get install ghostscript -y
RUN apt-get update && apt-get install imagemagick -y
RUN apt-get update && apt-get install fonts-roboto -y

#Set the ImageMagick-6 policy.xml file so we can do our thing.
RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml
RUN sed -i -E 's/name="memory" value=".+"/name="memory" value="8GiB"/g' /etc/ImageMagick-6/policy.xml
RUN sed -i -E 's/name="map" value=".+"/name="map" value="8GiB"/g' /etc/ImageMagick-6/policy.xml
RUN sed -i -E 's/name="area" value=".+"/name="area" value="8GiB"/g' /etc/ImageMagick-6/policy.xml
RUN sed -i -E 's/name="disk" value=".+"/name="disk" value="8GiB"/g' /etc/ImageMagick-6/policy.xml

ARG CACHEBUST=1

ADD requirements.txt requirements.txt

RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["bin/bash"]