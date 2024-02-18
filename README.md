# FoodGram Project (Yandex Practicum thesis)

## Description

The FoodGram project is an online platform for creating, searching, and exchanging culinary recipes. Users can register, create their own recipes, add them to favorites and shopping lists, as well as share their culinary masterpieces with other participants.

## Technologies Used

The FoodGram project utilizes the following technologies:

- Django: web framework for backend development
- Django REST framework: tool for creating APIs
- PostgreSQL: database for data storage
- Docker: application containerization
- Nginx: web server for handling HTTP requests
- HTML/CSS/JavaScript: frontend application

## Running Instructions

To run the project on your local machine, follow these steps:

1. Install Docker: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
    
    a. A Docker account will also be required for project operation on a remote server.

2. Clone the project repository:
```
git clone https://github.com/olegpro171/foodgram-project-react
cd foodgram-project-react/infra
```

3. Run compose:
```
sudo docker compose up --build
```

Remote server deployment is also provided (optional):

4. Build and upload `frontend` and `backend` images to Dockerhub:

```
sudo docker login

sudo docker build -t <username>/foodgram_frontend ../frontend
sudo docker build -t <username>/foodgram_backend ../backend
```

5. Configure the `docker-compose-production.yml` file: specify the backend and frontend image names. Example:

```
backend:
    ...
    image: docker_username/foodgram_backend:latest
    ...
```

6. Create a `.env` file and configure it according to `.env.example`.

7. Copy files `docker-compose-production.yml`, `nginx.conf`, and `.env` to the remote server directory `<project directory>/infra/` using a convenient method.

8. Execute the command on the remote server:

```
docker compose -f </path/to/docker-compose-production.yml> up -d
```

## Request Examples

Examples of requests that can be executed in the FoodGram application:

Registering a new user:


    POST /api/auth/users/
    Content-Type: json

    {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword"
    }


User authentication:


    POST /api/auth/token/login/
    Content-Type: application/json

    {
        "email": "newuser@example.com",
        "password": "securepassword"
    }

Creating a new recipe:

    POST /api/recipes/
    Authorization: Token yourAuthToken
    Content-Type: application/json

    {
        "name": "Delicious Pasta",
        "text": "A tasty pasta recipe...",
        "cooking_time": 30,
        "tags": [1, 2, 3],
        "ingredients": [
            {"id": 1, "amount": 200},
            {"id": 2, "amount": 100}
        ]
    }   


## Author

The FoodGram project was developed as part of the Yandex.Practicum program. Developer: Oleg Proshkin.

You can contact me at oleg.pro171@gmail.com.
