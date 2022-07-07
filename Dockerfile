FROM python:3.11
WORKDIR /

# install app dependencies
# react stuff
COPY frontend/package.json ./frontend/
COPY frontend/package-lock.json ./frontend/
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent
# backend stuff
RUN apt-get update && apt-get install -y ncbi-blast+
RUN pip install -r requirements.txt

# add app
COPY . ./

# Expose ports
EXPOSE 3000
WORKDIR /root

# Generate data
CMD ["cat", "data/genomes/*.txt > data/genomes/combined_prot.fasta"]
CMD ["makeblastdb", "-dbtype prot", "-in data/genomes/combined_prot.fasta", "-out data/db/mydb"]
CMD ["python3", "backend/manage.py", "makemigrations"]
CMD ["python3", "backend/manage.py", "migrate"]

# Start app
CMD ["npm", "start"]
CMD ["python3", "backend/manage.py", "runserver"]
