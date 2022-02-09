version 1.0

workflow Hisat2Workflow {
    input{
        File fq_input1
        File fq_input2
        File ref_fqc
        String build_ref
        String outfile
        String aqc_out
    }

    call hisat2_aln { input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=build_ref, outfile=outfile,aqc_out=aqc_out}
    output{
        String Soutfile=hisat2_aln.outfile
    }
}

task hisat2_aln {
    input {
      File fq_input1
      File fq_input2
      File ref_fqc
      String build_ref
      String outfile
      String aqc_out
    }

    command {
        hisat2 -x ${build_ref} -1 ${fq_input1} -2 ${fq_input2} -S ${outfile}
        #samtools stats ${outfile}|grep ^SN > ${aqc_out}
    }
    output{
        File outfile=outfile
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
