
from . import stringops
from .decorators import batch_comp_on_list
from .decorators import delay

from io import StringIO
from functools import reduce

from Bio import SeqIO
from Bio.Seq import Seq 
from Bio.SeqRecord import SeqRecord 

from Bio.Entrez import efetch
from Bio import Entrez

from urllib.error import HTTPError


def main():
    print(Entrez.email)
    seqs = {'seq1': 'aaccggtt',
            'seq2': 'aaccggt',
            'seq3': 'aaccggttt'}
    n = 4
    outfile = 'test.fasta'

    write_fasta(seqs, outfile, n)

    seqs = [('seq1', 'aaccggtt'),
            ('seq2', 'aaccggt'),
            ('seq3', 'aaccggttt')]
    n = 4
    outfile = 'test2.fasta'

    write_fasta(seqs, outfile, n)


def write_fasta(seqs, outfile, n=80):
    """
    Write sequences to fasta file. Note that we assume the order of the sequences
    is unimportant if the input passed in is a dictionary. 

    Input: 
        seqs (dict[str] -> str) OR (list[(str, str)]): a dictionary or a list of tuples (fasta header, sequence)
        outfile (str): path for output file
    """
    if isinstance(seqs, dict):
        seqs = seqs.items()
    with open(outfile, 'wt') as fout:
        for header, seq in seqs:
            print(f'>{header}', file=fout)
            print('\n'.join(stringops.chop(seq, n)), file=fout)


def fetch_seqs(db, id, rettype='fasta', retmode='text', parser=None):
    # must switch order of input in backend to accomodate batch decorator
    batches = reduce(lambda x, y: x + y, _fetch_seqs(id, db, rettype, retmode, parser))
    return {name: seq for name, seq in batches}


@batch_comp_on_list(block_size=150)
@delay(limit=0.35, time_delay=0.5)
def _fetch_seqs(id, db, rettype, retmode, parser):
    if not parser:
        if rettype == 'fasta' and retmode == 'text':
            parser = parse_entrez_fasta_output
    assert parser is not None
    try:
        seqs = efetch(db=db, id=id, rettype=rettype, retmode=retmode).read()
    except HTTPError:
        return None
    return parser(seqs)


def parse_entrez_fasta_output(s):
    ssss = '\n'.join(list(filter(lambda sss: len(sss) > 0, [ss.strip() for ss in s.split('\n')])))
    records = SeqIO.parse(StringIO(ssss), 'fasta')
    return [(r.id, str(r.seq)) for r in records]


if __name__ == '__main__': 
    main()
