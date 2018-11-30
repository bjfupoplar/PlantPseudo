cd /root/PlantPseudo

####get the sample data
wget ftp://106.2.11.172/pub/paper/sample.data.tar.gz
tar -zxvf sample.data.tar.gz


####get the data of the seven species

wget ftp://106.2.11.172/pub/paper/genome.tar.gz
tar -zxvf genome.tar.gz


#generate pathfile
##############################
pwd > ph
path=$(cat ph)

var1=software/fasta34
var2=software/MCScanX
var3=software/blast-2.2.25/bin
var4=software/exonerate-2.2.0-x86_64/bin

new=${path}/${var1}
echo "$new" > pathfile.txt
new=${path}/${var2}
echo "$new" >> pathfile.txt
new=${path}/${var3}
echo "$new" >> pathfile.txt
new=${path}/${var4}
echo "$new" >> pathfile.txt

export the  environment
echo "export EXONERATE=\$EXONERATE:$new" >script/env.sh
echo "$new" >script/env.sh
sh script/env.sh

rm -rf ph
#############################

cd bin

#sample data

perl pipeline.pl --scriptDir ../script --gff ../sample.data/genome.gff3 --pep ../sample.data/sample.pep --lncrna ../sample.data/lncrna.gff --rawFa ../sample.data/raw.fa --repeatMaskedFa ../sample.data/repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../sample.data

cd ../bin

#1.populus

perl pipeline.pl --scriptDir ../../script --gff pt.genome.gff3 --pep pt.pep --lncrna lncrna.gff  --rawFa pt.raw.fa --repeatMaskedFa pt.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/1.Populus

cd ../bin

#2.Arabidopsis/

perl pipeline.pl --scriptDir ../../script --gff at.genome.gff3 --pep at.pep --lncrna lncRNA.gff  --rawFa at.raw.fa --repeatMaskedFa at.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/2.Arabidopsis


cd ../bin

#3.Bdistachyon/

perl pipeline.pl --scriptDir ../../script --gff bd.genome.gff3 --pep bd.pep --lncrna lncRNA.gff --rawFa bd.raw.fa --repeatMaskedFa bd.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/3.Bdistachyon

cd ../bin

#4.Gmax/


perl pipeline.pl --scriptDir ../../script --gff gm.genome.gff3 --pep gm.pep --rawFa gm.raw.fa --repeatMaskedFa gm.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/4.Gmax

cd ../bin

#5.Mtruncatula/

perl pipeline.pl --scriptDir ../../script --gff mt.genome.gff3 --pep mt.pep --lncrna lncRNA.gff  --rawFa mt.raw.fa --repeatMaskedFa mt.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/5.Mtruncatula

cd ../bin

#6.Rice/
perl pipeline.pl --scriptDir ../../script --gff os.genome.gff3 --pep os.pep --lncrna lncRNA.gff --rawFa os.raw.fa --repeatMaskedFa os.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/6.Rice

cd ../bin

#7.Sbicolor/

perl pipeline.pl --scriptDir ../../script --gff sb.genome.gff3 --pep sb.pep --rawFa sb.raw.fa  --repeatMaskedFa sb.repmasked.fa  --eValueE 5 --idenThresh 20 --lenThresh 30 --proThresh 0.05 --qs 1 --mLenPse 50 --mLenIntron 50 --dirfile ../pathfile.txt  --outDir ../data/7.Sbicolor
