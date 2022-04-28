#!/usr/bin/env bash 
source ~/.bash_profile

cd /glade/scratch/ssfcst/I2000Clm50BgcCrop.002runRealtime
./xmlchange STOP_OPTION=ndays
./xmlchange STOP_N=7
./case.submit

