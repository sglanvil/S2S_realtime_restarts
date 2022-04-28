#!/usr/bin/env bash 
source ~/.bash_profile

# hist and postproc are combined, so just one src/dest
dest=/gpfs/csfs1/cesm/collections/S2Sfcst/POSTPROC/
src=/glade/scratch/ssfcst/70Lwaccm6/

rsync -avz --no-perms --no-owner --no-group --no-times --size-only $src/ casper.ucar.edu:$dest/

