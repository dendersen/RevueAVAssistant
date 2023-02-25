FROM python:3.8-slim-buster

RUN useradd app

RUN apt-get update &&\
    apt-get install tree -y &&\
    apt-get install libreoffice -y &&\
    apt-get install ghostscript -y &&\
    apt-get install imagemagick -y &&\
    apt-get install fonts-roboto -y

#Set the ImageMagick-6 policy.xml file so we can do our thing.
RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml &&\
    sed -i -E 's/name="memory" value=".+"/name="memory" value="8GiB"/g' /etc/ImageMagick-6/policy.xml &&\
    sed -i -E 's/name="map" value=".+"/name="map" value="8GiB"/g' /etc/ImageMagick-6/policy.xml &&\
    sed -i -E 's/name="area" value=".+"/name="area" value="8GiB"/g' /etc/ImageMagick-6/policy.xml &&\
    sed -i -E 's/name="disk" value=".+"/name="disk" value="8GiB"/g' /etc/ImageMagick-6/policy.xml

ADD requirements.txt requirements.txt

RUN python -m pip install -U pip &&\
    python -m pip install -r requirements.txt

ENTRYPOINT ["bin/bash"]