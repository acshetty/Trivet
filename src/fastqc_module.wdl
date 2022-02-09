version 1.0 

workflow FastQC{
  call fqc {
        input:task_var1= workflow_var1
        }
}

task fqc {
    input{
        String infile
    }
  command {
     echo "fastqc module"
    fastqc ${infile}
  }
  output {
     # Write output to standard out
     File output_greeting = "Running fqc"
  }
}
