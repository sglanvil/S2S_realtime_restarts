#!/usr/bin/env bash 
source ~/.bash_profile

# hist and postproc are combined, so just one src/dest
dest=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/S2SHINDCASTS/ 
src=/glade/scratch/ssfcst/cesm2cam6v2/ 

rsync -avz --no-perms --no-owner --no-group --no-times --size-only $src/ casper.ucar.edu:$dest/

