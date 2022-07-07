FROM python:3.11
WORKDIR /
# Copying Entryfile
COPY entryfile /entryfile
# Pre install packages
RUN apt-get update && apt-get install -y ncbi-blast+
RUN pip install -r requirements.txt
#ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PWD /root
ENV TERM xterm
ENV HOME /root
# Expose ports
EXPOSE 3000
WORKDIR /root
# Image Entrypoint
#!/bin/bash
CMD ["cat", "data/genomes/*.txt > data/genomes/combined_prot.fasta"]
CMD ["makeblastdb", "-dbtype prot", "-in data/genomes/combined_prot.fasta", "-out data/db/mydb"]
CMD ["python3", "backend/manage.py", "makemigrations"]
CMD ["python3", "backend/manage.py", "migrate"]
CMD ["npm", "start"]
CMD ["python3", "backend/manage.py", "runserver"]
