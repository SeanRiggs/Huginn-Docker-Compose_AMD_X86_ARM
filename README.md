# Huginn-Docker-Compose_AMD_X86_ARM
Compiled huginn docker run command converted into docker-compose.yml file. Includes images for both ARM/aarch64 and x86 Linux/AMD infrastructure. Compose file also includes separate container for MySQL database and separate docker network. This also includes persistant volumes so data is not lost on container recreation. Options will allow you to run on any physical linux maching (including RaspberryPi) and virtual Machines. Tested on Debian and Ubuntu.

# Getting Started

You can either clone the repository or copy the file and follow the instructions below.

<strong>1st Option: git clone process:</strong>

it will download it into its own folder. Do not run docker-compose up -d in this folder, it looks messy. Either rename the folder to huginn or move the file to newly created huginn folder.This process will snag the readme and any other file adds in the repo.

```bash
git clone https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM.git
```

<b><i>Recommended:</i></b> Or move to the directory you want to install huginn in and use <b>wget</b> to pull the single docker-compose file:

```bash
wget https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM/blob/main/docker-compose.yaml
```

</br>
<strong>2nd Option: download the file and copy into new directory:</strong>

make a directory you want to install your docker-compose contaners.

```bash
mkdir huginn
```

CD into that directory

```bash
cd huginn
```

copy docker-compose.yaml into the directory
once copied, open the yaml file with nano

```bash
sudo nano docker-compose.yml
```
<p align="center"><img src="https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM/blob/main/images/docker-compose%20example.jpg"</p>

# IMPORTANT

Ensure that you comment out the images you are not going to use for your architecture. Uncomment the images in the containers that match your architecture.
The compose file is preset for AMD - x86 Linux. Adjust for ARM/aarch64. Validate before spinning up your container.

<strong><i>Huginn Container:</i></strong>
</br>
</br>
<strong>Linux x86/AMD</strong>

```bash
#image: mjysci/huginn:arm32v7 
image: huginn/huginn
```

<strong>ARM/aarch64</strong>

```bash
image: mjysci/huginn:arm32v7 
#image: huginn/huginn
```
</br>
</br>
<strong><i>MySQL Container:</i></strong>
</br>
</br>
<strong>Linux x86/AMD</strong>
</br>

```bash
#image: yobasystems/alpine-mariadb:10.4.17-arm32v7
image: mysql:latest
```
<strong>ARM/aarch64</strong>

```bash
image: yobasystems/alpine-mariadb:10.4.17-arm32v7
#image: mysql:latest
```
</br>

# Bringing up with Docker-Compose

![Docker Compose ](https://user-images.githubusercontent.com/111924572/188755814-af9ef5fd-9aa5-44a4-81dc-47bf7a1a5849.png)

The downloaded and updated docker-compose.yaml file should ready to go in the directory you chose for it (i.e. huginn). The next step is to spin up your containers using docker-compose and starging the docker daemon:

```bash
docker-compose up -d
```

You should see the images download and containers create like the following: 
![bringing up the docker-compose container](https://user-images.githubusercontent.com/111924572/188754670-9d5416b5-151c-43fb-9269-0c7955d1617b.jpg)

list your docker containers and take a look: 

```bash
docker ps
```

![running containers](https://user-images.githubusercontent.com/111924572/188754917-7a040726-8e19-4aa3-9e31-4f2ffd858a1c.jpg)

check your docker network:

```bash
docker network ls
```

![docker network ls](https://user-images.githubusercontent.com/111924572/188755073-3401ff3d-4157-4f22-b882-2c704eebe8b1.jpg)







