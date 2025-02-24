# RAVA - the Revue AV Assistant

RAVA, the Revue AV Assistant, is a tool created to greatly reduce the amount of repetitive AV tasks for the pf revue. It helps with folder structure, creating and updating songs for QLab. 

<p align="center">
<img src="https://user-images.githubusercontent.com/35364024/154814545-f17f99f9-2893-4633-b5ff-43eb7d128a6b.png" width="450">
</p>

If you have any questions regarding RAVA, feel free to reach out either through creating a new [Issue](https://github.com/dendersen/RevueAVAssistant/issues) or by sending me an [email](mailto:dxyz@mtdm.dk).

## Easy mode
hi, this is the new fork of RAVA. While making it easier to avoid the headaches that song writers love giving us, i ended up making this easy mode guide. The actually good guide underneath is still correct and much better written.<br>

### begining
if you are complete noob just download the file called <br>

```commandLine/all_prep.bat```

this one file can do a lot for you, it will install git, install docker and clone the repository. now if you know how to do any of them by yourself don't use it.<br>

instead make sure you have a resent docker installed and git installed the run

```git clone https://github.com/dendersen/RevueAVAssistant.git```

this will clone the repository so you are ready to begin


### magic files
open the new folder called ```RevueAVAssistant```

in here a folder called commandline has all you really need to prepare. simply run 
```install.bat``` to prepare, this will prepare docker and only has to be run once.

now we are ready simply click ```run.bat``` to start the programme

### remember the lyrics

unfortunatly you have to make the correct folder structure, i suggest copying ```revue_template``` and calling it whatever you want. then simply copy your lyrics into the correct folder:<br>
```name/lyrics/oo_raw```<br>
do remember to place the ```\begin{obeylines}``` and ```\end{obeylines}``` that the song writers definetly forgot.

### DIY

inside the command line you now have to do things yourself unfortunatly but it will be very little

always start by typing ```cd RevueAVAssistant```<br>
this will open the folder with the script.

then ```python rava.py --project name``` will process the data in the folder called whatever you write instead of name. <br>


### reruns

so you made some changes, probably som \textit left in the middle of the lyrics<br>
you do need to remove some files, ```name/lyrics/01_preprocessed``` and ```name/lyrics/02_pptx``` has the files. remove the files with the name of the song that needs to be rerun. and the 

### giving up (or cleaning up after revue)

so to delete everything don't just remove the folder as this will still eat a bit of space instead, start by calling ```clean.bat``` from the ```commandLine``` folder this undoes the effect of ```install.bat``` and will have to be run again if you want to use RAVA.

### the original guide comes now

## Getting Started with RAVA

### Docker

Docker is a tool to help deploy applications in different environments. Check out Docker's [get started](https://www.docker.com/get-started/) page here and navigate to the *Docker Desktop* session, download it and familiarize yourself a bit with how to build a Dockerfile and how to run a container. If you get stuck, Nicki's MLOps course has a [great page on Docker](https://skaftenicki.github.io/dtu_mlops/s3_reproducibility/docker.html#docker) and how to set it up.

You can check that Docker is working correctly in your machine by typing `docker run hello-world` in your terminal. If you are using Windows, I suggest checking out [Git Bash](https://gitforwindows.org/) to call stuff from the commandline, but if you are using MacOS/Linux you should be fine.

### Cloning the Repository

Assuming you have set up Docker on your machine, you now have to clone this repository. You can do that by writing the following in your terminal:

```
git clone https://github.com/dendersen/RevueAVAssistant.git
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
docker run -dit --name rava rava-docker
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


# Tutorial

Having done all of the above, you're ready for the tutorial! This will show you the basic ins and outs of RAVA.

## Doing the First Pass

You, of course having read the entire guide thus far, are now an expert in Docker and know how to spin up a Docker container and navigate the terminal. In your interactive terminal inside of the Docker container, navigate to the `/RevueAVAssistant` folder from before.

Paste the following lyrics

```
Skema B, den med Michael P
Mere underholdende end skema A og C
Med sit smil, og sin læringsstil
Lærer Michael dig at bruge Eulers tal og pi
Husk’ hel’ pensum? Helt umuligt
Men jeg består nu - helt utroligt!
```
into a file called `skema_b.txt` inside of the `/RevueAVAssistant/project_template/lyrics/00_raw/` folder on *your local machine*. Similarly, place the lyrics below into `dataanalyse.txt` located in the same folder.

```
Du’ et fedt datasæt
Min analyse bliver let
Ingen manglende værdier
Alt kontinuert 
Nu skal jeg til at ta’ et valg
Om middel eller typetal 
Hørte de sku’ vær’ de bedste 
Men det er forkert

Medianer
Gennemsnittets bror
Smarter’ end man tror
Medianer
Dem beregner jeg
```

You can verify that the folder is mounted and therefore can be read from inside your container by writing `tree`. Now to the fun part! Write 

```
python rava.py --project revue_template
```

and let RAVA do its job. Once done, you should see that your container with RAVA has populated the folder on your local machine!

<img width="1265" alt="populated" src="https://user-images.githubusercontent.com/35364024/221361256-8c39e05b-fdfc-4265-ba91-7496c7ffbd8f.png">

## Reflecting a bit on the Pipeline

Having created your first pngs, let's understand a bit of how RAVA works under the hood. 

* The `00_raw` folder is used to store your raw lyrics. You can put `.tex` files here, but you can also play it safe and put `.txt` files here.
    *  If you place `.tex` files here, then `preprocess_tex` from `rava_utils.py` will try and clean up your messy `.tex` file, extract the lyrics and dump it into `01_preprocessed`. Experience tells me that because people always put a lot of garbage into the `.tex` files, then most often or not, I have not accounted for some stupid edge case and the function fails somehow. 
   
    *  If you place `.txt` files here, nothing will happen and it will be copied to the `01_preprocessed` folder. This is pretty easy.
    
* The `01_preprocessed` folder is for preprocessed lyrics. We will edit this in a bit.

* The `02_pptx` folder is for the powerpoints.

* The `03_png` folder contains a subfolder for each song, here `dataanalyse` and `skema_b`. 
    * The `dataanalyse` folder has 14 pngs in total, one for each line in `01_preprocessed/dataanalyse.txt`. 
    * The `skema_b` folder has 6 pngs in total, one for each line in `01_preprocessed/skema_b.txt`. 

## Fixing Errors

Fixing errors is a **big** part of the work. Lyrics don't match up with what singers are singing, and sometimes the lines breaks aren't where we want them to be. Let's have a look at the 6 pngs that RAVA produced. 

`000.png`| `001.png` | `002.png` | `003.png` | `004.png` | `005.png` 
:-:|:-:|:-:|:-:|:-:|:-:|
![skema_b_000](https://user-images.githubusercontent.com/35364024/221361749-80114a7a-df6d-4488-93ab-76d4e340680b.png)|![skema_b_001](https://user-images.githubusercontent.com/35364024/221361755-9e04f784-4365-428e-be9d-5b3fa69c2a15.png)|![skema_b_002](https://user-images.githubusercontent.com/35364024/221361761-a179112e-7b1c-4c64-bd0e-daa02ad96d8e.png)|![skema_b_003](https://user-images.githubusercontent.com/35364024/221361778-2b8b2580-e8ff-4dfc-8483-41f1cceef6d6.png)|![skema_b_004](https://user-images.githubusercontent.com/35364024/221361788-07cf94b2-7f4e-44d4-adb5-5deea77f9260.png)|![skema_b_005](https://user-images.githubusercontent.com/35364024/221361790-7c33f79f-ef32-4078-b0e0-6b0372963bd0.png)

I have found a few changes that I want to make - for instance, I would like specify some of the line breaks and I would like to split some of the lyrics up across multiple slides. I do this by modifying `01_preprocessed/skema_b.txt` and change it to the following:

```
Skema B!
Den med Michael P!
Mere underholdende \n end skema A og C
Med sit smil, \n og sin læringsstil
Lærer Michael dig \n at bruge Eulers tal og pi
Husk’ hel’ pensum? Helt umuligt
Men jeg består nu - helt utroligt!
```

I save the song and rerun RAVA from my Docker container by calling `python rava.py --project revue_template`. 

```
# python rava.py --project revue_template
RevueAVAssistant: 2023-02-25 14:27:13,104 - INFO - dataanalyse: processing...
RevueAVAssistant: 2023-02-25 14:27:13,107 - INFO - dataanalyse: 00 -> 01 skipped, preprocessed song already exists.
RevueAVAssistant: 2023-02-25 14:27:13,112 - INFO - dataanalyse: 01 -> 02 skipped, pptx is up to date.
RevueAVAssistant: 2023-02-25 14:27:13,118 - INFO - dataanalyse: 02 -> 03 skipped. png is already up to date.

RevueAVAssistant: 2023-02-25 14:27:13,118 - INFO - skema_b: processing...
RevueAVAssistant: 2023-02-25 14:27:13,123 - INFO - skema_b: 00 -> 01 skipped, preprocessed song already exists.
RevueAVAssistant: 2023-02-25 14:27:13,385 - INFO - skema_b: 01 -> 02 done.
RevueAVAssistant: 2023-02-25 14:27:13,394 - INFO - skema_b: 02 -> 03 creating pngs, please wait...
RevueAVAssistant: 2023-02-25 14:27:24,618 - INFO - skema_b: 02 -> 03 complete, 7 pngs written to ./revue_template/lyrics/03_png/skema_b/.
```

Let's have a look at the pngs again!

`000.png`| `001.png` | `002.png` | `003.png` | `004.png` | `005.png` | `006.png` |
:-:|:-:|:-:|:-:|:-:|:-:|:-:|
![skema_b_000](https://user-images.githubusercontent.com/35364024/221362359-1457cb49-00a4-4111-8602-8f1e49516753.png)|![skema_b_001](https://user-images.githubusercontent.com/35364024/221362362-53bbeb83-11b9-45e4-88ea-b46e9cca1847.png)|![skema_b_002](https://user-images.githubusercontent.com/35364024/221362365-b0a44bde-9cc2-48ce-b352-f9281832cf54.png)|![skema_b_003](https://user-images.githubusercontent.com/35364024/221362366-96e28f9e-f897-4b43-b07d-fd5309fa7d35.png)|![skema_b_004](https://user-images.githubusercontent.com/35364024/221362367-6a4bac8b-f0fa-46fe-8545-65252900f189.png)|![skema_b_005](https://user-images.githubusercontent.com/35364024/221362368-0fcd8e7d-bb78-469b-b8dd-6ee5e5d47a66.png)|![skema_b_006](https://user-images.githubusercontent.com/35364024/221362369-0e133e52-d79a-415a-95ca-40223bcc3b7f.png)

Great! From this, you've learned the essentials of going from the `.txt` file in the `01_preprocessed` folder to the pngs.
* Each line corresponds to a png. 
    * Blank lines will give you a black screen (check `01_preprocessed/dataanalyse.txt` and `dataanalyse_008.png`!) 
* Add `\n` if you want to control where the line breaks.
* When rerunning RAVA, it will check whether or not `01_preprocessed` is newer than `03_png` for that specific song. If so, it will remake the `.pptx` file and then the `png` files. 

## Creating Your Own Project

Now let's create your own project. Delete the files in `00_raw`, `01_preprocessed`, `02_pptx` and delete the subfolders `skema_b` and `dataanalyse` in the `03_png` folder. Copy the `revue_template` and rename it something new, e.g. `Revue2022`.

<img width="1267" alt="new_project" src="https://user-images.githubusercontent.com/35364024/221362830-6fcfede5-378e-488d-8b3d-802b11034a57.png">

Take all of your `tex` songs (or `txt`) and dump them in your newly created folder. Calling `tree` from the container terminal allows you see your files before you use RAVA.

```
# tree
.
├── Dockerfile
├── LICENSE
├── README.md
├── Revue2022
│   ├── config.yaml
│   ├── images
│   ├── lyrics
│   │   ├── 00_raw
│   │   │   ├── Acapella.tex
│   │   │   ├── Afslutningsnummer.tex
│   │   │   ├── Åbningsnummer.tex
│   │   │   ├── Dataanalyse.tex
│   │   │   ├── Endnu_en.tex
│   │   │   ├── Frihed.tex
│   │   │   ├── Første_spacer_paa_maanen.tex
│   │   │   ├── General_engineering.tex
│   │   │   ├── Hotel_Kampsax.tex
│   │   │   ├── ICE_Kongen.tex
│   │   │   ├── Imponerer_mig_ik.tex
│   │   │   ├── Karls_sang.tex
│   │   │   ├── Manden_i_anden_kvadrant.tex
│   │   │   ├── Olkroket.tex
│   │   │   ├── Skema_B.tex
│   │   │   └── Ups_jeg_dumpede_igen.tex
│   │   ├── 01_preprocessed
│   │   ├── 02_pptx
│   │   └── 03_png
│   ├── other
│   ├── qlab
│   ├── sound
│   └── video
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

and then again, we call `rava.py`, only this time, change the `--project` argument to the folder in which you have your songs. For me, that would be:

```
python rava.py --project Revue2022
```

and grab a cup of tea or go for a walk. The `pdf` to `png` step takes a while, so have patience! You can follow along in the log to see how it's going, and if the `01_preprocessed` file is empty, it means that something went wrong in the `tex -> txt` step. And then you'll have to fix the errors, rerun the script, ...

# Closing Remarks

This concludes the documentation of RAVA! QLab is an entirely different beast which takes quite a lot of time to set up and learn, so having familiarized yourself with RAVA before starting out with QLab is definitely a good thing.

If you have any suggestions or improvements for RAVA, again, feel free to contact me. Also make sure to give this repository a star if you enjoyed it!
