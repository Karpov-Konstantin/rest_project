# base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 8080

# run the application
#CMD ["python", "./manage.py", "runserver", "0.0.0.0:8080"]
#CMD sleep 1d