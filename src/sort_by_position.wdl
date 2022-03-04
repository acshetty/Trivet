version 1.0

workflow SortPosWorkflow {
    input {
        String temp_bam
        String sort_pos
    }
    call sort_by_pos { input:temp_bam=temp_bam,sort_pos=sort_pos }
    output{
        String sortbam=sort_by_pos.outfile
    }
}

task sort_by_pos {
    input {
      String sort_pos
      String temp_bam
    }

    command {
        samtools sort ${temp_bam} -o ${sort_pos}
    }
    output{
        String outfile=sort_pos
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
