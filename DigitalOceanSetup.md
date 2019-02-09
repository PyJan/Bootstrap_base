## set up SSH key (Secure Shell, 2 keys - public key, private key; challenge-response authorization, on Windows they use PuTTY)

https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys

ssh-keygen # generate keys
la .ssh # see the keys
sudo vi .ssh/id_rsa.pub # read the public key and copy it on the server
ssh root@157.230.104.180 # log in at the server
logout # end your server session

### setup regular user with sudo privileges

https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04

### flask deployment on Ubuntu

 https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

 ### NGINX setup and commands

 https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04

 systemctl status nginx
 sudo systemctl start nginx
 sudo systemctl stop nginx

### test uwsgi

uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

### git cheat sheet

https://www.digitalocean.com/community/tutorials/how-to-use-git-a-reference-guide