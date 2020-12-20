# base image
FROM python

RUN apt update


# copy over all
COPY . /.

# command to run on container start
RUN chmod +x /final.sh
RUN ./final.sh

