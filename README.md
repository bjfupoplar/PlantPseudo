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


6. MCSCANX (git clone https://github.com/wyp1125/MCScanX.git)
Simply put MCscanX.zip into a directory and run:
###### $ unzip MCscanx.zip
###### $ cd MCScanx
###### $ make

7. exeronate (git clone https://github.com/nathanweeks/exonerate.git)
###### $ git clone https://github.com/nathanweeks/exonerate.git
###### $ cd exonerate
###### $ git checkout v2.4.0
###### $ ./configure [YOUR_CONFIGURE_OPTIONS]
###### $ make
###### $ make check
###### $ make install

8. blast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.25/)

# Installation:

Put PlantPseudo.tar.gz in any directory:

###### $tar zxf PlantPseudo.tar.gz or unzip PlantPseudo.zip

###### $cd  PlantPseudo/sample.data/

###### $unzip *.zip

###### cd  PlantPseudo/bin/


# Input data

###### You may create a separate folder within the input_data (result_data) for each species. There need to be three files for each species genomic input data

###### - rawFa: contains a file named genome.fa, which is the unmaksed genome for each species.
###### - repeatMaskedFa:  contains a file named genome_rm.fa which is  entire repeat masked genome dna sequence from that species in FASTA format;
###### - pep: contains a FASTA file for all the proteins in the species;
###### - gff: The GFF (General Feature Format) format consists of one line per feature, each containing 9 columns of data, plus optional track definition lines. The following documentation is based on the Version 3 specifications.
###### - repeatMaskedGff: if provided, the pipeline will identifty helitron-associated pseudogenes. (The file is the output of RepeatMasker, which is a gff3 format )

# Run the pipeline:

First go to the folder PlantPseudo/bin, and run with  command line in the form of: perl  pseudopipe.pl  --scriptDir [script dir] --gff [gff file] --pep [input pep dir] --rawFa [rawFa dir] --repeatMaskedFa [repeatMaskedFa dir] --fasta34Dir [fasta34 dir] --MCSDir [MCScanX dir] --repeatMaskedGff (optional) --outDir [result dir]

Examples using the sample.data is as follow:


###### (1)


###### perl pipeline.pl --scriptDir ../script --gff /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/genome.gff3 --pep /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/sample.pep --rawFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/raw.fa --repeatMaskedFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/repmasked.fa --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile pathfile.txt --repeatMaskedGff /home/pub/share_dat/ref/2_Ptrichocarpa/Ptrichocarpa.chr.fa.out --outDir /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/Pipeline/result






###### (2)


###### perl pipeline.pl --scriptDir ../script --gff /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/genome.gff3 --pep /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/sample.pep --rawFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/raw.fa --repeatMaskedFa /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/sample.data2/repmasked.fa --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile pathfile.txt --outDir /share_bio/project/working/16.12.26.Pseudogene/2_characteristics/16.software.packaged/Pipeline/result



# Output:

###### - result: the result pseudogene table 

###### The output can be found at result/final.pg.xls, given the above command line.

# Workflow description

###### (1) step1
###### script: Gff2Genepos.py
###### description: Extract gene position information from gff3 file
###### output table: Chromosome   start    end    strand       gene

###### (2)step2
###### script: fa-mask.py
###### description: masked genic regions
###### output: Repeatmasked- and genic-Masked genome sequence

###### (3)step3
###### script: exonerate
###### description: align the protein sequences to the masked genome
###### output table：Chromosome	programe	gene_partion	start	end	length	strand	.	gene

###### (4)step4
###### script: ExtractExonerateOut.py
###### description: extract the best alignment result
###### output table: Query id	Subject id	% identity	alignment length	mismatches	gap openings	q. start	q. end	s. start	s. end	e-value	bit score

###### (5)step5
###### script: ParseBlast.py
###### description: Filter the alignment result using parameter -E Evalue -I (identity) -L (match length) -P (length) -Q 1 (protein or subject for depth )
###### output table: Query id	Subject id	% identity	alignment length	mismatches	gap openings	q. start	q. end	s. start	s. end	e-value	bit score

###### (6)step6
###### script: Pseudo_step1.py
###### description: Consolidate multiple matches between the same intergenic seq-query protein pairs.
###### output table: Chromosome  [genome:start,en] [protein;start,end] [E value] strand gene

###### (7)step7
###### script: Pseudo_step2.py
###### description: Combine matches with different proteins at once to construct pseudoexons. 
###### output table: Chromosome gene [genome:start,end]  [protein;start,end]

###### (8)step8
###### script: Pseudo_step3.py
###### description: get the coordinates of pseudogenes on the subject sequences
###### output table: output table: Gene Chromosome|start-end

###### (9)step9
###### script: FastaManager.py
###### description: Extract Pseudoexon regions
###### output: Pseudoexon sequences 

###### (10)step10
###### script: BlastUtilityv2.py
###### description:  Perform realignment using tfasty software 
###### output: tfasty output

###### (11)step11
###### script: Pseudo_step4.py
###### description:  Extract tfasty output infromation
###### output: 
###### Gene Chromosome|start-end
###### >Gene_length Genome_subject_length identity% E_value Smith-Waterman_score	Smith-Waterman_%identity	Smith-Waterman_simlarity	alignment_start_end
###### seq1 (Protein sequences)
###### seq2 (Genome sequence)

###### (12)step12
###### script: CheckStrand.py
###### description:  Check the alignment orientation
###### output table: Chromosome	start end	strand	pseudogene

###### (13)step13
###### script: PolyACheck.py
###### description:  Check if there are any PolyA signal in the downsteam of pseudogene
###### output table: Chromosome start end strand pseudogene maxCount	maxPos	maxStr	signalPos	kind

###### (14)step14
###### script: CheckIntron.py
###### description:  Extract intron information from exonerate
###### output table:  exonerate output

###### (15)step15
###### script:  SumTablev2.py
###### description:  Combine the previous outputs
###### output table: pgId    pgChr   pgStart pgEnd   pgStrand        pgpolyA expect  ident   stop1   stop2   fShift1 fShift2 numofIntrons paln    pId

###### (16)step16
###### script:  GetIntronfracv2.py
###### description:  Calculate the match length ratio against the full length protein length
###### output table:  pgId    pgChr   pgStart pgEnd   pgStrand        pgpolyA expect  ident   stop1   stop2   fShift1 fShift2 numofIntrons intronPos       paln    pId     pChr    pStart  pEnd    pStrand Frac

###### (17)step17
###### script:  PgClassification.py
###### description:  Filter the pseudogene output (The match length ratio <0.05 and the pseudogene length<30 were removed)
###### output table:  pgId    pgChr   pgStart pgEnd   pgStrand        pgpolyA expect  ident   stop1   stop2   fShift1 fShift2 numofIntrons intronPos       paln    pId     pChr    pStart  pEnd    pStrand Frac

###### (18)step18
###### script:  Pggff.py,mcscanformatv2.py,Mcscan2Pglstv2.py
###### description:  Prepare for the input for MCscanX.
###### output: WGD-derived pseudogene list is generated. 

###### (19)step19
###### software: MCScanX
###### description: The WGD-derived pseudogenes were detected using MCScanX.
###### output: MCScanX output.

###### (20)step20
###### script:  FinalPglst.py
###### description:  The type of pseudogene is added to the last column.
###### output table: pgId    pgChr   pgStart pgEnd   pgStrand        pgpolyA expect  ident   stop1   stop2   fShift1 fShift2 numofIntrons intronPos       paln    pId     pChr    pStart  pEnd    pStrand Frac	DupType



# Pipeline

The pipeline consisted of five major steps: 
###### (1) identify intergenic regions (masked genic and transposon regions) with sequence similarity to known proteins using exonerate; RM-masked genomes were used to mask the genic regions (annotated transcription unit in the genome annotation) and generate a file of intergenic regions. If repeatmasked genome sequence has beeen provided, the following steps of Ψs identification focused on intergenic nonTE regions, and if not, the following steps could identify helitron-related pseudogenes. This step is to identify all the regions in the genome that share sequence similarity with any known protein, using exonerate (Slater and Birney, 2005) with parameters --model protein2genome --showquerygff no --showtargetgff yes --maxintron 5000 --showvulgar yes --ryo "%ti\t%qi\t%tS\t%qS\t%tl\t%ql\t%tab\t%tae\t%tal\t%qab\t%qae\t%qal\t%pi\n".

###### (2) conduct quality control, identity >= 20%, match length >= 30 aa, match length >= 5% of the query sequence, and only the best match is retained; In addition to the filters already included in the PseudoPipe (overlap >= 30 bp between a hit and a functional gene), we did not accept alignments with E-value >1e-5, identity < 20%, match length < 30 aa, match length (proportion aligned) < 5%. Then the best match of alignment hits was selected in places where a given chromosomal segment has multiple hits.

###### (3) link homologous segments into contigs (set I Ψs); The third step is to link pseudogene contigs based on the distance between the hits on the chromosome (Gc) and the distance on the query protein (Gq). In our workflow, these gaps Gc can arise from low complexity or very decayed regions of the pseudogene that are discarded by exonerate. We set this distance to 50 bp.

###### (4) realign using tfasty to identify features that disrupt contiguous protein sequences; The set I Ψs is realigned using a more accurate alignment program, tfasty34, with parameters “-A -m 3 –q”. Accurate sequence similarity and annotate positions of disablements (frame shifts and stop codons), as well as insertions and deletions were generated in this step.

###### (5) distinguish WGD-derived Ψs and set II Ψs. In this step, WGD-derived pseudogenes were detected using MCScanX (Wang et al., 2012) based on the DAGchainer algorithm (Haas et al., 2004) with parameters -k 50 -g -1 -s 5 -m 25, and blocks with minimum of 5 gene pairs were selected. We used protein pairs from each organism with a BLASTP E-value of less than 1e-5 and Ψ-FP pairs as the input data when running MCScanX. Pairs of Ψ-FP in the syntenic block were considered WGD derived.


# The directory tree

>--------|bin
>> ----------------|pipeline.pl
>--------|sample.data
>> ----------------|genome.gff3
>> ----------------|raw.fa
>> ----------------|Repeatmasked.gff3
>> ----------------|repmasked.fa
>> ----------------|sample.pep
>--------|script
>> ----------------|AlignPosition.py
>> ----------------|BlastUtility.py
>> ----------------|BlastUtilityv2.py
>> ----------------|blosum50.matrix
>> ----------------|CheckIntron.py
>> ----------------|CheckStrand.py
>> ----------------|DistributionGene.py
>> ----------------|ExtractExonerateOut.py
>> ----------------|fa-mask.py
>> ----------------|FastaManager.py
>> ----------------|FileUtility.py
>> ----------------|FinalPglsthelit.py
>> ----------------|FinalPglst.py
>> ----------------|GetIntronfrac_0.py
>> ----------------|GetIntronfracv2.py
>> ----------------|Gff2Genepos.py
>> ----------------|intersetoutput.py
>> ----------------|Mcscan2Pglstv2.py
>> ----------------|mcscanformatv2.py
>> ----------------|Overlap2Helilst.py
>> ----------------|overlapRegion.pl
>> ----------------|ParseBlast.py
>> ----------------|PgClassificationv2.py
>> ----------------|Pggff.py
>> ----------------|Pggffv2.py
>> ----------------|PolyACheck.py
>> ----------------|Pseudo_step1.py
>> ----------------|Pseudo_step2.py
>> ----------------|Pseudo_step3.py
>> ----------------|Pseudo_step4.py
>> ----------------|Repeat2Region.py
>> ----------------|SingleLinkage.py
>> ----------------|SumTablev2.py
>> ----------------|Translation.py
> |-------|software
>> ----------------|blast-2.2.25
>> ----------------|exonerate-2.2.0-x86_64
>> ----------------|fasta34
>> ----------------|MCScanX
> |-------|README.md
> |-------|pathfile.txt
