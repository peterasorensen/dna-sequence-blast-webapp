# Data
Data pulled from NCBI database. Each data file represents the proteins contained within the corresponding genome/nucleotide. 

## Important Internal Commands

### Constructing the database
```
makeblastdb -dbtype prot -in genomes/combined_prot.fasta -out db/mydb
```

### Blast Protein Search CLI Command
```
blastx -query ./searchseq -db db/mydb -outfmt 6
```