#!/usr/bin/env bash 
source ~/.bash_profile

# ------------------------ JULIE CARON ------------------------
src_pp=/glade/scratch/ssfcst/cesm2cam6climoATMv2/
src_hist=/glade/scratch/ssfcst/archive/cesm2cam6climoATM*

dest_pp=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/S2SHINDCASTSclimoATM/postprocess/
dest_hist=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/S2SHINDCASTSclimoATM/archive/

mkdir -p ${dest_hist}
mkdir -p ${dest_pp}

rsync -avz --no-perms --no-owner --no-group --no-times --size-only ${src_pp} casper.ucar.edu:${dest_pp}
rsync -avz --no-perms --no-owner --no-group --no-times --size-only ${src_hist} casper.ucar.edu:${dest_hist}



