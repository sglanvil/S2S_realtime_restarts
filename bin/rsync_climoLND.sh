#!/usr/bin/env bash 
source ~/.bash_profile

src=/glade/scratch/ssfcst/archive/I2000Clm50BgcCrop.002runRealtimeClimo/rest/
dest=/glade/campaign/cesm/development/cross-wg/S2S/CESM2/CLIMOLND/

rsync -avz --no-perms --no-owner --no-group --no-times --size-only ${src} casper.ucar.edu:${dest}

