## feature viewer script
## Author: Reid Spalding
## Ver. 0.0
## Updated: Aug. 25, 2024

## imports
import sys
import pysam

## read vcf
def parse_vcf(vcf_file):

    try:
        vcf = pysam.VariantFile(vcf_file, "r")
        output = []

        ## iterate over vcf
        for rec in vcf.fetch():

            ## inits
            chrom = rec.chrom
            pos = rec.pos
            ref = rec.ref
            alts = rec.alts

            ## ignore multi allele
            if len(alts) > 1:  
                continue

            alt = alts[0]

            ## find SNP
            if len(ref) == 1 and len(alt) == 1:
                output.append(f"SNP found: {chrom}:{pos} {ref}->{alt}")

        return output
    
    except Exception as e:
        return f"Error processing file: {e}"


if __name__ == "__main__":
    ## get file path from args
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        result = parse_vcf(filepath)
        print(result)  # print out
    else:
        print("No file path provided.")