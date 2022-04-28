#!/usr/bin/env bash 
source ~/.bash_profile

# ------------------------ ISLA SIMPSON ------------------------
#src_hist=/glade/scratch/ssfcst/archive/cesm2cam6NS*
#src_pp=/glade/scratch/ssfcst/cesm2cam6v2NS/
#dest_hist=/glade/campaign/cesm/development/cross-wg/S2S/SNAP/NudgedtoCLIMO/archive/
#dest_pp=/glade/campaign/cesm/development/cross-wg/S2S/SNAP/NudgedtoCLIMO/postprocess/

# ------------------------ JULIE CARON ------------------------
src_hist=/glade/scratch/ssfcst/archive/cesm2cam6climoOCNclimoATM*
src_pp=/glade/scratch/ssfcst/cesm2cam6climoOCNclimoATMv2/
dest_hist=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/S2SHINDCASTSclimoOCNclimoATM/archive/
dest_pp=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/S2SHINDCASTSclimoOCNclimoATM/postprocess/

mkdir -p ${dest_hist}
mkdir -p ${dest_pp}

rsync -avz --no-perms --no-owner --no-group --no-times --size-only ${src_pp} casper.ucar.edu:${dest_pp}
rsync -avz --no-perms --no-owner --no-group --no-times --size-only ${src_hist} casper.ucar.edu:${dest_hist}

