version 1.0

workflow SortNameWorkflow {
    input {
        String temp_bam
        String sort_name
    }
    call sort_by_name { input:temp_bam=temp_bam,sort_name=sort_name }
}

task sort_by_name {
    input {
      String sort_name
      String temp_bam
    }

    command {
        samtools sort -n ${temp_bam} -o ${sort_name}
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
