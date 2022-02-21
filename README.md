# RAVA - the Revue AV Assistant

RAVA, the Revue AV Assistant, is a tool created to greatly reduce the amount of repetitive AV tasks for the pf revue. It helps the user with folder structure, creating and updating song slides. Make sure to also check out the [*Using QLab with RAVA*](https://github.com/vstenby/RevueAVAssistant/wiki/Using-QLab-with-RAVA) guide in the Wiki. 

<p align="center">
<img src="https://user-images.githubusercontent.com/35364024/154814545-f17f99f9-2893-4633-b5ff-43eb7d128a6b.png" width="450">
</p>

## Getting Started with RAVA

Getting started with RAVA is easy. If you have not used RAVA before, the first step is cloning it. 

```
git clone https://github.com/vstenby/RevueAVAssistant.git
```

Once you have cloned the repository, try navigating to the folder and calling the RAVA script with `--help` to see which arguments you can give. Depending on where you cloned the repository, it could look something like this:

```
cd /Users/pfhumor/Documents/RevueAVAssistant/ && python rava.py --help
```

## Understanding RAVA's File Structure

If you have cloned RAVA, the folder structure might not look like much. 

```
.
├── LICENSE
├── README.md
└── rava.py
```

This is because at the moment, there are no projects. You can add a new project as follows:

```
python rava.py --project MyProject
```

You will also be prompted to enter a Overleaf URL from which RAVA will fetch the songs located in the `/Musik/` folder of your Overleaf project. **Your Overleaf document should have a `Musik`-folder with songs as shown below.** 

```
.
⋮
├── Musik
│   ├── songa.tex
│   ├── songb.tex
⋮
│   └── songz.tex
⋮
└── main.tex
```

You don't *have* to give RAVA the Overleaf URL, but if you don't, you will have to move some files yourself. After downloading your .tex files (either via Overleaf i.e. git or manually), your structure will look like this. 

```
.
├── LICENSE
├── MyProject
│   ├── image
│   ├── lyrics
│   ├── other
│   ├── pptx
│   ├── qlab
│   ├── sound
│   ├── tex
│   │   ├── songa.tex
│   │   ├── songb.tex
⋮
│   │   └── songz.tex
│   └── video
├── README.md
└── rava.py
```

In short, the idea behind the folder structure is:

* `image`, `sound`, `video`, `qlab` and `other`. RAVA will not touch these files and you can use them as you see fit. 
* `tex`: This folder contains all of your tex files and will change the structure of your project. RAVA will **not** change any of your tex files, but they will be read. 
* `pptx`: For each tex file in the `tex` folder, RAVA will create a powerpoint for that song. The structure of the `pptx` folder be as follows:

  ```
  .
  ├── songa.pptx
  ├── songb.pptx
  ⋮
  └── songz.pptx
  ```
  **Important: If you have made changes to e.g. `songa.tex`, then RAVA will overwrite `songa.pptx`. Therefore - be careful of making changes in the pptx files and then tex files afterwards. Correct what you want in the tex files and run RAVA again.**
  
  
* `lyrics`: Here you will find the .png images with text for each song. Once populated, it will have the following structure:

  ```
  .
  ├── songa
  │   ├── songa00.png
  │   ├── songa01.png
  │   ├── songa03.png
  │   └── songaxx.png
  ├── songb
  │   ├── songb_00.png
      ⋮
  │   └── songb_xx.png
  ⋮
  └── songz
      ├── songz_00.png
      ⋮
      └── songz_xx.png
  ```
  **Important: These folders are wiped every time the corresponding pptx is updated. Do not save important stuff in these folders!** 
  
 
## RAVA's Dependencies

In order to do her job, RAVA has some needs. I could imagine that the following caused some problems: 

1) `git` to clone the Overleaf repository. 
2) `python-pptx` to generate pptx files. Install using `pip install python-pptx`.
3) `unoconv` and `libreoffice` to generate pdfs from pptx. Check out this [guide](https://nono.ma/export-powerpoint-to-jpg-images-png-pdf) if you are running into issues. 
4) ImageMagick to chop up the pdf into images. Can be installed via [Homebrew](https://formulae.brew.sh/formula/imagemagick) as well.


RAVA has been tested on the following:
* Intel MacBook Pro (2017) running macOS Monterey (12.2).
* Mac Pro (2012) running macOS Mojave (10.14.6).
