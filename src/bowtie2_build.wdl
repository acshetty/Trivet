version 1.0

workflow B2BWorkflow {
    input {
        File fref
        String outdir
    }

    call b2build { input: fref=fref,outdir=outdir }
    output{
        String indxout=b2build.outf
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
        String outf=outdir
    }
    meta {
        author: "Apaala Chatterjee"
    }
}
