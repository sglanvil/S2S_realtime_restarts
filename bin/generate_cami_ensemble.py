#!/usr/bin/env python
import os, sys
cesmroot = os.environ.get('CESM_ROOT')
s2sfcstroot = os.path.join(os.path.dirname(os.path.join(os.path.abspath(__file__))), os.path.pardir)

if cesmroot is None:
    raise SystemExit("ERROR: CESM_ROOT must be defined in environment")

# This is needed for globus_sdk
#_LIBDIR=os.path.join(os.environ.get("HOME"),".local","lib","python3.6","site-packages")
#sys.path.append(_LIBDIR)
_LIBDIR = os.path.join(cesmroot,"cime","scripts","Tools")
sys.path.append(_LIBDIR)
_LIBDIR = os.path.join(cesmroot,"cime","scripts","lib")
sys.path.append(_LIBDIR)

import datetime, random, threading, time, shutil
from standard_script_setup import *
from CIME.utils            import run_cmd, safe_copy, expect
from argparse              import RawTextHelpFormatter
#from globus_utils          import *

def parse_command_line(args, description):
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=RawTextHelpFormatter)
    CIME.utils.setup_standard_logging_options(parser)
    parser.add_argument("--date",
                        help="Specify a start Date")

    parser.add_argument("--model",help="Specify a case (cesm2cam6, 70Lwaccm6)", default="cesm2cam6")

    args = CIME.utils.parse_args_and_handle_standard_logging_options(args, parser)
    cdate = os.environ.get("CYLC_TASK_CYCLE_POINT")

    if args.date:
        try:
            date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD or YYYY-MM")
    elif cdate:
        date = datetime.datetime.strptime(cdate, '%Y-%m-%d')
    else:
        date = datetime.date.today()
        date = date.replace(day=date.day-1)

    return date.strftime("%Y-%m-%d"), args.model

def get_rvals(date, ensemble, model):
    if model == "70Lwaccm6":
        rvals_file = os.path.join(os.getenv("WORK"),"cases","70Lwaccm6","camic_"+date+".txt")
    else:
        rvals_file = os.path.join(os.getenv("WORK"),"cases","CESM2","camic_"+date+".txt")
    rvals = []
    if os.path.isfile(rvals_file):
        with open(rvals_file,"r") as fd:
            rawvals = fd.read().split(',')
        for rval in rawvals:
            rval = rval.strip()
            if rval.startswith('['):
                rval = int(rval[1:])
            elif rval.endswith(']'):
                rval = int(rval[:-1])
            else:
                rval = int(rval)
            rvals.append(rval)
    if len(rvals) < ensemble//2:
        newrvals = random.sample(range(500),k=ensemble//2)
        if len(rvals)>0:
            for i in 0,len(rvals)-1:
                if rvals[i] not in newrvals:
                    newrvals[i] = rvals[i]
        #save these rvals to a file
        with open(rvals_file,"w") as fd:
            fd.write("{}".format(newrvals))
        rvals = newrvals
    print "LEN of rvals is {}".format(len(rvals))
    return rvals

def create_cam_ic_perturbed(original, ensemble, date, baserundir, model, outroot="b.e21.f09_g17.cam.i.", factor=0.15):
    rvals = get_rvals(date, ensemble, model)

    outfile = os.path.join(baserundir,outroot+date+"-00000.nc")
    # first link the original ic file to the 0th ensemble member
    if os.path.exists(outfile):
        os.unlink(outfile)
    expect(os.path.isfile(original),"ERROR file {} not found".format(original))
    print("Linking {} to {}".format(original, outfile))
    rundir = os.path.dirname(outfile)
    if os.path.isdir(rundir):
        shutil.rmtree(rundir)
    os.makedirs(rundir)
    os.symlink(original, outfile)

    # for each pair of ensemble members create an ic file with same perturbation opposite sign
    month = date[5:7]

    if model == "70Lwaccm6":
        local_path = "/glade/campaign/cesm/collections/S2Sfcst"
    else:
        local_path = "/glade/campaign/cesm/development/cross-wg/S2S/CESM2/CAMI/RP"
    perturb_files = []
    for i in range(1,ensemble, 2):
        print "HERE rvals[{}] = {}".format(i//2,rvals[i//2])
        if model == "70Lwaccm6":
            perturb_file = os.path.join("S2S_70LIC",
                                        "{}".format(month),
                                        "70Lwaccm6.cam.i.M{}.diff.{}.nc".format(month,rvals[i//2]))
        else:
            perturb_file = os.path.join("{}".format(month),
                                        "CESM2.cam.i.M{}.diff.{}.nc".format(month,rvals[i//2]))
        dirname = os.path.dirname(os.path.join(local_path,perturb_file))
        if not os.path.isdir(dirname):
            print("Creating directory {}".format(dirname))
            os.makedirs(dirname)
        perturb_files.append(perturb_file)

    for i in range(1,ensemble, 2):
        perturb_file = os.path.join(local_path,perturb_files[i//2-1])
        outfile1 = os.path.join(baserundir[:-2]+"{:02d}".format(i), outroot+date+"-tmp.nc")
        outfile2 = os.path.join(baserundir[:-2]+"{:02d}".format(i+1), outroot+date+"-tmp.nc")
        print("Creating perturbed init file {}".format(outfile1))
        t = threading.Thread(target=create_perturbed_init_file,args=(original, perturb_file, outfile1, factor))
        t.start()
        t = threading.Thread(target=create_perturbed_init_file,args=(original, perturb_file, outfile2, -1*factor))
        t.start()
    while(threading.active_count() > 1):
        time.sleep(1)
#    for perturb_file in perturb_files:
#        os.unlink(os.path.join(local_path,perturb_file))
    

def create_perturbed_init_file(original, perturb_file, outfile, weight):
    ncflint = "ncflint"
    if not os.path.isdir(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    safe_copy(original, outfile)
    if "BWHIST" in original:
        cmd = ncflint + " -A -v US,VS,T,Q,PS -w {},1.0 {} {} {}".format(weight, perturb_file, original, outfile)    
    else:
        cmd = ncflint+" -O -C -v lat,lon,slat,slon,lev,ilev,hyai,hybi,hyam,hybm,US,VS,T,Q,PS -w {},1.0 {} {} {}".format(weight, perturb_file, original, outfile)    
    run_cmd(cmd, verbose=True)
    os.rename(outfile, outfile.replace("-tmp.nc","-00000.nc"))


def _main_func(description):
    date, model = parse_command_line(sys.argv, description)

    ensemble = 10
    if model == "cesm2cam6":
        sdrestdir = os.path.join(os.getenv("SCRATCH"),"CESM2","Ocean","rest","{}".format(date))
        baserundir = os.path.join(os.getenv("SCRATCH"),"cesm2cam6."+date[5:7]+".00","run.00")
        caminame = os.path.join(sdrestdir,"b.e21.f09_g17.cam.i.{date}-00000.nc".format(date=date))
        outroot = "b.e21.f09_g17.cam.i."
    else:
        ensemble = 20
        baserundir = os.path.join(os.getenv("SCRATCH"),"70Lwaccm6."+date[5:7]+".00","run.00")
        sdrestdir = os.path.join(os.getenv("SCRATCH"),"S2S_70LIC_globus","SDnudgedOcn","rest","{}".format(date))
        caminame = os.path.join(sdrestdir,"b.e21.BWHIST.SD.f09_g17.002.nudgedOcn.cam.i.{date}-00000.nc".format(date=date))
        outroot = "b.e21.BWHIST.SD.f09_g17.002.nudgedOcn.cam.i."

    create_cam_ic_perturbed(caminame,ensemble, date,baserundir, model, outroot=outroot)

if __name__ == "__main__":
    _main_func(__doc__)
