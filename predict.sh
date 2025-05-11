echo Job Name: predict

## predict w command line (seqs)
kolossus-cli --pairs <pairs.txt>  --seqs <seqs.fasta>  --device cuda -o <preds.txt>

## extract embeddings
kolossus-extract -i <seqs.fasta> --device cuda -o <seq_embeddings.h5> 

## predict w command line (embeddings)
kolossus-cli --pairs <pairs.txt>  --embeddings <seq_embeddings.h5>  --device cuda -o <preds.txt>
