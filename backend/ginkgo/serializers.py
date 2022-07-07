from rest_framework import serializers

from ginkgo.models import BlastQuery, BlastResult


class BlastQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlastQuery
        fields = ('dna_sequence', 'title', 'description', 'completed')


class BlastResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlastResult
        fields = ('protein_name', 'protein_id', 'subseq_start', 'subseq_end', 'orig_query', 'dna_sequence', 'locus_tag', 'hsp_bit_score')
