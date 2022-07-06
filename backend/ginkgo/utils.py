# Import Biopython tools for running local BLASTX
import asyncio
import random

from Bio.Blast.Applications import NcbiblastxCommandline
from asgiref.sync import async_to_sync
import xml.etree.ElementTree as ET


@async_to_sync
async def lambda_logic(query):
    await asyncio.sleep(3)
    cmd_blastx = NcbiblastxCommandline(cmd='blastx', outfmt=5, db='../data/db/mydb')
    stdout, stderr = cmd_blastx(stdin=query)

    # Check STDOUT, STDERR
    print("STDOUT: %s" % stdout)
    print("STDERR: %s" % stderr)

    # parse XML output
    responseXml = ET.fromstring(stdout)
    hits = responseXml.find('BlastOutput_iterations').find('Iteration').find('Iteration_hits')
    result = random.choice(hits)
    for child in result:
        print(child.tag, child.attrib)

    return stdout
