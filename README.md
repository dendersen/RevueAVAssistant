# RAVA - the Revue AV Assistant

RAVA, the Revue AV Assistant, is a tool created to greatly reduce the amount of repetitive AV tasks for the pf revue. It helps with folder structure, creating and updating songs for QLab. 

<p align="center">
<img src="https://user-images.githubusercontent.com/35364024/154814545-f17f99f9-2893-4633-b5ff-43eb7d128a6b.png" width="450">
</p>

If you have any questions regarding RAVA, feel free to reach out either through creating a new [Issue](https://github.com/vstenby/RevueAVAssistant/issues/new) or by sending me an [email](mailto:viktor.s.johansson@hotmail.com).

## Getting Started with RAVA

### Docker

Docker is a tool to help deploy applications in different environments. Check out Docker's [get started](https://www.docker.com/get-started/) page here and navigate to the *Docker Desktop* session, download it and familiarize yourself a bit with how to build a Dockerfile and how to run a container. If you get stuck, Nicki's MLOps course has a [great page on Docker](https://skaftenicki.github.io/dtu_mlops/s3_reproducibility/docker.html#docker) and how to set it up.

You can check that Docker is working correctly in your machine by typing `docker run hello-world` in your terminal. If you are using Windows, I suggest checking out [Git Bash](https://gitforwindows.org/) to call stuff from the commandline, but if you are using MacOS/Linux you should be fine.

### Cloning the Repository

Assuming you have set up Docker on your machine, you now have to clone this repository. You can do that by writing the following in your terminal:

```
git clone https://github.com/vstenby/RevueAVAssistant.git
```

Navigate into your folder by writing `cd RevueAVAssistant`, and the `tree` command should look something like this:

```
(base) Viggos-MacBook:RevueAVAssistant viktorstenby$ tree
.
├── Dockerfile
├── LICENSE
├── README.md
├── rava.py
├── rava_utils.py
├── requirements.txt
└── revue_template
    ├── config.yaml
    ├── images
    ├── lyrics
    │   ├── 00_raw
    │   ├── 01_preprocessed
    │   ├── 02_pptx
    │   └── 03_png
    ├── other
    ├── qlab
    ├── sound
    └── video
```

### Building the Dockerfile

In this section, you are going to be building your Dockerfile. This only needs to be done once, and once you have built your Docker image, you don't need to worry about it anymore!

I'll demonstrate how to build the RAVA docker image using the terminal and the Docker Dekstop application. You can also do it only using the terminal, but I'm going to assume you haven't played around with Docker before. First, open up the Docker Desktop application. If you have built Docker images before, you should be able to see them here. I don't have any built images on my machine, so right now, it's empty. 

<img width="1250" alt="docker_before_building" src="https://user-images.githubusercontent.com/35364024/221357439-358a7c77-1c41-4aa0-8336-84f2cded560d.png">

Good, now let's build the Docker image. Call the following command from the terminal:

```
docker build --pull --rm -f "Dockerfile" -t rava-docker "."  
```

Note: if you're not logged in as the administrator on your system, you might need to write `sudo` followed by the command above. 

Now, this command should take a while. What's happening is that we're creating a Docker image of what RAVA needs in order to run. You can check the `Dockerfile` if you're interested to see what we're building into the image. Essentially, instead of installing these packages directly onto your computer, we're building a container with these packages so you can remove them once you're done. 

<img width="1250" alt="docker_after_building" src="https://user-images.githubusercontent.com/35364024/221357450-6391a83d-64b6-49c8-b0a8-2ec8a9aa9715.png">

You have now succesfully built your Docker image! 🎉 This only needs to be done **once**, and once you've succesfully built your image it's only a matter of spinning up a container, which is super easy.

## Spinning up the Docker container

Now, I'll show you how to start a Docker container. Generally it's a good idea to close your container when you're not using RAVA, since it consumes memory having the container running in the background. 

First, make sure that you are inside the `RevueAVAssistant` folder in your terminal. This can be checked using `pwd` and should return something along the lines of `/.../.../RevueAVAssistant`. If you are in the right folder in your terminal, then copy the following line into your terminal and press return.

```
docker run -dit -m 2g --name rava -v "$(pwd)":/RevueAVAssistant rava-docker
```

This should spin up a container with that you just built. The container is mounted on your local computer, so that the `RevueAVAssistant` folder in your container is the same as the `RevueAVAssistant` folder on your computer, but we'll see that later. You can verify that you succesfully started your container by checking the Docker Desktop app.

<img width="1246" alt="rava_running" src="https://user-images.githubusercontent.com/35364024/221357970-30387c37-8bab-4374-9963-7e78978deba1.png">

If you click the **CLI** (command-line interface) button seen above, you are now opening a terminal **inside** your running Docker container. Inside this container, the Dockerfile made sure you have a) Python, b) LibreOffice for creating the powerpoints and c) ImageMagick, which is going to create pngs from your powerpoints. 

<img width="1120" alt="container_checks" src="https://user-images.githubusercontent.com/35364024/221358142-01834d13-98d9-4ed7-aace-628de178afa8.png">

In the terminal you have started inside of your Docker container, navigate to the `RevueAVAssistant` folder by writing 

```
cd /RevueAVAssistant
```

and writing `tree` should allow you to see all of the files! Congratulations - you now know how to build a Docker image and how to open an interactive session inside of your container. Docker is a nifty tool for making code run on different machines, so I hope you've learned a thing or two! 

While setting this up might have taken you a bit of time, believe me, it's **much** easier than having to install all of these packages on your own machine and getting it to run there!

Since the container is running in the background, remember to close it once you're done with it and need your RAM for something else (QLab, for instance!)

<img width="1245" alt="docker_delete" src="https://user-images.githubusercontent.com/35364024/221359735-72423bd5-527a-45a0-98d6-bb0b1994ff08.png">

Also remember that built Docker images take up space on your computer, so clean up through Docker Desktop every once in a while!

<img width="1245" alt="docker_clean" src="https://user-images.githubusercontent.com/35364024/221359843-9468fb2f-41ec-4a26-9bf3-2651404c5065.png">


# Examples

