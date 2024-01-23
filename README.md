# Huginn-Docker-Compose_AMD_X86_ARM
Compiled huginn docker run command converted into docker-compose.yaml file. Includes images for both ARM/aarch64 and x86 Linux/AMD infrastructure. Compose file also includes separate container for MySQL database and separate docker network. This also includes persistant volumes so data is not lost on container recreation. Options will allow you to run on any physical linux machine (including RaspberryPi) and virtual Machines. Tested on Debian and Ubuntu.
</br>
#### Update to show new repo for AMD_x86: ghcr.io/huginn/huginn
<table>
<tr>
<th>Architecture</th>
<th>Available</th>	
</tr>
<tr>
<td>x86-64</td>
<td>✅</td>
</tr>
<tr>
<td>amd64</td>
<td>✅</td>
</tr>
<tr>	
<td>arm64</td>
<td>✅</td>
</tr>
<tr>
<td>arm64v8</td>
<td>✅</td>
</tr>
<tr>
<td>armhf</td>
<td>✅</td>
</tr>
<td>arm32v7</td>
<td>✅	</td>
</table>

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
sudo nano docker-compose.yaml
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
image: ghcr.io/huginn/huginn
```

<strong>ARM/aarch64</strong>

```bash
image: mjysci/huginn:arm32v7 
#image: ghcr.io/huginn/huginn
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

# Consider Extra Security by Adding an .env file to protect passwords for your databases

create a .env file for the Docker Compose file you provided, you can create a new file called .env in the same directory as the Docker Compose file and add the following contents:
</br>
```bash
HUGINN_ROOT_PASSWORD=your_huginn_root_password
HUGINN_PASSWORD=your_huginn_password
HUGINN_DATABASE=your_huginn_database
HUGINN_USER=your_huginn_user
```
</br>
Then, in the Docker Compose file, you can reference the environment variables in the environment field of the huginn and mysql services like so:

```bash
huginn:
# other service configuration
environment:
HUGINN_ROOT_PASSWORD: ${HUGINN_ROOT_PASSWORD}
HUGINN_PASSWORD: ${HUGINN_PASSWORD}
HUGINN_DATABASE: ${HUGINN_DATABASE}
HUGINN_USER: ${HUGINN_USER}
mysql:
# other service configuration
environment:
MYSQL_ROOT_PASSWORD: ${HUGINN_ROOT_PASSWORD}
MYSQL_PASSWORD: ${HUGINN_PASSWORD}
MYSQL_DATABASE: ${HUGINN_DATABASE}
MYSQL_USER: ${HUGINN_USER}
```
</br>
This will allow you to store sensitive information such as passwords and secrets in the .env file, rather than hardcoding them in the Docker Compose file. The .env file should not be committed to version control, as it may contain sensitive information.

# Having Some Trouble? See the FAQ

https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM/blob/main/FAQ.md
</br>
</br>
</br>
</br>
</br>
</br>
![Huginn small art](https://user-images.githubusercontent.com/111924572/188938817-6fa7d75f-948d-4f40-9706-df0bff4b1529.jpg)


