#!/usr/bin/perl -w
#Author: jianbo xie

#====version 3.0====
#
use strict;
use warnings;
use Getopt::Long;
use File::Basename;

my %opts=qw();
GetOptions(\%opts,"scriptDir:s","gff:s","pep:s","rawFa:s","repeatMaskedFa:s","lncrna:s","eValueE:i","idenThresh:i","lenThresh:i","proThresh:f","qs:i","mLenPse:i","mLenIntron:i","dirFile:s","repeatMaskedGff:s","outDir:s","help|h!");

my @usage=qq(
============================= Plant pseudogene analysis pipeline  ============================

                                             Version 1.2

Usage: PlantPseudo_v1.2 [Options]

Options:
	--scriptDir				Directory of the scripts
	--gff					Input GFF file, example: pt.gff or pt.gff3, where pt is a short name for Ptrichocarpa
	--pep					Input protein file
	--rawFa					Raw whole genome sequence file in fasta format
	--repeatMaskedFa		Repeat masked genome sequence in fasta format
	--lncrna				A file in gff/gff3 format providing lncRNA position
	--eValueE				Evalue threshold in -log(e) [Default: -1].
	--idenThresh			Identity threshold in % [Default: 95].
	--lenThresh				Length threshold [Default: 150].
	--proThresh				Threshold for the proportion of match length vs sequence length [Default: 0.9].
	--qs					For match length vs. sequence length comparison, use both query & subject [0], query only [1], or subject only [2].
	--mLenPse				The max gap size for linking pseudoexons [Default: 50]
	--mLenIntron			The max size for intron length [Default: 50]
	--dirFile				The path file contains the absolute paths of fasta34, MCScanX, blastall and exonerate sequentially
	--repeatMaskedGff		Repeat masked gene file in gff format
	--outDir				Result output directory
	--h or help				Display this message
);


my $scriptdir;
my $gff;
my $pep;
my $rfa;
my $rmfa;
my $ev;
my $identh;
my $lenth;
my $pepth;
my $qs;
my $mlp;
my $mli;
my $dirf;
my $fastadir;
my $mcscanxdir;
my $blastadir;
my $exoneratedir;
my $outdir;
my $spe = "temp";
my $new_pep;
my $file;

if ((scalar(keys %opts) == 0) or (exists($opts{"help"})) or (exists($opts{"h"}))) {
	print join("\n",@usage)."\n";
	exit;
}

if (exists $opts{"scriptDir"}) {
	$scriptdir = $opts{"scriptDir"};
	$scriptdir =~ s/\/$//;
} else {
	die "Please input the directory of the scripts!!!\n";
}

if (exists $opts{"gff"}) {
	$gff = $opts{"gff"};
	unless ($gff =~ /\.gff3?$/) {
		die "$gff is an illegal file name!!!\n";
	}
} else {
	die "Please input the GFF file!!!\n";
}

if (exists $opts{"rawFa"}) {
	$rfa = $opts{"rawFa"};
	unless ($rfa =~ /\.fa$/) {
		die "$rfa is an illegal file name!!!\n";
	}
} else {
	die "Please input the raw whole genome sequence file in fasta format!!!\n";
}

if (exists $opts{"repeatMaskedFa"}) {
	$rmfa = $opts{"repeatMaskedFa"};
	unless ($rmfa =~ /\.fa$/) {
		die "$rmfa is an illegal file name!!!\n";
	}
} else {
	die "Please input the repeat masked genome sequence file in fasta format!!!\n";
}

if (exists $opts{"pep"}) {
	$pep = $opts{"pep"};
} else {
	die "Please input the protein file!!!\n";
}

if (exists $opts{"eValueE"}) {
	$ev = $opts{"eValueE"};
} else {
	die "Please input the evalue threshold in -log(e)!!!\n";
}

if (exists $opts{"idenThresh"}) {
	$identh = $opts{"idenThresh"};
	die "The identity threshold should be an a value between 0 and 100!!!" unless $identh >=0 and $identh <= 100;
} else {
	die "Please input the identity threshold in %!!!\n";
}

if (exists $opts{"lenThresh"}) {
	$lenth = $opts{"lenThresh"};
	die "The length threshold should be an a value > 0!!!" unless $lenth > 0;
} else {
	die "Please input the length threshold!!!\n";
}

if (exists $opts{"proThresh"}) {
	$pepth = $opts{"proThresh"};
	die "The threshold for the proportion of match length vs sequence length should be between 0 and 1!!!" unless $pepth >= 0 and $pepth <= 1;
} else {
	die "Please input the threshold for the proportion of match length vs sequence length!!!\n";
}

if (exists $opts{"qs"}) {
	$qs = $opts{"qs"};
	die "Please input 0, 1 or 2!!!" unless $lenth =~ /[012]/;
} else {
	die "Please input 0, 1 or 2!!!\n";
}

if (exists $opts{"mLenPse"}) {
	$mlp = $opts{"mLenPse"};
	die "The max gap size for linking pseudoexons should be between 50 and 500!!!" unless $mlp >= 50 and $mlp <= 500;
} else {
	die "Please input the max gap size for linking pseudoexons!!!\n";
}

if (exists $opts{"mLenIntron"}) {
	$mli = $opts{"mLenIntron"};
	die "The max size for intron length should be between 50 and 500!!!" unless $mli >= 50 and $mli <= 500;
} else {
	die "Please input the max size for intron length!!!\n";
}

if (exists $opts{"dirFile"}) {
	$dirf = $opts{"dirFile"};
	open A, "$dirf" or die "can't open file $dirf: $!";
	my $line = <A>;
	$line =~ s/\s+$//;
	$line =~ s/\/$//;
	$fastadir = $line;
	$line = <A>;
	$line =~ s/\s+$//;
	$line =~ s/\/$//;
	$mcscanxdir = $line;
	$line = <A>;
	$line =~ s/\s+$//;
	$line =~ s/\/$//;
	$blastadir = $line;
	$line = <A>;
	$line =~ s/\s+$//;
	$line =~ s/\/$//;
	$exoneratedir = $line;
	close A;
} else {
	die "Please input the path file containing the absolute paths of fasta34, MCScanX, blastall and exonerate sequentially!!!\n";
}

if (exists $opts{"outDir"}) {
	$outdir = $opts{"outDir"};
	$outdir =~ s/\/$//;
} else {
	die "Please input the result output directory!!!\n";
}


system("date");
system("echo change working directory to $outdir");
chdir "$outdir" or die "can't change to directory: $outdir";

system("date");
system("echo Gff2Genepos.py");
system("python $scriptdir/Gff2Genepos.py $gff gene.pos");
system("cut -f1,2,3 gene.pos >gene.regions");

system("date");
system("cut -f1,2,3 gene.pos >masked.region");


system("date");
system("echo fa-mask.py");
#system("python $scriptdir/fa-mask.py --regions gene.pos $rmfa > $spe.rep.gene.masked.fa");

goto L if exists $opts{"repeatMaskedGff"};

############################################### if repeatMaskedGff is not provided ##########################################################

system("python $scriptdir/fa-mask.py --regions masked.region $rmfa > $spe.rep.gene.masked.fa");

system("date");
#system("exonerate");
system("$exoneratedir/exonerate --model protein2genome --showquerygff no --showtargetgff yes --maxintron 5000 --showvulgar yes --ryo \"%ti\\t%qi\\t%tS\\t%qS\\t%tl\\t%ql\\t%tab\\t%tae\\t%tal\\t%qab\\t%qae\\t%qal\\t%pi\\n\" $pep $spe.rep.gene.masked.fa > exonerate.out");

system("date");
system("echo ExtractExonerateOut.py");
system("python $scriptdir/ExtractExonerateOut.py exonerate.out exonerate.blast");

system("date");
system("echo ParseBlast.py");
system("python $scriptdir/ParseBlast.py -f get_qualified4 -blast exonerate.blast -fasta $pep -E $ev -I $identh -L $lenth -P $pepth -Q 1");

system("date");
system("rm -rf q") if -s "q";

system("date");
system("echo create soft link");
$new_pep = $pepth * 100;
$file = "exonerate.blast_E".$ev."I".$identh."L".$lenth."P".$new_pep."Q1.qlines";
system("ln -s $file q");

system("date");
system("echo Pseudo_step1.py");
system("python $scriptdir/Pseudo_step1.py q $mlp");

system("date");
system("echo Pseudo_step2.py");
system("python $scriptdir/Pseudo_step2.py q_G$mlp.PE $mli");

system("date");
system("echo Pseudo_step3.py");
system("python $scriptdir/Pseudo_step3.py q_G$mlp.PE_I$mli.PS1");

system("date");
system("echo FastaManager.py");
system("python $scriptdir/FastaManager.py -f get_stretch4 -fasta $rfa  -coords q_G$mlp.PE_I$mli.PS1.subj_coord");

system("date");
system("echo BlastUtilityv2.py");
system("python $scriptdir/BlastUtilityv2.py -f batch_sw -p tfasty34 -g q_G$mlp.PE_I$mli.PS1.pairs -i $pep -j q_G$mlp.PE_I$mli.PS1.subj_coord.fa -bdir $fastadir -d 1"); #/home/pub/share_soft/fasta34

system("date");
system("echo Pseudo_step4.py");
system("python $scriptdir/Pseudo_step4.py $scriptdir/blosum50.matrix q_G$mlp.PE_I$mli.PS1.pairs.sw.out");

system("date");
system("echo CheckStrand.py");
system("python $scriptdir/CheckStrand.py q_G$mlp.PE_I$mli.PS1.pairs.sw.raw q_G$mlp.PE_I$mli.PS1.subj_coord q_G$mlp.PE_I$mli.PS1.subj_coord.Strd");

system("date");
system("echo PolyACheck.py");
system("python $scriptdir/PolyACheck.py $rfa q_G$mlp.PE_I$mli.PS1.subj_coord.Strd q_G$mlp.PE_I$mli.PS1.subj_coord.PolyA");

system("date");
system("echo CheckIntron.py");
system("python $scriptdir/CheckIntron.py q_G$mlp.PE_I$mli.PS1.pairs $pep q_G$mlp.PE_I$mli.PS1.subj_coord.fa");

system("date");
system("echo SumTablev2.py");
system("python $scriptdir/SumTablev2.py q_G$mlp.PE_I$mli.PS1.subj_coord.PolyA  q_G$mlp.PE_I$mli.PS1.pairs.sw.out.disable_count  q_G$mlp.PE_I$mli.PS1.pairs.ex.out q_G$mlp.PE_I$mli.PS1.pairs.sw.out");

system("date");
system("echo GetIntronfracv2.py");
system("python $scriptdir/GetIntronfracv2.py gene.pos pseudogene.phase2 $pep  Pg.xls");

system("date");
system("echo PgClassification.py");
system("python $scriptdir/PgClassificationv2.py Pg.xls Pg.add.xls");

system("date");
system("echo wgdlist pipeline");
system("$blastadir/formatdb -i $pep -p T");
system("$blastadir/blastall -i $pep -d $pep -p blastp -e 1e-10 -b 10 -v 10 -m 8 -o blast -a 18");
system("python $scriptdir/Pggff.py Pg.xls");
system("python $scriptdir/mcscanformatv2.py $pep gene.pos spe.gff");
system("cat spe.gff pg.gff > xyz.gff");
system("cat blast pg.blast > xyz.blast");
system("$mcscanxdir/MCScanX xyz"); #/home/pub/share_soft/MCScanX/MCScanX
system("python $scriptdir/Mcscan2Pglstv2.py xyz.collinearity xyz.tandem wgdlist tandemlst");

system("date");
system("echo FinalPglst.py");
system("python $scriptdir/FinalPglst.py wgdlist tandemlst Pg.add.xls final.pg.xls");

if (exists $opts{"lncrna"}) {
	my $lrna = $opts{"lncrna"};
	unless ($lrna =~ /\.gff3?$/) {
		die "$lrna is an illegal file name, it should be in gff format!!!\n";
	}
	system("python $scriptdir/DistanceComparev5.1.py final.pg.xls gene.pos $lrna compare.xls");
	system("python $scriptdir/Sumgenev1.py compare.xls Gene.Pseudo.distance.xls");
	system("python $scriptdir/Sumpgv1.py compare.xls Pg.Pseudo.distance.xls");
}

system("rm -rf xyz* gene.pos gene.regions masked.region spe.gff tandemlst wgdlist q pseudogene.phase2  blast q_* overlap* temp* Pg.xls Pg.add.xls helitron.region pg.*");

system("echo completed!!!");
system("date");
exit(0);


L:
############################################### if repeatMaskedGff is provided ##########################################################

my $remagff = $opts{"repeatMaskedGff"};

system("python $scriptdir/fa-mask.py --regions masked.region $rfa > $spe.rep.gene.masked.fa");

system("date");
system("exonerate");
system("$exoneratedir/exonerate --model protein2genome --showquerygff no --showtargetgff yes --maxintron 5000 --showvulgar yes --ryo \"%ti\\t%qi\\t%tS\\t%qS\\t%tl\\t%ql\\t%tab\\t%tae\\t%tal\\t%qab\\t%qae\\t%qal\\t%pi\\n\" $pep $spe.rep.gene.masked.fa > exonerate.out");

system("date");
system("echo ExtractExonerateOut.py");
system("python $scriptdir/ExtractExonerateOut.py exonerate.out exonerate.blast");

system("date");
system("echo ParseBlast.py");
system("python $scriptdir/ParseBlast.py -f get_qualified4 -blast exonerate.blast -fasta $pep -E $ev -I $identh -L $lenth -P $pepth -Q 1");

system("date");
system("rm -rf q") if -s "q";

system("date");
system("echo create soft link");
$new_pep = $pepth * 100;
$file = "exonerate.blast_E".$ev."I".$identh."L".$lenth."P".$new_pep."Q1.qlines";
system("ln -s $file q");

system("date");
system("echo Pseudo_step1.py");
system("python $scriptdir/Pseudo_step1.py q $mlp");

system("date");
system("echo Pseudo_step2.py");
system("python $scriptdir/Pseudo_step2.py q_G$mlp.PE $mli");

system("date");
system("echo Pseudo_step3.py");
system("python $scriptdir/Pseudo_step3.py q_G$mlp.PE_I$mli.PS1");

system("date");
system("echo FastaManager.py");
system("python $scriptdir/FastaManager.py -f get_stretch4 -fasta $rfa  -coords q_G$mlp.PE_I$mli.PS1.subj_coord");

system("date");
system("echo BlastUtilityv2.py");
system("python $scriptdir/BlastUtilityv2.py -f batch_sw -p tfasty34 -g q_G$mlp.PE_I$mli.PS1.pairs -i $pep -j q_G$mlp.PE_I$mli.PS1.subj_coord.fa -bdir $fastadir -d 1"); #/home/pub/share_soft/fasta34

system("date");
system("echo Pseudo_step4.py");
system("python $scriptdir/Pseudo_step4.py $scriptdir/blosum50.matrix q_G$mlp.PE_I$mli.PS1.pairs.sw.out");

system("date");
system("echo CheckStrand.py");
system("python $scriptdir/CheckStrand.py q_G$mlp.PE_I$mli.PS1.pairs.sw.raw q_G$mlp.PE_I$mli.PS1.subj_coord q_G$mlp.PE_I$mli.PS1.subj_coord.Strd");

system("date");
system("echo PolyACheck.py");
system("python $scriptdir/PolyACheck.py $rfa q_G$mlp.PE_I$mli.PS1.subj_coord.Strd q_G$mlp.PE_I$mli.PS1.subj_coord.PolyA");

system("date");
system("echo CheckIntron.py");
system("python $scriptdir/CheckIntron.py q_G$mlp.PE_I$mli.PS1.pairs $pep q_G$mlp.PE_I$mli.PS1.subj_coord.fa");

system("date");
system("echo SumTablev2.py");
system("python $scriptdir/SumTablev2.py q_G$mlp.PE_I$mli.PS1.subj_coord.PolyA  q_G$mlp.PE_I$mli.PS1.pairs.sw.out.disable_count  q_G$mlp.PE_I$mli.PS1.pairs.ex.out q_G$mlp.PE_I$mli.PS1.pairs.sw.out");

system("date");
system("echo GetIntronfracv2.py");
system("python $scriptdir/GetIntronfracv2.py gene.pos pseudogene.phase2 $pep  Pg.xls");

system("date");
system("echo PgClassificationv2.py");
system("python $scriptdir/PgClassificationv2.py Pg.xls Pg.add.xls");

system("date");
system("echo wgdlist pipeline");
system("$blastadir/formatdb -i $pep -p T");
system("$blastadir/blastall -i $pep -d $pep -p blastp -e 1e-10 -b 10 -v 10 -m 8 -o blast -a 18");
system("python $scriptdir/Pggff.py Pg.xls");

system("python $scriptdir/mcscanformatv2.py $pep  gene.pos spe.gff");
system("cat spe.gff pg.gff > xyz.gff");
system("cat blast pg.blast > xyz.blast");
system("$mcscanxdir/MCScanX xyz"); #/home/pub/share_soft/MCScanX/MCScanX

#####################################################################################################################
system("date");
system("echo Repeat2Region");
system("python $scriptdir/Repeat2Region.py $remagff Pg.add.xls helitron.region pg.element");

system("date");
system("echo overlapRegion");
system("perl $scriptdir/overlapRegion.pl -i1 pg.element -i2 helitron.region -o overlap.out");

system("date");
system("echo Overlap2Helilst");
system("python $scriptdir/Overlap2Helilst.py overlap.out helitron.pg.lst");

system("date");
system("echo Mcscan2Pglstv2.py");
system("python $scriptdir/Mcscan2Pglstv2.py xyz.collinearity xyz.tandem wgdlist tandemlst");

system("date");
system("echo FinalPglsthelit");
#############################################################################
system("python $scriptdir/FinalPglsthelit.py wgdlist tandemlst helitron.pg.lst Pg.add.xls final.pg.xls");
#system("python $scriptdir/PgClassification.py wgdlist pseudogene.phase3");

if (exists $opts{"lncrna"}) {
	my $lrna = $opts{"lncrna"};
	unless ($lrna =~ /\.gff3?$/) {
		die "$lrna is an illegal file name, it should be in gff format!!!\n";
	}
	system("python $scriptdir/DistanceComparev5.1.py final.pg.xls gene.pos $lrna compare.xls");
	system("python $scriptdir/Sumgenev1.py compare.xls Gene.Pseudo.distance.xls");
	system("python $scriptdir/Sumpgv1.py compare.xls Pg.Pseudo.distance.xls");
}

system("rm -rf xyz* gene.pos gene.regions masked.region spe.gff tandemlst wgdlist q pseudogene.phase2  blast q_* overlap* temp* Pg.xls Pg.add.xls helitron.region pg.*");

system("date");
system("echo completed!!!");



