version 1.0

workflow ALNWorkflow {
    input{
        File fq_input1
        File fq_input2
        File ref_fqc
        String build_ref
        String outfile
        String aqc_out
    }

    call aln { input: fq_input1=fq_input1,fq_input2=fq_input2, ref_fqc=ref_fqc, build_ref=build_ref, outfile=outfile,aqc_out=aqc_out}
    output{
        String Soutfile=aln.outfile
    }
}

task aln {
    input {
      File fq_input1
      File fq_input2
      File ref_fqc
      String build_ref
      String outfile
      String aqc_out
    }

    command {
        bowtie2 -x ${build_ref} -1 ${fq_input1} -2 ${fq_input2} -S ${outfile}
        #samtools stats ${outfile}|grep ^SN > ${aqc_out}
    }
    output{
        File outfile=outfile
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
