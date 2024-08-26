## bam to vcf script
## Author: Reid Spalding
## Ver. 0.2
## Updated: Aug. 25, 2024

import subprocess
import sys

def vcf_from_bam(bam_unsort, reference_fasta, output_vcf):

    bam_sorted = 'temp_sorted.bam'

    ## sam sort command
    samtools_sort_cmd = ['samtools', 'sort', '-o', bam_sorted, bam_unsort]

    subprocess.run(samtools_sort_cmd, check=True)

    ## bcf pile and call command
    mpileup_cmd = ['bcftools', 'mpileup', '-Ou', '-f', reference_fasta, bam_sorted]
    call_cmd = ['bcftools', 'call', '-mv', '-Oz', '-o', output_vcf]

    ## run one, pipe result
    mpileup_process = subprocess.Popen(mpileup_cmd, stdout=subprocess.PIPE)

    call_process = subprocess.Popen(call_cmd, stdin=mpileup_process.stdout, stdout=subprocess.PIPE)

    ## close pipe
    mpileup_process.stdout.close()

    ## wait for results
    call_output, call_error = call_process.communicate()

    ## check for err/results
    if call_process.returncode == 0:
        print("Variants successfully called and saved to '" + output_vcf + "'")
    else:
        print(f"Error in bcftools call: {call_error.decode('utf-8') if call_error else 'Unknown error'}")

if __name__ == "__main__":

    ## debug
    #bam_file = "bs_aligned.bam"
    #reference_fasta = "bs_ref.fasta"
    #output_vcf = "output.vcf.gz"
    #vcf_from_bam(bam_file, reference_fasta, output_vcf)
    
    output_vcf = "output.vcf.gz"

    ## get file path from args
    if len(sys.argv) > 3:
        bam_file = sys.argv[1]
        reference_fasta = sys.argv[2]
        output_vcf = sys.argv[3]
        vcf_from_bam(bam_file, reference_fasta, output_vcf)
        print(output_vcf)

    else:
        print("No file path provided.")

