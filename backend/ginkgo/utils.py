# Import Biopython tools for running local BLASTX
import asyncio
import os
import random
import re

from Bio.Blast.Applications import NcbiblastxCommandline
from asgiref.sync import async_to_sync, sync_to_async
import xml.etree.ElementTree as ET
from .models import BlastQuery, BlastResult


@async_to_sync
async def process_query(query, sess_id):
    await asyncio.sleep(3)
    eval = 10
    input = query[:]
    # blastx 17 base minimum, extend the sequence artificially
    while len(input) <= 17:
        input += query
        eval = 1000
    utils_dir_path = os.path.dirname(os.path.realpath(__file__))
    blast_db_path = utils_dir_path + '../data/db/mydb'
    cmd_blastx = NcbiblastxCommandline(cmd='blastx', outfmt=5, db=blast_db_path,
                                       word_size=2, threshold=1, seg='no', evalue=eval)
    stdout, stderr = cmd_blastx(stdin=input)

    # Check STDOUT, STDERR
    print("STDOUT: %s" % stdout)
    print("STDERR: %s" % stderr)

    protein_info = await parse_xml(stdout)
    await complete_query(query, protein_info, sess_id)

    return stdout


@sync_to_async
def parse_xml(xml):
    # parse XML output
    protein_info = {}
    protein_name = protein_id = locus_tag = 'undef'
    hsp_bit_score = hsp_hit_from = hsp_hit_to = -1
    responseXml = ET.fromstring(xml)
    hits = responseXml.find('BlastOutput_iterations').find('Iteration').find('Iteration_hits')
    if len(hits) == 0:
        for each in ['protein_name', 'protein_id', 'locus_tag', 'hsp_bit_score', 'hsp_hit_from', 'hsp_hit_to']:
            protein_info[each] = eval(each)
        return protein_info
    result = random.choice(hits)
    prot_def = result.find('Hit_def').text
    high_scoring_pair = result.find('Hit_hsps').find('Hsp')
    m = re.search(r'\[protein=(.+?)\]', prot_def)
    if m:
        protein_name = m.group(1)
    m = re.search(r'\[protein_id=(.+?)\]', prot_def)
    if m:
        protein_id = m.group(1)
    m = re.search(r'\[locus_tag=(.+?)\]', prot_def)
    if m:
        locus_tag = m.group(1)
    hsp_bit_score = high_scoring_pair.find('Hsp_bit-score').text
    hsp_hit_from = high_scoring_pair.find('Hsp_hit-from').text
    hsp_hit_to = high_scoring_pair.find('Hsp_hit-to').text

    for each in ['protein_name', 'protein_id', 'locus_tag', 'hsp_bit_score', 'hsp_hit_from', 'hsp_hit_to']:
        protein_info[each] = eval(each)
    return protein_info


@sync_to_async
def complete_query(query, protein_info, sess_id):
    blast_query = BlastQuery.objects.filter(user_cookie=sess_id, dna_sequence=query, completed=False).latest('id')
    run_job(query, blast_query, protein_info, sess_id)

    # cleanup any leftover jobs
    while BlastQuery.objects.filter(user_cookie=sess_id, completed=False).exists():
        blast_query = BlastQuery.objects.filter(user_cookie=sess_id, completed=False).latest('id')
        run_job(query, blast_query, protein_info, sess_id)


def run_job(query, blast_query, protein_info, sess_id):
    blast_query.completed = True
    bq_pk = blast_query.id
    blast_result = BlastResult(
        user_cookie=sess_id,
        protein_name=protein_info['protein_name'],
        protein_id=protein_info['protein_id'],
        subseq_start=protein_info['hsp_hit_from'],
        subseq_end=protein_info['hsp_hit_to'],
        orig_query=blast_query,
        dna_sequence=query,
        locus_tag=protein_info['locus_tag'],
        hsp_bit_score=protein_info['hsp_bit_score']
    )
    blast_query.save(update_fields=['completed'])
    blast_result.save()
