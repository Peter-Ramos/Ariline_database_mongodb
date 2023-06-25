FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /Digital_airlines
RUN mkdir -p /Digital_airlines/data
COPY service.py /Digital_airlines/DigitalAirlines.py
ADD data /Digital_airlines/data
EXPOSE 5000
WORKDIR /Digital_airlines
ENTRYPOINT [ "python3","-u", "DigitalAirlines.py" ]