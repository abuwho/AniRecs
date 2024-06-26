![Anirecs Main](https://github.com/abuwho/AniRecs/actions/workflows/main.yml/badge.svg)
![Frontend CI](https://github.com/abuwho/AniRecs/actions/workflows/frontend-ci.yaml/badge.svg)

# AniRecs: Anime Recommender Based on Preference

## Description

The backend can be run using docker-compose. And the frontend is deployed on [Vercel](https://anirecs.vercel.app). In order to run the application, it is necessary to have the docker container running on your local machine. 

## Installation steps

- Clone the repository: 
    ```shell
    # Clone
    git clone git@github.com:abuwho/AniRecs.git
    # Change directory
    cd AniRecs
    ```

- Run `backend` container (make sure you have Docker daemon running on your machine):
    ```shell
    # Change directory
    cd backend/volumes
    # Run docker-compose
    docker-compose up
    ```

- Run `frontend`
    - Can be run in 2 ways: 
        1. Vercel function
            - Just visit https://anirecs.vercel.app
        2. Using Docker
            ```
            # Pull from Docker Hub
            docker pull abuwho/anirecs-frontend:latest
            # Run container
            docker run -p 3000:3000 abuwho/anirecs-frontend
            # Go to http://localhost:3000
            ```

## Contributors

- David [@Ejedavy](https://github.com/Ejedavy) Eje 
- Abu [@abuwho](https://github.com/abuwho) Huraira
- Chibuoyim [@bruteforceboy](https://github.com/bruteforceboy) Ogbonna
- Wesam [@Wesam-Naseer](https://github.com/Wesam-Naseer) Naseer
