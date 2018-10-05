## PlantPseudo

# Description:
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
$ cd PlantPseudo/sample.data| unzip *.zip
$ cd ../master


#Input data

You may create a separate folder within the input_data (result_data) for each species. There need to be three files for each species genomic input data

- rawFa: contains a file named genome.fa, which is the unmaksed genome for each species.
- repeatMaskedFa:  contains a file named genome_rm.fa which is  entire repeat masked genome dna sequence from that species in FASTA format;
- pep: contains a FASTA file for all the proteins in the species;
- gff: The GFF (General Feature Format) format consists of one line per feature, each containing 9 columns of data, plus optional track definition lines. The following documentation is based on the Version 3 specifications.
--repeatMaskedGff: if provided, the pipeline will identifty helitron-associated pseudogenes. (The file is the output of RepeatMasker, which is a gff3 format )

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

# Pipeline

The pipeline consisted of five major steps: 
(1) identify intergenic regions (masked genic and transposon regions) with sequence similarity to known proteins using exonerate; 
    RM-masked genomes were used to mask the genic regions (annotated transcription unit in the genome annotation) and generate a file of intergenic regions.
	If repeatmasked genome sequence has beeen provided, the following steps of Ψs identification focused on intergenic nonTE regions, and if not, the following steps could identify helitron-related pseudogenes.
	This step is to identify all the regions in the genome that share sequence similarity with any known protein, using exonerate (Slater and Birney, 2005) with parameters --model protein2genome --showquerygff no --showtargetgff yes --maxintron 5000 --showvulgar yes --ryo \"%ti\\t%qi\\t%tS\\t%qS\\t%tl\\t%ql\\t%tab\\t%tae\\t%tal\\t%qab\\t%qae\\t%qal\\t%pi\\n\". 

(2) conduct quality control, identity >= 20%, match length >= 30 aa, match length >= 5% of the query sequence, and only the best match is retained; 
    In addition to the filters already included in the PseudoPipe (overlap >= 30 bp between a hit and a functional gene), we did not accept alignments with E-value >1e-5, identity < 20%, match length < 30 aa, match length (proportion aligned) < 5%. Then the best match of alignment hits was selected in places where a given chromosomal segment has multiple hits.

(3) link homologous segments into contigs (set I Ψs); 
    The third step is to link pseudogene contigs based on the distance between the hits on the chromosome (Gc) and the distance on the query protein (Gq). In our workflow, these gaps Gc can arise from low complexity or very decayed regions of the pseudogene that are discarded by exonerate. We set this distance to 50 bp. 

(4) realign using tfasty to identify features that disrupt contiguous protein sequences; 
    The set I Ψs is realigned using a more accurate alignment program, tfasty34, with parameters “-A -m 3 –q”. Accurate sequence similarity and annotate positions of disablements (frame shifts and stop codons), as well as insertions and deletions were generated in this step.

(5) distinguish WGD-derived Ψs and set II Ψs.
    In this step, WGD-derived pseudogenes were detected using MCScanX (Wang et al., 2012) based on the DAGchainer algorithm (Haas et al., 2004) with parameters -k 50 -g -1 -s 5 -m 25, and blocks with minimum of 5 gene pairs were selected. We used protein pairs from each organism with a BLASTP E-value of less than 1e-5 and Ψ-FP pairs as the input data when running MCScanX. Pairs of Ψ-FP in the syntenic block were considered WGD derived.
