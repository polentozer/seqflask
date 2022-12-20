# init a base image (Alpine is small Linux distro)
FROM python:3.9.15-slim
# update pip to minimize dependency errors
RUN pip install --upgrade pip
# define the present working directory
WORKDIR /seqflask-docker
# copy the contents into the working dir
ADD . /seqflask-docker
# run pip to install the dependencies of the app
RUN pip install -r requirements.txt
# exposing ports
EXPOSE 8080
EXPOSE 80
EXPOSE 443
# define the command to start the container
CMD ["python", "wsgi.py"]
