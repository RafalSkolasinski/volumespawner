# MesoSpawner

Our modification of SystemUserSpawner. We basically subclass it and modify to
our needs.

Basic difference is that we don't want to put homes of users (in our case
students of our programming course) inside ``/home/{username}`` but rather inside
some folder of a host user that starts hub. Default is set to be:
``/home/{host_username}/spawned_users/{username}``

Later we use host's user_id for users inside container.
During start procedure we make sure that students folders on the user side
exists. If they doesn't we create them.

Advantages:
* we don't pollute /home/ folder with temporary students' homes
* we can easily distribute some files to student's homes without using root
    privileges

# References
1. [jupyterhub](https://github.com/jupyter/jupyterhub)
2. [oauthenticator](https://github.com/jupyter/oauthenticator)
3. [dockerspawner](https://github.com/jupyter/dockerspawner)

In case of problems, please visit first references listed above and try original
packages.


# Installation
## jupyterhub
```
sudo apt-get install python3-dev
sudo apt-get install npm nodejs-legacy
sudo npm install -g configurable-http-proxy

pip3 install jupyterhub ipython[all]
npm install
```

## oauthenticator
```
git clone https://github.com/jupyter/oauthenticator.git
cd oauthenticator

pip3 install -r requirements.txt
python3 setup.py install
cd ..
```

## dockerspawner
```
git clone https://github.com/jupyter/dockerspawner.git
cd dockerspawner

pip3 install -r requirements.txt
python setup.py install
cd ..
```



# Running

build ``mesouser`` image
```
docker build -t jupyter/volumeuser volumeuser
```

Then run everything as standard dockerspawner example but with modified
``jupyterhub_config.py`` ([check](https://github.com/jupyter/dockerspawner/tree/master/examples/oauth))
