This repo contains many functions I've found useful and used over and over and got tired of writing over and over again. Mostly in python. 

For now, one can import functions by 
``` bash
git clone https://github.com/aprkh/aprkh_utils.git  # or however you import git repos
```
Then in python:
``` python
import sys
sys.path.append('/path/to/parent/directory/of/aprkh_utils')
```


# Examples below. 

Table of amino acids. Useful 
``` python
# keys are codons, values are amino acids, '*' for termination
from aprkh_utils.misc import CODON_TABLE
AMINO_ACIDS = [aa for aa in CODON_TABLE.values() if aa != '*']
```

Utility functions to retrieve protein/nucleotide sequences from NCBI Entrez and write to fasta. Wrapper around `Bio.Entrez.efetch`
and `Bio.SeqIO.write`. 
``` python
from aprkh_utils.seqio import fetch_seqs
from aprkh_utils.seqio import write_fasta

# names of two protein sequences
seq_ids = ['NP_001361173.1', 'NP_001341538.1']

# fetch sequences
seqs = fetch_seqs(db='protein', id=seq_ids)
```

Returned object is a dictionary mapping `name -> seq`. To save to a file `out.fasta`:
``` python
write_fasta(seq, 'out.fasta')
```

# Useful decorators

## Timing function execution. 
Use the `fn_timer` as a decorator. Useful for code profiling.

Example: timing how long it takes to construct a certain number of random protein sequences.
``` python
# keys are codons, values are amino acids, '*' for termination
from aprkh_utils.misc import CODON_TABLE
AMINO_ACIDS = [aa for aa in CODON_TABLE.values() if aa != '*']

from aprkh_utils.decorators import fn_timer
import numpy as np

@fn_timer
def random_protein(n, L):
    """
    Makes n random proteins of size L.
    """
    seqs = {}
    for _ in range(n):
        # random name 
        name = 'NP_' + ''.join(map(str, np.random.choice(10, size=10, replace=True)))
        # random sequence
        seq = ''.join(map(lambda i: AMINO_ACIDS[i], np.random.choice(len(AMINO_ACIDS), size=L, replace=True)))
        # save sequence
        seqs[name] = seq
    return seqs

# make various numbers of random proteins of length 1000
random_protein(10, 1000)
random_protein(100, 1000)
random_protein(1000, 1000)
random_protein(10000, 1000)
random_protein(100000, 1000)
```

The output will be:
```
random_protein took 0.001 seconds to run.
random_protein took 0.010 seconds to run.
random_protein took 0.096 seconds to run.
random_protein took 0.963 seconds to run.
random_protein took 9.544 seconds to run.
```

## Delay between function calls
Useful for when we have to limit rates of a function call, e.g. if we're querying from a website but we can't make too many calls/second
otherwise we get banned. But we don't want to delay in cases where it's been a while since we've made the call to the function.  

Use the `@delay(limit, time_delay)` decorator. Here `limit` is the minimum number of time we need to wait between calls, and `time_delay` is the
amount of time we'll wait if try to call the function again too soon. 

Example: we only want to call the function `foo` at most once per second. 

``` python
@delay(limit=1.0, time_delay=1.0)
def foo():
    print("hello, world")

# will delay 1 second between each call
for i in range(3):
    foo()
```

However, if `foo` takes longer than one second to run, then won't wait before calling it again. 

### Example: Querying from NCBI Database
A good example of when this is useful is querying data from NCBI using the Entrez utility, which has a limit of 3 queries/second. 

Most obvious solution would be to simply use `time.sleep(DELAY)` between each query:

``` python
# script to fetch and process some protein sequences
from Bio.Entrez import efetch
import time

def fetch_seq(accession, **kwargs):
    # might be invalid accession
    try:
        seq = efetch(id=accession, **kwargs).read()
    except:
        return None
    return seq

# fetch and process sequences 
accessions = ['NP_001361173.1', 'NP_001341538.1', ...]
for accession in accessions:
    seq = fetch_seq(accession, db='protein', retmode='text', rettype='fasta') 
    if seq is not None:
        ...
    time.sleep(1)
```

But sometimes, this will make our code unnecessarily slow, especially if we have to do some processing between each step:
``` python 
# fetch and process accessions
accessions = ['NP_001361173.1', 'NP_001341538.1', ...]
for accession in accessions:
    seq = fetch_seq(accession, db='protein', retmode='text', rettype='fasta')
    if seq is not None:
        # might take a long time (e.g., long protein sequence), in which case no reason to sleep
        # but might also not take that long (e.g., short protein sequence), in which case we'd want to sleep. 
    time.sleep(1)
```

In this case, we could remove the `time.sleep` argument. But sometimes, the amount of time for processing will vary based on the sequence. 

If we simply want to ensure we don't want to make too many calls per second, we can use the `delay` decorator. 

``` python
from aprkh_utils.decorators import delay

# limit is 3 calls/second, so ensure at most 1 call/0.35 seconds to be safe
@delay(limit=0.35, time_delay=0.35)
def fetch_seq(accession, **kwargs):
    seq = efetch(id=accession, **kwargs)
    ...
```

Note that this utility is already implemented in `aprkh_utils.seqio`. 

## Batching operations 

Sometimes we only want to process chunks of data at a time, perhaps because we have to create intermediate objects when processing 
that make it too memory intensive to process the entire data at a time. 

If we can run the calculation on each row of the data (first dimension) independently (e.g., if each row is an independent observation
and we're trying to calculate some statistic), but we still want to vectorize computations (i.e., running a for loop over each observation too 
expensive), we can simply break the data into blocks and operate on each block independently. 

Use the `@batch_comp_on_list(BLOCK_SIZE)` decorator in this case. Example:

``` python
from aprkh_utils.decorators import batch_comp_on_list

@batch_comp_on_list(block_size=100)    
def process_list(A):
    create very large intermediate object
    calculate output
    return output

# also works with numpy arrays and tensors
A = [list of data]

# will split A into blocks and compute independently on each block
process_list(A)
```

### Contrived toy example: 
``` python
import numpy as np
A = np.array([1, 2, 3, 4, 5, 6, 8, 9, 10])

def add_one(A):
    if len(A) > 5:
        print("ERROR!!!"); exit()
    return A + 1

# will crash
result = add_one(A)
```

To fix: 
``` python
import numpy as np
A = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10})

@batch_comp_on_list(block_size=5)
def add_one(A):
    if len(A) > 5:
        print("ERROR!!!"); exit()
    return A + 1

# now works, output is a list of results over each block
result = add_one(A)
```

To reduce to what we'd get if we'd simply operated on `A` in one go:
``` python
from functools import reduce
result = reduce(np.append, add_one(A))
```

### A more useful example (also an example of stacking decorators)
The `efetch` utility allows us to retrieve multiple sequences with each query, but only up to about 200 at a time. In this case, we can 
combine the functionalities of the `delay` and `batch_comp_on_list` decorators if we have to query 1000's of sequences.

``` python
@batch_comp_on_list(block_size=150)  # query 150 sequences at a time
@delay(limit=0.35, time_delay=0.35)  # ensure not too many calls/second
def fetch_seqs(accession_list):
    try:
        seq = efetch(id=accession_list, **kwargs).read()
    except:
        return None
    return seq

accession_list = ['NP_001361173.1', 'NP_001341538.1', ...] # 1000s of sequences
seqs = fetch_seqs(accession_list)
```

Note, again, that this utility is already implemented (with the batching and delaying functionality) in `aprkh_utils.seqio`. 
