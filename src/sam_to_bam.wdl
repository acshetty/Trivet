version 1.0

workflow Sam2BamWorkflow {
    input {
        String input_sam
        String temp_bam
    }
    call sam2bam { input:temp_bam=temp_bam,input_sam=input_sam }
    output{
        String outfile=sam2bam.outfile
    }
}

task sam2bam {
    input {
      String input_sam
      String temp_bam
    }

    command {
        samtools view -bS -o ${temp_bam} ${input_sam}
    }
    output{
        File outfile=temp_bam
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
