## feature viewer script
## Author: Reid Spalding
## Ver. 0.0
## Updated: Aug. 25, 2024

## imports
import pysam

## read vcf
def parse_vcf(vcf_file):

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

def get_snps():

    file = "static/files/bs_variants.vcf.gz"
    snps = parse_vcf(file)
    return snps

## main run
if __name__ == "__main__":

    file = "static/files/bs_variants.vcf.gz"
    snps = parse_vcf(file)
    print(snps)