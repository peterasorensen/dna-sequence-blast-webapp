FROM python:3.10-buster
WORKDIR /root

# add app
RUN mkdir backend/
COPY requirements.txt backend/ data/ ./backend/
# install app dependencies
RUN apt-get update && apt-get install -y ncbi-blast+
#RUN npm install react-scripts@3.4.1 -g --silent
# backend stuff
RUN pip3 install -r requirements.txt

# Expose ports
EXPOSE 8000

# Generate data
CMD ["cat", "data/genomes/*.txt > data/genomes/combined_prot.fasta"]
CMD ["makeblastdb", "-dbtype prot", "-in data/genomes/combined_prot.fasta", "-out data/db/mydb"]
CMD ["python3", "backend/manage.py", "makemigrations"]
CMD ["python3", "backend/manage.py", "migrate"]

# Start app
CMD ["python3", "backend/manage.py", "runserver"]
