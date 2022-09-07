![faq-banner](https://user-images.githubusercontent.com/111924572/188916778-36449805-f2f8-44fb-85ea-35a6258c9208.png)
</br>
</br>
<b>1. When I run docker-compose up -d I get an error to check if the docker daemon is started or a permission error, what is happening?</b>
</br>
</br>
Try running sudo infront of your ``` docker-compose up -d ``` . If you have not added your userID to the permission group, you will need to run sudo or modify your user permissions by doing the following in terminal: ``` sudo usermod -aG docker <username> ``` . Then type the following to switch to the same user (need to do this to "sign out and back in"): ``` su - ${USER} ```  You will be prompted to enter your user's password to continue. If you want you can also confirm that your user is now added to the docker group by typing: ``` group ``` .
</br>
</br>
<b>2. When I spin up my containers I get an error of unsupported architecture, why?</b>
</br>
</br>
You may have not edited the docker-compose.yml file for your supported architecture. From the folder that your docker compose file is located in run: ``` sudo nano docker-compose.ymal ``` . Use # to "comment" out the image you <i>do NOT</i> want to use. remove the # for the supported image you want to use. This needs to be done for the huginn and the mysql container in the file. Comments in the file help explain this.
</br>
</br>
<b>3. I try to download the GitHub yaml file using curl, but it just returns content and not the file?</b>
</br>
</br>
curl will not pull the file in file format, but display it instead. When downloading just the yaml file directly, use wget ``` wget https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM/blob/main/docker-compose.yaml ``` .
</br>
</br>
<b>4. This compose file puts the containers on a seperate network. I want them on the same network as my other containers.</b>
</br>
</br>
No problem, just edit the compose file and remove the network variables from both the huginn and mysql container image. Also remove the Network specifications at the bottom of the file that define the seperate network and subnets.
</br>
</br>
<b>5. You are using .yaml instead of .yml why? and is this a mistake?</b>
</br>
</br>
either extension will work. yaml stands for "yet another markup language". I just use the 4 character extension. Many people are used to the standard 3 character extension. Feel free to change the extension if you would like. It will not break anything.
