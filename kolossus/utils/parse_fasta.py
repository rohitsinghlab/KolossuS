
from Bio import SeqIO


def parse_fasta(fname, to_dict=False):
    if to_dict:
        return {r.id: str(r.seq) for r in SeqIO.parse(fname, 'fasta')}
    else:
        return [(r.id, str(r.seq)) for r in SeqIO.parse(fname, 'fasta')]

