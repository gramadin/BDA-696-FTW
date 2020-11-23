# BASE IMAGE
FROM python:3.9.0

# create and use folder for the image
WORKDIR /code

# define port to use to communicate with environment variables
ENV PORT 5000

# Get files to create image and indicate where to put them
COPY app.py /code/app.py

#bash commands - must be in correct format for OS/CLI on users system
RUN pip install flask

# copy indicated files from local folder into the image - use docker.ignore to prevent undsired files from being copied
COPY . /code

# run image as a container [what to run, what to pass]
CMD ["python", "app.py"]




# use docker build to build image - 'docker build --tag test1 .' dot is local directory