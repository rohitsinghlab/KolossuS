
import kolossus

# set batch size for how many pairs to run model on at a time
kolossus.set_batch_size(3)


ffasta = 'test.fasta'
fembeds = 'embed.h5'
fpairs = 'pairs.txt'


print(kolossus.kolossus(fpairs, fseqs=ffasta))

print('-' * 40)

print(kolossus.kolossus(fpairs, fembeds=fembeds))
