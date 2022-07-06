from django.db import models


# Create your models here.
class BlastQuery(models.Model):
    dna_sequence = models.CharField(max_length=270)
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class BlastResult(models.Model):
    protein_name = models.CharField(max_length=270)
    subseq_start = models.IntegerField()
    subseq_end = models.IntegerField()
    orig_query = models.ForeignKey(BlastQuery, on_delete=models.DO_NOTHING)

    def _str_(self):
        return str(self.protein_name)


# class Protein(models.Model):
#     name = models.CharField(max_length=270)