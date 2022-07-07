FROM python:3.11

RUN apt-get update && apt-get install -y ncbi-blast+
RUN pip install -r requirements.txt
RUN cd data
RUN rm -rf db/mydb* genomes/combined_prot.fasta
RUN cat genomes/*.txt > genomes/combined_prot.fasta
RUN makeblastdb -dbtype prot -in genomes/combined_prot.fasta -out db/mydb
RUN cd ../backend
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]