version 1.0

import "fqc.wdl" as fqc
import "bowtie2.wdl" as aln
import "alnQC.wdl" as aqc
import "sam_to_bam.wdl" as sam2bam
import "sort_by_position.wdl" as sortbypos
import "sort_by_name.wdl" as sortbyname
import "hisat2_build.wdl" as hisat_build
import "bowtie2_build.wdl" as bowtie2_build
import "hisat2.wdl" as hisat2

workflow alignment_recipe_workflow {
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
        String aligner
        Boolean buildref
    } 

    call fqc.FQCWorkflow as fqc1 { input: fq_input1 = fq_input1,fq_input2 = fq_input2, outdir= outdir}
    if(aligner=="bowtie2"){
    if(buildref){
        call bowtie2_build.B2BWorkflow as b2b{ input:fref=ref_fqc, outdir=build_ref}
    String hold=b2b.indxout
    call aln.ALNWorkflow as alnb2b{ input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=hold, outfile=outfile, aqc_out=aqc_out}
    call aqc.AQCWorkflow as aqc  { input: sam_input=alnb2b.Soutfile, aqc_out=aqc_out} 
    call sam2bam.Sam2BamWorkflow as s2b { input: input_sam=alnb2b.Soutfile, temp_bam=temp_bam}
    call sortbypos.SortPosWorkflow as sbp {input: temp_bam=s2b.outfile, sort_pos=sort_pos}
    call sortbyname.SortNameWorkflow as sbn {input: temp_bam=s2b.outfile, sort_name=sort_name}
   }
    if(!buildref){
    call aln.ALNWorkflow as alnd{ input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=build_ref, outfile=outfile, aqc_out=aqc_out}
    call aqc.AQCWorkflow as aqcd  { input: sam_input=alnd.Soutfile, aqc_out=aqc_out}
    call sam2bam.Sam2BamWorkflow as s2bd { input: input_sam=alnd.Soutfile, temp_bam=temp_bam}
    call sortbypos.SortPosWorkflow as sbpd {input: temp_bam=s2bd.outfile, sort_pos=sort_pos}
    call sortbyname.SortNameWorkflow as sbnd {input: temp_bam=s2bd.outfile, sort_name=sort_name}
}}
    if(aligner=="hisat2"){
    if(buildref){
        call hisat_build.H2BWorkflow as h2b{ input:fref=ref_fqc, outdir=build_ref}
    String hhold=h2b.indexout
    call hisat2.Hisat2Workflow as alnh2b{ input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=hhold, outfile=outfile, aqc_out=aqc_out}
    call aqc.AQCWorkflow as aqchisat  { input: sam_input=alnh2b.Soutfile, aqc_out=aqc_out}
    call sam2bam.Sam2BamWorkflow as s2bhisat { input: input_sam=alnh2b.Soutfile, temp_bam=temp_bam}
    call sortbypos.SortPosWorkflow as sbphisat {input: temp_bam=s2bhisat.outfile, sort_pos=sort_pos}
    call sortbyname.SortNameWorkflow as sbnhisat {input: temp_bam=s2bhisat.outfile, sort_name=sort_name}
    }
    if(!buildref){
    call hisat2.Hisat2Workflow as alnh2bd{ input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=build_ref, outfile=outfile, aqc_out=aqc_out}
    call aqc.AQCWorkflow as aqchisatd  { input: sam_input=alnh2bd.Soutfile, aqc_out=aqc_out}
    call sam2bam.Sam2BamWorkflow as s2bhisatd { input: input_sam=alnh2bd.Soutfile, temp_bam=temp_bam}
    call sortbypos.SortPosWorkflow as sbphisatd {input: temp_bam=s2bhisatd.outfile, sort_pos=sort_pos}
    call sortbyname.SortNameWorkflow as sbnhisatd {input: temp_bam=s2bhisatd.outfile, sort_name=sort_name}
}
}
}
