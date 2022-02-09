version 1.0

workflow B2BWorkflow {
    input {
        File fref
        String outdir
    }

    call b2build { input: fref=fref,outdir=outdir }
    output{
        String indexout=b2build.outfile
    }
}

task b2build {
    input {
      File fref
      String outdir
    }

    command {
        bowtie2-build -f ${fref} ${outdir}
    }
    output{
        File outfile=outdir
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
