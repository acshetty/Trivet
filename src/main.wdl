version 1.0

import "fqc.wdl" as fqc
import "bowtie2.wdl" as aln
import "alnQC.wdl" as aqc
import "sam_to_bam.wdl" as sam2bam
import "sort_by_position.wdl" as sortbypos
import "sort_by_name.wdl" as sortbyname

workflow main_workflow {
    input{
        File fq_input1
        File fq_input2
        String outdir
        String ref_fqc
        String build_ref
        String outfile
        String aqc_out
        String temp_bam
        String sort_pos
        String sort_name
    } 

    call fqc.FQCWorkflow as fqc1 { input: fq_input1 = fq_input1,fq_input2 = fq_input2, outdir= outdir}
    call aln.ALNWorkflow{ input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=build_ref, outfile=outfile, aqc_out=aqc_out} 
    call aqc.AQCWorkflow as aqc  { input: sam_input=ALNWorkflow.Soutfile, aqc_out=aqc_out} 
    call sam2bam.Sam2BamWorkflow as s2b { input: input_sam=ALNWorkflow.Soutfile, temp_bam=temp_bam}
    call sortbypos.SortPosWorkflow as sbp {input: temp_bam=s2b.outfile, sort_pos=sort_pos}
    call sortbyname.SortNameWorkflow as sbn {input: temp_bam=s2b.outfile, sort_name=sort_name}
}
