# web_devops
A web application using Flask that posts an Live Movenet module, to be used by cloud services for remote hosting.

## Cloning the Repo

    $ git clone https://github.com/Bsindra/web_modelnet.git

## Running docker container

    $ docker build -t movenet .

## Running the app

    $ docker run -d -p 5000:5000 movenet

> To get the API live use an Terminal/Powershell instance to run app.py, Flask will publish it to **_localhost:5000_** by default, just open your Web Browser there and it'll load shortly using your default Webcam.
