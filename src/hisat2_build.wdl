version 1.0

workflow H2BWorkflow {
    input {
        File fref
        String outdir
    }

    call h2build { input: fref=fref,outdir=outdir }
    output{
        String indexout=h2build.outfile
    }
}

task h2build {
    input {
      File fref
      String outdir
    }

    command {
        hisat2-build -f ${fref} ${outdir}
    }
    output{
        String outfile=outdir
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
