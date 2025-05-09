
from .kolossus import BATCH_SIZE
from .kolossus import set_batch_size
from .kolossus import run_kolossus

from .utils import read_sequences
from .utils import read_pairs 
from .utils import read_embeddings
from .utils import convert_data_seqs_to_embeddings

from .aprkh_utils.seqio import fetch_seqs

from Bio import Entrez
Entrez.email = "aditya.parekh@duke.edu"

import argparse
import sys 
import h5py

from functools import reduce
from collections import defaultdict


def main():
    args = parse_args()

    if args['batch_size']:
        print(f"setting batch size to {args['batch_size']}...", end=' ')
        set_batch_size(args['batch_size'])
        print("done!")

    # now fetch sequences 
    if args['db']:
        seqs = read_sequences(args['db'], to_dict=True)
    else:
        sub_ids = set()
        with open(args['fsubs'], 'rt') as f:
            for line in f:
                sub_ids.add(line.split()[0])
        seqs = build_db(sub_ids)

    print("parsing data")
    pairs, embeddings = combine_inputs(args['fkins'], args['fsubs'], args['device'], seqs)

    print("running model...", end=' ')
    results = run_kolossus(pairs, embeds=embeddings, **args['kolossus'])
    print("done!")

    output_results(results, **args['output'])


def combine_inputs(fkins, fsubs, device, seqs):
    sequences = {}
    embeddings = {}
    pairs = []
    # parse kinases
    if fkins.endswith('.h5'):
        embeddings.update(read_embeddings(fkins, device))
    else:
        sequences.update(read_sequences(fkins, to_dict=True))

    # parse substrates
    kinase_keys = set(embeddings.keys()).union(sequences.keys())
    subs_to_site = defaultdict(list)
    with open(fsubs, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue 

            #substrate_id, psites = line.split()
            split = line.split()
            substrate_id = split[0]
            # handle either comma or space-separated psites
            psites = []
            for psite in split[1:]:
                psites.extend([int(s.strip()) for s in psite.split(',')])

            subs_to_site[substrate_id].extend(psites)

    # make pairs 
    for sid in subs_to_site.keys():
        if sid not in seqs.keys(): 
            print("WARNING: invalid sequence id:", substrate_id, file=sys.stderr)
            continue

        # add pairs 
        for key in kinase_keys:
            for psite in subs_to_site[sid]:
                pairs.append((key, sid, psite))

        # add sequence 
        sequences[sid] = seqs[sid]

    pairs, embeds2 = convert_data_seqs_to_embeddings(sequences, pairs, device, testing=False)
    embeddings.update(embeds2)

    return pairs, embeddings


def output_results(results, dists_fname_out, projections_fname_out):
    if projections_fname_out:
        results, projections = results
        print("writing embeddings to:", projections_fname_out)
        with h5py.File(projections_fname_out, 'w') as fout:
            for _id, e in projections.items():
                fout[_id] = e

    print("writing predictions to", dists_fname_out)
    with open(dists_fname_out, 'wt') as fout:
        print('#kinase\tsubstrate\tpredicted_prob', file=fout)
        for pair, prob in results.items():
            pair = tuple(map(str, pair))
            prob = str(prob)
            print('\t'.join((*pair, prob)), file=fout)


def build_db(sub_ids):
    out = {}
    for sid in sub_ids:
        seq = fetch_seqs('protein', [sid])
        if seq:
            out[sid] = list(seq.values())[0]

    return out
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--substrates', type=str, required=True, 
                        help="format: \t<substrate_id>\t<psite1>,<psite2>,...")
    parser.add_argument('-k', '--kinases', type=str, required=True, 
                        help='kinase sequences either seqs or embeddings (.h5) must be provided')
    parser.add_argument('--db', type=str, default=None, 
                        help='database of substrate sequences, in fasta format')
    parser.add_argument('--dtype', type=str, default='', 
                        help='data type of sequence embeddings (usually float32)')
    parser.add_argument('-r', '--projections', type=str, default='', 
                        help='name of .h5 files for kolossus projections')
    parser.add_argument('-d', '--device', type=str, default='cpu', 
                        help='default device on which to run model')
    parser.add_argument('--batch_size', type=int, default=None, 
                        help='Number of pairs at a time on which to run model')
    parser.add_argument('-o', '--output', type=str, required=True, 
                        help='desired file path for output')

    args = parser.parse_args()

    real_args = {'kolossus': {'dtype': args.dtype,
                              'device': int(args.device) if args.device.isdigit() else args.device,
                              'return_projections': len(args.projections) > 0},
                 'fsubs': args.substrates,
                 'fkins': args.kinases,
                 'db': args.db,
                 'device': int(args.device) if args.device.isdigit() else args.device,
                 'dtype': args.dtype,
                 'batch_size': args.batch_size,
                 'output': {'dists_fname_out': args.output,
                            'projections_fname_out': args.projections if len(args.projections) > 0 else None}}
    
    return real_args    


if __name__ == '__main__':
    main(args)
