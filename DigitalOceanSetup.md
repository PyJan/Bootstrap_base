# set up SSH key (Secure Shell, 2 keys - public key, private key; challenge-response authorization)

ssh-keygen # generate keys
la .ssh # see the keys
sudo vi .ssh/id_rsa.pub # read the public key and copy it on the server
ssh root@157.230.104.180 # log in at the server
logout # end your server session
