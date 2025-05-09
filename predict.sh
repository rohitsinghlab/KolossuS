echo Job Name: predict


## extract embeddings
kolossus-extract -i <seqs.fasta> --device cuda -o <seq_embeddings.h5> 

## predict w command line arg
kolossus-cli --pairs <pairs.txt>  --embeddings <seq_embeddings.h5>  --device cuda -o <preds.txt>
