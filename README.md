# Accoknox Social Media

a social media application api demonistration 

Backend : Django with DRF ( djanog REST framework ) 

Database : SqlLite3


## Hosted API Root 

```bash
https://accoknox-social-media-backend.onrender.com/api/
```

### Local Installation

1- Clone the project
```bash
  git clone https://github.com/mansoorgt/accoknox-social-media-backend.git
```

2- Change directory to the project directory
```bash
cd accoknox-social-media-backend
```

3- Make a virtual environment and activate (optional)
```bash
python -m venv env
env/Scripts/activate #windows 
source env/bin/activate #mac and linux
```
3- Install dependencies
```bash
   pip install -r requirements.txt 
```
4- Run the application
```bash
   python manage.py runserver 
    #accoknox social media application now running on localhost:8000
```

### Local Installation

1- build docker image
```bash
docker build --tag 'accunox-social-media-mansoor' .
```
2- run docker image
```bash
docker run --detach 'accunox-social-media-mansoor'
#now the application running on localhost:8000
```
## Api URLS
1 - Registration 👉 /sign-up

2 - Login 👉 /login

3 - Seach 👉 /search

4 - Send Friend Request 👉 /send-request

5 - Get Pending Request 👉 /get-pending-requests

6 - Update Friend Request 👉 update-friend-request

7 - Get all accepted friends 👉 /get-all-friends

### You can also find the POSTMAN collection on the repository to testing purpose

Two collection is ther on for localhost one for Hosted in Render.com

#⚠️ please make sure add authentication token on every api request except sign up and login 

# THANKS 
