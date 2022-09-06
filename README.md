# Huginn-Docker-Compose_AMD_X86_ARM
Compiled huginn docker run command converted into docker-compose.yml file. Includes images for both ARM/aarch64 and x86 Linux/AMD infrastructure. Compose file also includes separate container for MySQL database and separate docker network. This also includes persistant volumes so data is not lost on container recreation.

# Getting Started

You can either clone the repository or copy the file and follow the instructions below.

<strong>1st Option: git clone process:</strong>

it will download it into its own folder. Do not run docker-compose up -d in this folder, it looks messy. Either rename the folder to huginn or move the file to newly created huginn folder.

```bash
git clone https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM.git
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
