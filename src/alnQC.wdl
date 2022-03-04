version 1.0

workflow AQCWorkflow {
    input {
        String sam_input
        String aqc_out
    }

    call aqc { input:sam_input=sam_input,aqc_out=aqc_out }
}

task aqc {
    input {
      String sam_input
      String aqc_out
    }

    command {
        samtools stats ${sam_input}|grep ^SN|cut -f2- >${aqc_out}
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
