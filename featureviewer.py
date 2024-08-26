## feature viewer script
## Author: Reid Spalding
## Ver. 0.2
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

## print results into html format
def printout(results):

    ## create data frame, convert to html
    cols = ['Gene', 'LOC', 'Ref_Base', 'SNP']
    df = pd.DataFrame(result, columns = cols)
    html = df.to_html()

    ## print to html file
    head_string = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}"<title>Results</title></head><body><a href="/viewer"><button type="button">Go to Viewer</button></a>'''

    out = open('templates/results.html', 'w')
    out.write('')
    out.close()

    out = open('templates/results.html', 'a')
    out.write(head_string)
    out.write(html)
    out.write('</body>')
    out.close()

## test get positions
def get_pos(vcf_file):

    try:
        vcf = pysam.VariantFile(vcf_file, "r")
        outpos = []

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
                snp =[str(pos), str(chrom)]
                outpos.append(snp)

        return outpos
    
    except Exception as e:
        return f"Error processing file: {e}"


if __name__ == "__main__":

    ## debug
    #result = parse_vcf('output.vcf.gz')
    #print(result)

    ## test to create output for timeline
    #result = get_pos('output.vcf.gz')
    #testfile = open('testfile.txt', 'w')
    #testfile.close()
    #testfile = open('testfile.txt', 'a')
    
    #for LOC in result:

        #testfile.write('{ position: ' + LOC[0] + ', label: "' + LOC[1] + '"},')
        
        #testfile.write('\n')
    
    #testfile.close()


    #exit()

    ## get file path from args
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        result = parse_vcf(filepath)
        printout(result)
        print(result)  # print out

    else:
        print("No file path provided.")

    