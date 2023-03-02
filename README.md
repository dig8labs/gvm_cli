# gvm-cli
Small Script to remotely use GVM, made for tests only. 
This allows you to control GVM hosted on another machine remotely via Command line.

```
git clone https://github.com/dig8labs/gvm_cli
cd gvm_cli
python3 gvm_cli.py
```

### Setup

##### Connection
We need to create a user with a shell that points to a Script that exposes the socket gvmd.sock.
**Gvmd socket must be setup.**
1. Install Complete SSH.
```
apt-get install ssh
```
2. Create the Script that exposes the socket.
```
#!/bin/bash
socat UNIX:/var/run/gvmd/gvmd.sock -
```
Save the script to ``/home/$USER/myuser/run.sh``

4. Set permissions.
```
cd /home/$USER/myuser
chmod +x run.sh
sudo chmod a+w+r /var/run/gvmd/gvmd.sock
```
**Note**: The permissions of gvmd.sock are changed everytime by gvm. The last command needs to be run everytime on startup.

5. Create user.
```
useradd -s /home/$USER/myuser/run.sh myuser
passwd myuser
```
This will create a user named __myuser__ with your set password.
Before running gvm_cli.py edit settings.ini and test connection.


### Screenshot
![s](https://github.com/dig8labs/gvm_cli/raw/main/rgvm.PNG)

- March 3, 2023
