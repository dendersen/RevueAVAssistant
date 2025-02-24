@echo off
echo "warning, do not run this if you have git or docker installed as it may cause problems"
pause
echo "this will instal git and docker, which are required for this program"
pause
winget install -e --id Git.Git
winget install -e --id Docker.DockerDesktop
echo "git and docker has been installed"
echo "this will now clone the repository"
pause
git clone https://github.com/dendersen/RevueAVAssistant.git
cd RevueAVAssistant
cd commandline
echo "the repository has been cloned"
echo "the next step is to run 'install.bat' in RevueAVAssistant/commandline"
pause