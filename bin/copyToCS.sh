#!/usr/bin/env bash 
source ~/.bash_profile

# ----------------- original archive directory ----------------- 
landSource=/glade/scratch/ssfcst/archive/I2000Clm50BgcCrop.002runRealtime/rest/
sdSource=/glade/scratch/ssfcst/archive/b.e21.BWHIST.SD.f09_g17.002.nudgedOcn/rest/
atmSource=/glade/scratch/ssfcst/CESM2_NCEP_0.9x1.25_L32/
ocnSource=/glade/scratch/ssfcst/archive/g.e21.GIAF_JRA.TL319_g17.ssfcst_03/rest/

# ----------------- campaign storage ----------------- 
landDest=/glade/campaign/cesm/development/cross-wg/S2S/land/rest/
sdDest=/glade/campaign/cesm/development/cross-wg/S2S/SDnudgedOcn/rest/
atmDest=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/CAMI/CFSv2/
ocnDest=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/OCEANIC/

echo "......................rsync begin..................."

rsync -avz --no-perms --no-owner --no-group --no-times --size-only $sdSource/2022* casper.ucar.edu:$sdDest/
rsync -avz --no-perms --no-owner --no-group --no-times --size-only $atmSource/*2022* casper.ucar.edu:$atmDest/
rsync -avz --no-perms --no-owner --no-group --no-times --size-only $ocnSource/0273* casper.ucar.edu:$ocnDest/
rsync -avz --no-perms --no-owner --no-group --no-times --size-only $landSource/2022* casper.ucar.edu:$landDest/

echo ".........................rsync done......................."

#latestFile=$(ls $sdSource | sort -V | tail -n 1)
#rsync -av $sdSource/$latestFile casper.ucar.edu:$sdDest/

#latestFile=$(ls $atmSource | sort -V | tail -n 1)
#rsync -av $atmSource/$latestFile casper.ucar.edu:$atmDest/

#for daysBack in {7..1}; do
#       latestFile=$(ls $landSource | sort -V | tail -n $daysBack | head -n 1)
#       rsync -av $landSource/$latestFile casper.ucar.edu:$landDest/
#done


