# BASE IMAGE
FROM mariadb:10.5.8

# Me
MAINTAINER gramadin@databygram.com

# create and use folder for the image

WORKDIR .


# get requirements
COPY requirements.txt .
COPY baseball.sql .

#copy all that to the working directory
#COPY app.py ./app.py

# get and unpack the SQL file
#RUN curl https://teaching.mrsharky.com/data/baseball.sql.tar.gz \
#  | tar -xjC /tmp/package \
#  && make -C /tmp/package

# install reqs
# RUN pip install --no-cache-dir -r requirements.txt

RUN echo Please wait....
RUN docker container exec -i db-container mysql bbdb < baseball.sql -ppass
Run echo Complete


# use docker build to build image - 'docker build --tag test1 .' dot is local directory
# copy things that dont change often first. this uses cache most efficently

