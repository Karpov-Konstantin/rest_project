# REST project on DRF

## Steps installing:
### 1.Install git:
1.1. sudo apt-get update

1.2. sudo apt-get install git-core

### 2.Install docker:
https://docs.docker.com/install/linux/docker-ce/ubuntu/
##### For linux:
2.1. Install packages to allow apt to use a repository over HTTPS:
```bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

2.2. Add Docker’s official GPG key:
```bash 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

2.3. Get fingerprint
```bash
sudo apt-key fingerprint 0EBFCD88
```

2.4. Add repository

```bash
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

2.5. Install docker package

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### 3. Install docker-compose
https://docs.docker.com/compose/install/:

###### For linux:
3.1 Download the current stable release of Docker Compose:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

3.2 Apply executable permissions to the binary:
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

### 4. Run project
4.1 Download git repository
```bash
git clone https://github.com/Karpov-Konstantin/rest_project.git
```

4.2 move to project directory with Dockerfile

4.3 Build docker containers
```bash
sudo docker-compose build
```

4.4 Run docker containers
```bash
sudo docker-compose up -d 
```

##### 4.5 If it's 1st run, it's necessary to make migrations
```bash
sudo docker-compose exec app python manage.py makemigrations
sudo docker-compose exec app python manage.py migrate
```

### 5. Run tests

5.1 Run django tests 
```bash
sudo docker-compose exec app python manage.py test
```