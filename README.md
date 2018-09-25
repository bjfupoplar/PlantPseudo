## PlantPseudo
Pseudogenes are important resources in understanding the evolutionary history of genes and genomes.This pseudogene pipeline was used for pseudogene identification in plant species. 

# Usage:
This software provides a pipeline for identification pseudogenes in plant species, and it has an advantage in identification whole genome duplication (WGD)-derived pseudogenes, 
tandem duplicated pseudogenes, and helitron-related pseudogenes. It takes the predicted whole duplication blocks from mcscan and then report their close functional paralogs (FPs), 
math coverage of FPs, math identity, math expect,  poly(A) signals, and WGD-derived pseudogenes, tandem duplicated, helitron-related pseudogenes.


# Requirements:

Note:
PlantPseudo currently will only run on linux or cygwin platform, as it is dependent on GNU function.

1. python (2.7 or later, not 3; https://www.python.org/downloads/)
2. perl (v5.16.3 or later; https://www.activestate.com/activeperl/downloads)
3. Scripts in the _pipeline_scripts folder
4. tfasty (part of the FASTA package; ftp://ftp.ebi.ac.uk/pub/software/unix/fasta/fasta3/)
5. blast(version 2.2.25)

simply type:
make -f Makefile.os_x all

6. MCSCANX (git https://github.com/wyp1125/MCScanX.git)
Simply put MCscanX.zip into a directory and run:
$ unzip MCscanx.zip
$ cd MCScanx
$ make

7. exeronate (git https://github.com/nathanweeks/exonerate.git)
$ git clone https://github.com/nathanweeks/exonerate.git
$ cd exonerate
$ git checkout v2.4.0
$ ./configure [YOUR_CONFIGURE_OPTIONS]
$ make
$ make check
$ make install

8. blast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.25/)

# Installation:

Put PlantPseudo.tar.gz in any directory:

$ tar zxf PlantPseudo.tar.gz or unzip PlantPseudo.zip

$ cd  PlantPseudo/sample.data/

$ unzip *.zip

$ cd  PlantPseudo/bin/


# Input data

You may create a separate folder within the input_data (result_data) for each species. There need to be three files for each species genomic input data

- rawFa: contains a file named genome.fa, which is the unmaksed genome for each species.
- repeatMaskedFa:  contains a file named genome_rm.fa which is  entire repeat masked genome dna sequence from that species in FASTA format;
- pep: contains a FASTA file for all the proteins in the species;
- gff: The GFF (General Feature Format) format consists of one line per feature, each containing 9 columns of data, plus optional track definition lines. The following documentation is based on the Version 3 specifications.
- repeatMaskedGff: if provided, the pipeline will identifty helitron-associated pseudogenes. (The file is the output of RepeatMasker, which is a gff3 format )

# Run the pipeline:

First go to the folder PlantPseudo/bin, and run with  command line in the form of: perl  pseudopipe.pl  --scriptDir [script dir] --gff [gff file] --pep [input pep dir] --rawFa [rawFa dir] --repeatMaskedFa [repeatMaskedFa dir] --fasta34Dir [fasta34 dir] --MCSDir [MCScanX dir] --repeatMaskedGff (optional) --outDir [result dir]

Examples using the sample.data is as follow:
(1)
perl pipeline.pl --scriptDir ../script --gff /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/genome.gff3 --pep /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/sample.pep --rawFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/raw.fa --repeatMaskedFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/repmasked.fa --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/Pipeline/dirfile --repeatMaskedGff /home/pub/share_dat/ref/2_Ptrichocarpa/Ptrichocarpa.chr.fa.out --outDir /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/Pipeline/result
(2)
perl pipeline.pl --scriptDir ../script --gff /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/genome.gff3 --pep /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/sample.pep --rawFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/raw.fa --repeatMaskedFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/repmasked.fa --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/Pipeline/dirfile --outDir /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/Pipeline/result

# Output:

- result: the result pseudogene table 

===
The output can be found at result/final.pg.xls, given the above command line.

