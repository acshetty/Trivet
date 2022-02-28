version 1.0

workflow FQCWorkflow {
    input {
        File fq_input1
        File fq_input2
        String outdir
    }

    call fqc { input: fq_input1=fq_input1,fq_input2=fq_input2,outdir=outdir }
}

task fqc {
    input {
      File fq_input1
      File fq_input2
      String outdir
    }

    command {
        fastqc --extract -o ${outdir} ${fq_input1} ${fq_input2}
        python /local/projects-t3/achatterjee/WDL/scripts/rename_fqc.py -o ${outdir}
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
