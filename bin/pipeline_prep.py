import getopt, sys, os
from optparse import OptionParser
import subprocess
import pandas
import json
from datetime import datetime

parser = OptionParser()
parser.add_option("-i", "--info", dest="info",help="Path to info file", metavar="FILE")
parser.add_option("-n", "--name", dest="filename",help="Name for Outputs", metavar="FILE")
parser.add_option("-o", "--outdir", dest="outdir",help="Path to Output Directory", metavar="PATH")
parser.add_option("-b", "--refindex", dest="ref",help="Path to indexed reference", metavar="PATH")
parser.add_option("-r", "--ref", dest="reff",help="Path to reference", metavar="PATH")
parser.add_option("-a", "--aligner", dest="aligner",help="What aligner would you like to use (bowtie2 or hisat2)", metavar="bowtie2/hisat2")
(options, args) = parser.parse_args()

#Feb 14
#make -b optional
#check json file format
#add bowtie build component
#indicate in -h if arg is optional or not
#check what aligner to use

def main():
    if options.info and options.outdir:
        print("In main")
        info=pandas.read_table(options.info, skip_blank_lines=True)
        if(options.filename):
            name=options.filename
        else:
            namef=str(datetime.now())
            name=namef.strip("'")
        print(name)
        ###precheck to verify inputs
        pre=presub_QC(info, options.outdir,options.reff,name)
        samples=info["SampleID"]
        snum=len(info)
        ireff=0
        if(options.ref):
            treff=False
            ireff=options.ref
        else:
            treff=True
            ireff=aligner(options.reff, options.outdir, name,options.aligner)
        # for each sample make json and append wdl command to shell script
        for i in samples:
            tmp=info.loc[info['SampleID']==i]
            #tmp=tp.drop(index=True)
            tmp.reset_index(drop=True,inplace=True)
            print(tmp)
            jsonstr=makedf(i, tmp, name, options.outdir,ireff,options.reff,options.aligner,treff)
            jname=options.outdir+"/"+i+".json"
            jobj=json.loads(jsonstr)
            with open(jname, 'w') as json_file:
                json.dump(jobj[0], json_file,indent=4,sort_keys=True)
            wdlsh=shwdl(name,jname, options.outdir)


def aligner(ref, outdir, name, tool):
    if(tool=="bowtie2"):
        b2dir=outdir+"/Bowtie2_Build/"
        if not os.path.exists(b2dir):
            os.makedirs(b2dir)
        b2path=outdir+"/Bowtie2_Build/"+name 
    elif(tool=="hisat2"):
        b2dir=outdir+"/Hisat2_Build/"
        if not os.path.exists(b2dir):
            os.makedirs(b2dir)
        b2path=outdir+"/Hisat2_Build/"+name
    else:
        print("No aligner selected")
    return b2path

def shwdl(name, jsonpath, outdir):
    #Write shell script
    fname=outdir+"/"+name+"_wdl.sh"
    with open(fname, "a") as myfile:
        st="cromwell run main.wdl -i "+ jsonpath
        myfile.write(st+"\n")


def makedf(sample, df,name, outdir,refbuild,ref,tool,treff):
    #make json
    aqcout=outdir+"/AlignStats/"
    fqcout=outdir+"/fastQC/"
    bowtie2out=outdir+"/"+tool+"/"+sample+"/"
    sam2bamout=outdir+"/Sorted_Files/Temp/"+sample+"/"
    sortedout=outdir+"/Sorted_Files/"+sample+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(aqcout):
        os.makedirs(aqcout)
    if not os.path.exists(fqcout):
        os.makedirs(fqcout)
    if not os.path.exists(bowtie2out):
        os.makedirs(bowtie2out)
    if not os.path.exists(sam2bamout):
        os.makedirs(sam2bamout)
    if not os.path.exists(sortedout):
        os.makedirs(sortedout)
    samf=bowtie2out+name+"_"+sample+".sam"
    temp_bam=sam2bamout+name+"_"+sample+".bam"
    aqcout=aqcout+sample+".stats"
    sortnameout=sortedout+sample+"_sortedbyname.bam"
    sortposout=sortedout+sample+"_sortedbypos.bam"
    dat=[{'main_workflow.fq_input1':df['Read.File1'][0],
        'main_workflow.fq_input2': df['Read.File2'][0],
        'main_workflow.outdir':fqcout,
        'main_workflow.build_ref':refbuild,
        'main_workflow.aqc_out':aqcout,
        'main_workflow.outfile':samf,
        'main_workflow.ref_fqc':ref,
        'main_workflow.temp_bam':temp_bam,
        'main_workflow.sort_name':sortnameout,
        'main_workflow.aligner':tool,
        'main_workflow.buildref':treff,
        'main_workflow.sort_pos':sortposout}]
    jsonStr = json.dumps(dat,indent=4,sort_keys=True)
#    print(jsonStr)
    return jsonStr
    pass

def presub_QC(info, outdir, ref, name):
    #Check inouts provided by user
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    preqc_out=outdir+"/"+name+"_precheck.log"
    infocheck="Checking Info File"
    refcheck="Checking reference"
    if("SampleID" in info.columns and "Read.File1" in info.columns and "Read.File2" in info.columns and "Group" in info.columns):
        infocheck="Info file format requirements are satisfied"
    else:
        infocheck="Info file check failed. Ensure info file has following columns: SampleID, Group, Read.File1 and Read.File2"
    rf1=info['Read.File1']
    rf2=info['Read.File2']
    #check if files exist
    #R1
    listr1=[]
    listr2=[]
    r1c="Checking r1"
    r2c="checking r2"
    print("Checking inputs")
    for r1 in rf1:
        listr1.append(os.path.isfile(r1))
    if all(listr1):
        r1c="All paths have been verified for Files.Read1"
    else:
        r1c="Unable to verify presence of files. Please check the paths in Files.Read1 in the info file."
    for r2 in rf2:
        listr2.append(os.path.isfile(r2))
    if all(listr1):
        r2c="All paths have been verified for Files.Read2"
    else:
        r2c="Unable to verify presence of files. Please check the paths in Files.Read2 in the info file."
    #CHECK REFERENCE is present
    if(os.path.isfile(ref)):
        refcheck="Reference file exists and the path was verified."
    #check output directory and write log
    with open(preqc_out,'w') as logg:
        logg.write(infocheck+"\n"+r1c+"\n"+r2c+"\n"+refcheck+"\n"+"Pre-submission check completed sucessfully")
    return("success")

def makedir(pathlist):
    """
    Input: List of FULL Paths to be made if they dont exist

    Output: Confirmation if the paths were made
    """
    for path in pathlist:
        if not os.path.isdir(path):
            os.makedirs(path)
    return True

def prepend(files, dirpath):
    """
    Input: List of files in the input directory and path to input directory         Input: List of files in the input directory and path to input directory

    Output: List of full paths to log files in input directory      Output: List of full paths to log files in input directory
    """
    return [os.path.join(dirpath, i) for i in files]

if __name__ == '__main__':
    main()

