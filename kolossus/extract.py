
from .utils.seq_to_embedding import extract_embeddings_from_fasta
from .utils.seq_to_embedding import extract_embeddings_from_fasta_individual

import argparse
import sys 
import pathlib
import os 

ESM_TRANSFORMER_LAYERS = {
        "esm2_t6_8M_UR50D": 6,
        "esm2_t12_35M_UR50D": 12,
        "esm2_t30_150M_UR50D": 30,
        "esm2_t33_650M_UR50D": 33,
        "esm2_t36_3B_UR50D": 36,
        "esm2_t48_15B_UR50D": 48
}


def main():
    args = parse_args()
    
    fasta_file = args.i
    model_name = args.model
    device = args.device
    output_file = args.o

    layer = ESM_TRANSFORMER_LAYERS.get(model_name, None)
    if not layer:
        print(f"Error: illegal model name: {model_name}", file=sys.stderr)
        print("Must be one of:", ESM_TRANSFORMER_LAYERS.keys(), file=sys.stderr)
        sys.exit(1)

    if args.individual:
        extract_embeddings_from_fasta_individual(fasta_file, output_file, device, model_name,
                                                 repr_layers=[layer], layer_to_use=layer)
    else:
        extract_embeddings_from_fasta(fasta_file, output_file, device, model_name,
                                      repr_layers=[layer], layer_to_use=layer)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='name of input fasta file')
    parser.add_argument('--model', type=str, default='esm2_t48_15B_UR50D', help='name of model to extract embeddings')
    parser.add_argument('--device', type=str, default='cpu', help='cpu or gpu device to use')
    parser.add_argument('--individual', action='store_true', default=False, help='flag to indicate whether or not to store individual sequences')
    parser.add_argument('-o', type=str, required=True, help='name of output .h5 file (or output directory if --individual is true)')
    args = parser.parse_args()
    return args 


if __name__ == '__main__':
    main()
