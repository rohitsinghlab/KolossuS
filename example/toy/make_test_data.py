
import torch
import numpy as np

import h5py

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

AMINO_ACIDS = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']


def main():
    n = 9
    fout_seqs = 'test.fasta'
    fout_pairs = 'pairs.txt'
    fout_embed = 'embed.h5'

    embedding_dim = 5120

    kinase_seqs = [(f'kin{i+1}', s) for i, s in enumerate(rseqs(n))]
    substrate_seqs = [(f'sub{i+1}', s) for i, s in enumerate(rseqs(n))]
    seqs = kinase_seqs + substrate_seqs
    tofasta(seqs, fout_seqs)

    pairs_out = set()
    for (a, _), (b, _) in zip(kinase_seqs, substrate_seqs):
        n = len(b)
        i = str(np.random.choice(n))
        pairs_out.add((a, b, i))
    with open(fout_pairs, 'wt') as fout:
        print('#lines starting with \'#\' are ignored', file=fout)
        print('#kinase_id\tsubstrate_id\tphosphorylation_site', file=fout)
        for pair in pairs_out:
            print('\t'.join(pair), file=fout)

    with h5py.File(fout_embed, 'w') as fout:
        for name, s in seqs:
            x = torch.Tensor([AMINO_ACIDS.index(c) for c in s] + [-100 for _ in range(embedding_dim-len(s))])
            fout[name] = x


def rseqs(n, maxlen=60, minlen=20):
    lens = (np.random.choice(range(minlen, maxlen), size=n, replace=True) + 1).tolist()
    seqs = [''.join(np.random.choice(AMINO_ACIDS, size=a, replace=True).tolist()) for a in lens]
    return seqs


def tofasta(seqs, fout, prefix=''):
    seqs = [SeqRecord(Seq(s), id=name, description='') for name, s in seqs]
    SeqIO.write(seqs, fout, 'fasta')


if __name__ == '__main__':
    main()
