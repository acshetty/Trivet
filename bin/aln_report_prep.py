import shutil
import getopt, sys, os
from optparse import OptionParser
import subprocess
import pandas
import json
import re
from datetime import datetime


parser = OptionParser()
parser.add_option("-i", "--info", dest="info",help="Path to info file", metavar="FILE")
parser.add_option("-n", "--name", dest="filename",help="Name for Outputs", metavar="FILE")
parser.add_option("-o", "--outdir", dest="outdir",help="Path to Output Directory", metavar="PATH")
(options, args) = parser.parse_args()

###
###

def main():
    infof=pandas.read_table(options.info)
    print(infof)
    sample_names=infof['SampleID']
    print(sample_names)
    cn=["SampleID", "Total.Reads", "Total.Mapped.Reads","Percent.Mapped.Reads","Percent.Properly.Paired","Uniquely.Mapped.Reads","Percent.Exonic","Percent.Intronic","Percent.Intergenic"]
    sumt=pandas.DataFrame(columns=cn)
    for sampleid in sample_names:
        aqcdir=options.outdir+"/AlignStats/"
        reportdir=options.outdir+"Reports/"
        if not os.path.exists(reportdir):
            os.makedirs(reportdir)
        sout1=aqcdir+sampleid+".picard.stats" 
        sout2=aqcdir+sampleid+".stats"
        aqc=make_summary(sout1,sout2, sampleid,aqcdir)
        sumt=sumt.append(aqc)
    summary=aqcdir+"Summary.txt"
    sumt.to_csv(summary, index=False, sep="\t")
    print(sumt)
    aqcReport(options.filename, options.outdir,options.info)

def aqcReport(name, odir,infof):
    fqcdir=odir+"/Reports/"
    outdir=odir+"/AlignStats/"
    rcmd="rmarkdown::render('/local/projects-t3/achatterjee/WDL/Trivet/src/ALN_WDL.Rmd', params=list(projectname='"+name+"', pathd='"+ outdir+"', infof='"+infof+"'), output_dir='"+fqcdir+"' ,output_file='ALN_Report.pdf')"
    print(rcmd)
    rmake=fqcdir
    if not os.path.exists(rmake):
        os.makedirs(rmake)
    #rmake1=outdir+"FastQC_Outputs/"
    #if not os.path.exists(rmake1):
    #    os.makedirs(rmake1)
    rpath=rmake+"/ALN.R"
    f=open(rpath,"w")
    f.write(rcmd)
    f.close()
    return True

def make_summary(picard,sam, sampleid, aqcdir):
    pstats=pandas.read_table(picard, nrows=1, skiprows=6)
    ppp=0
    rts=0
    tmr=0
    umr=0
    pe=0
    pintronic=0
    pinter=0
    non_decimal = re.compile(r'[^\d.]+')
    ###Extract from picard
    pintronic=pstats["PCT_INTRONIC_BASES"]
    pe=pstats["PCT_MRNA_BASES"]
    pinter=pstats["PCT_INTERGENIC_BASES"]
    ###Extract stats from .stats
    with open(sam, 'r') as f:
        for line in f:
            if 'percentage of properly paired reads' in line:
                ppp=float(non_decimal.sub('',line))
            elif 'raw total sequences' in line:
                rts=non_decimal.sub('',line)
            elif 'reads mapped:' in line:
                tmr=non_decimal.sub('',line)
        umr=int(line)
    pmr=(float(tmr)/float(rts))*100
    ctemp=["SampleID", "Total.Reads", "Total.Mapped.Reads","Percent.Mapped.Reads","Percent.Properly.Paired","Uniquely.Mapped.Reads","Percent.Exonic","Percent.Intronic","Percent.Intergenic"]
    temp=pandas.DataFrame(columns=ctemp)
    temp.at[0,"SampleID"]=sampleid
    temp.at[0,"Total.Reads"]=rts
    temp.at[0,"Total.Mapped.Reads"]=tmr
    temp.at[0,"Percent.Mapped.Reads"]=round(pmr,2)
    temp.at[0,"Percent.Properly.Paired"]=round(ppp,2)
    temp.at[0,"Uniquely.Mapped.Reads"]=umr
    temp.at[0,"Percent.Exonic"]=round(float(pe)*100,2)
    temp.at[0,"Percent.Intronic"]=round(float(pintronic)*100,2)
    temp.at[0,"Percent.Intergenic"]=round(float(pinter)*100,2)
    print(umr)
    print(pmr)
    print(ppp)
    print(rts)
    print(tmr)
    return temp
                

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
    Input: List of files in the input directory and path to input directory	    Input: List of files in the input directory and path to input directory
    Output: List of full paths to log files in input directory	    Output: List of full paths to log files in input directory
    """
    return [os.path.join(dirpath, i) for i in files]

if __name__ == '__main__':
    main()
