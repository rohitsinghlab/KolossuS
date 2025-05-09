# KolossuS: Kinase Signaling Prediction Tool

Deconvolving the substrates of hundreds of kinases linked to phosphorylation networks driving
cellular behavior is a fundamental, unresolved biological challenge, largely due to the poorly
understood interplay of kinase selectivity and substrate proximity. We introduce KolossuS, a
deep learning framework leveraging protein language models to decode kinase-substrate
specificity. KolossuS achieves superior prediction accuracy and sensitivity across mammalian
kinomes, enabling proteome-wide predictions and evolutionary insights. By integrating
KolossuS with CRISPR-based proximity proteomics in vivo, we capture kinase-substrate
recognition and spatial context, obviating prior limitations. We show this combined framework
identifies kinase substrates associated with physiological states such as sleep, revealing both
known and novel Sik3 substrates during sleep deprivation. This novel integrated
computational-experimental approach promises to transform systematic investigations of
kinase signaling in health and disease.


## Preprint
**Jha K., Shonai D., Parekh A., Uezu A., Fujiyama T., Yamamoto H., Parameswaran P., Yanagisawa M., Singh R., Soderling S. (2025). Deep Learning-coupled Proximity Proteomics to Deconvolve Kinase Signaling In Vivo. bioRxiv, 2025-04. [bioRxiv preprint](https://www.biorxiv.org/content/10.1101/2025.04.27.650849v1)**


Main function you would use is `kolossus`. Function works as follows: 

```
Input:
  - fasta file of all sequences (or .h5 file of embeddings)
  - pair file of format '<kinase_id>\t<substrate_id>\t<substrate_phosphorylation_site>'

Output:
  - pairs (kinase_id, substrate_id, substrate_phosphorylation_site, predicted_probability)
```

Over here, `<substrate_phosphorylation_site>` is the offset of the phosphorylated residue. 
So for example, if the substrate has sequence 'GGRGSDD', and the serine (5th amino acid)
is the phosphorylated residue, then `substrate_phosphorylation_site=5`.

Note that the fasta file should contain **all** of the sequences (including the full substrate sequences). 
We'll get the appropriate windows from the pairs file. 

Usage:

``` python
## on the command line
kinase_file="kinases.fasta"
substrate_file="substrates.fasta"

cat $kinase_file $substrate_file > seqs.fasta

## in python
from kolossus import kolossus

# define inputs to function
seqs_file = 'seqs.fasta' 
pairs_file = 'pairs_with_phosphorylation_sites.txt'

# returns a dictionary (kinase, substrate, site): probability
pairs_and_probs = kolossus(pairs_file, fseqs=seqs_file, device='cpu')

# to get kolossus embeddings: use the return_projections parameter
pairs_and_probs, projections = kolossus(pairs_file, fseqs=seqs_file, device='cpu', return_projections=True)
```

There is also a command-line interface which can be called on the terminal: `kolossus-cli`.

```
usage: kolossus-cli [-h] --pairs PAIRS [--seqs SEQS] [--embeddings EMBEDDINGS] [--dtype DTYPE] [--projections PROJECTIONS]
                    [--device DEVICE] [--batch_size BATCH_SIZE] -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --pairs PAIRS         format: <kinase_id> <substrate_id> <substrate_phosphorylation_site>
  --seqs SEQS           fasta formatted file of sequences, either seqs or embeddings must be provided
  --embeddings EMBEDDINGS
                        h5 file of sequence embeddings, either seqs or embeddings must be provided
  --dtype DTYPE         data type of sequence embeddings (usually float32)
  --projections PROJECTIONS
                        name of .h5 files for kolossus projections
  --device DEVICE       default device on which to run model
  --batch_size BATCH_SIZE
                        Number of pairs at a time on which to run model
  -o OUTPUT, --output OUTPUT
                        desired file path for output
```

To get esm embeddings, you can use the `kolossus-extract` command. 

```
usage: kolossus-extract [-h] -i I [--model MODEL] [--device DEVICE] -o O

optional arguments:
  -h, --help       show this help message and exit
  -i I             name of input fasta file
  --model MODEL    name of model to extract embeddings
  --device DEVICE  cpu or gpu device to use
  -o O             name of output .h5 file
```
