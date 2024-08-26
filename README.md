# featureviewerApp
Feature Viewer web based app

## Author: Reid Spalding
## Ver. 0.2
## Updated: Aug. 26, 2024

##### SETUP #####

	1. clone git repo to easily accessible location

	2. check os/terminal/python has access to following tools from the repo's dir
		a. SAMtools
		b. BCFtools

	3. install necessary python packages
		packages:
			- sys
			- os
			- pysam
			- pandas
			- subprocess
			- flask

	*** all above packages and tools MUST be accessible in the venv where main.py is run! ***

##### INPUTS #####

	- input files MUST currently be in .bam format for UNSORTED alignment and .fasta for reference genome
	- for best results, use .bam and .fasta file provided with repo/submission
	- input files were retrieved from:
		reference genome: https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_002571405.2/
		read data: https://www.ncbi.nlm.nih.gov/sra/SRR5892450
	- to obtain .bam from .fastq.gz, follow pipeline outlined in doc terminal_commands.txt

	- 

##### RUNNING CODE #####

	1. run main.py from repo dir

	2. console will output web address for application, nagivate to url
		this location will appear in the console as:
		|
		|	* Running on all addresses (0.0.0.0)
 		|	* Running on http://127.0.0.1:5000
 		|	* Running on http://192.168.0.84:5000
 		|
 		using either URL should access the application

 	3. upload files
 		*** files MUST be .bam and .fasta, respectively. See inputs for details

 	4. depending on system speed and file sizes, variant calling may take time. Results page will refresh when results are avaliable
 		*** For run-time reference: running application from 2019 Macbook Air as the server host took approx. 20 minutes for approx. 1gb bam file

 	5. View results as a table or navigate to viewer page to see visual snp location map
 		*** this feature is NOT fully implimented. Currently, data displayed is STATIC and only shows output from provided test data.
 		*** again, viewer is currenly NOT DYNAMIC and WILL NOT SHOW map from inputs due to time constraints

##### TROUBLESHOOTING #####

 	- input files currently must be in correct format!!!
 		*** formated input files for testing are provided or avaliable 
 	- server host CANNOT run while asleep or logged out. local server host must be on and running currently for application to work

##### DESIGN APPROACH AND ASSUMPTIONS #####

	- assumption: processing would be handled by UNIX pipe for faster processing, currentl bottleneck at local implementation
	- assumption: adapters were not present in reads
		*** cutadapt was run but adapters apeared to be already filtred
	- assumption: quality was overall high across reads for sample set and quality visualization was low priority, skipped for current implementations

	data analysis was handled following pipeline outlined in terminal_commands.txt
	most familiarity was in html, but react could be used later for better visual implementation
	main goals were data analysis fuctions and output of snps due to time contraints

##### COMPLETED FEATURES / DESIGN REQUIRMENTS #####

 	Data Analysis
		1. Gather data. 
		2. Align the short read sequences to the reference genome using your preferred aligner (bowtie2).
		3. Use a variant caller to identify SNPs
			- Determine the appropriate constraints within the variant caller to determine whatis a “real” SNP versus a sequencing artifact.
				*** uses standard constraints

	Backend
		1. Set up a basic Flask server from scratch
		2. Run the variant caller to identify SNPs when provided the .BAM alignment file and the reference genome.
		3. API/Controller to provide results of the variant caller to the front end

	Frontend (Choose one option)
		Option 2: Vanilla HTML/JavaScript/CSS (Bootstrap)
			1. Create an HTML page with Bootstrap for styling
			2. Use JavaScript to: *kinda*
				- Display identified SNPs from the VCF as highlights or markers on the sequence
				- Show a table listing detected SNPs with their positions 
	
	Bonus Features (if time allows)
		- Implement basic error handling and input validation

##### KNOWN ISSUES & FUTURE IMPROVEMENTS #####

 	1. javascript visualization of genome map/snp locations is not finished and NOT CURRENTLY DYNAMIC
 		*** next steps would be to complete this feature and increase avaliable information

 	2. strict file input types
 		*** next steps include:
 			- increasing input options to include sorted bam files, sam files, fastq reference, compressed of all forms
 			- add input option for raw read data to fully automate pipeline

 	3. next step: add snp.csv report

 	4. next step: include quality scores in reports

 	5. next step: improve UI and aestetics


