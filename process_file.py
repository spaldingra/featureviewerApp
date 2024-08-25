## feature viewer script
## Author: Reid Spalding
## Ver. 0.0
## Updated: Aug. 25, 2024

## imports
import sys
import pysam
import pandas as pd


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
                snp =[str(chrom), str(pos), str(ref), str(alt)]
                output.append(snp)

        return output
    
    except Exception as e:
        return f"Error processing file: {e}"



if __name__ == "__main__":
    ## get file path from args
    result = parse_vcf('static/files/bs_variants.vcf.gz')
    #for i in result:
        #print(i)  # print out
    #print(result)


    cols = ['Gene', 'LOC', 'Ref_Base', 'SNP']
    df = pd.DataFrame(result, columns = cols)
    html = df.to_html()
    #print(df)
    #print(html)

    out = open('templates/results.html', 'w')
    out.write(html)
    out.close()

    print('done')
