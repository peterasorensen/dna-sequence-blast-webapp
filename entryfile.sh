#!/bin/bash
# Generate data
cat data/genomes/*.txt > data/genomes/combined_prot.fasta
makeblastdb -dbtype prot -in data/genomes/combined_prot.fasta -out data/db/mydb
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate --noinput

# Start app
python3 backend/manage.py runserver