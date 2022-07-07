FROM python:3.10-buster

# add app
RUN mkdir /root/blast_app/
WORKDIR /root/blast_app/
COPY requirements.txt ./
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

# Generate data
CMD ["cat", "data/genomes/*.txt > data/genomes/combined_prot.fasta"]
CMD ["makeblastdb", "-dbtype prot", "-in data/genomes/combined_prot.fasta", "-out data/db/mydb"]
CMD ["python3", "backend/manage.py", "makemigrations"]
CMD ["python3", "backend/manage.py", "migrate"]

# Start app
CMD ["python3", "backend/manage.py", "runserver"]
