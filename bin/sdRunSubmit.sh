#!/usr/bin/env bash 
source ~/.bash_profile

cd /glade/scratch/ssfcst/b.e21.BWHIST.SD.f09_g17.002.nudgedOcn
./xmlchange STOP_OPTION=ndays
./xmlchange STOP_N=7
./case.submit

