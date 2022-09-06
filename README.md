# Huginn-Docker-Compose_AMD_X86_ARM
Compiled huginn docker run command converted into docker-compose.yml file. Includes images for both ARM/aarch64 and x86 Linux/AMD infrastructure. Compose file also includes separate container for MySQL database and separate docker network. This also includes persistant volumes so data is not lost on container recreation.

# Getting Started

You can either clone the repository or copy the file and follow the instructions below.

```bash
git clone https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM.git
```

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
![docker-compose example](https://user-images.githubusercontent.com/111924572/188748919-8f59c65f-0f1a-42bf-9849-7e37e5d448a9.jpg)


