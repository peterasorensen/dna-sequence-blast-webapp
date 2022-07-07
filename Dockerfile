FROM python:3.10-buster

# add app
RUN mkdir /root/blast_app/
WORKDIR /root/blast_app/
COPY requirements.txt entryfile.sh ./
COPY backend/ ./backend
COPY data/ ./data
# install app dependencies
RUN apt-get update && apt-get install -y ncbi-blast+
# backend stuff
RUN pip3 install -r requirements.txt

# Add env variables
ENV SECRET_KEY=$SECRET_KEY

# Expose ports
EXPOSE 8000

# Entryfile
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
