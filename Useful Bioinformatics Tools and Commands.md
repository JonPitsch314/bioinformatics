# Useful Bioinformatics Tools and Commands

## Broad Institute Bundle: 

Paste this link into your browser: ftp://ftp.broadinstitute.org/bundle . It should bring up a window that asks for a username and password.

Enter gsapubftp-anonymous as the username and leave the password blank. You should now see the contents of this bundle in your file management system.  

<img width="913" alt="Screen Shot 2022-09-29 at 2 26 15 PM" src="https://user-images.githubusercontent.com/105939034/199572524-89df28b6-741a-4f55-be58-f58c4a92a0ae.png">


This bundle contains literally dozens of useful files like reference genomes, panel of normals, and known sites of variants.

## GATK Best Practices Resources:  

https://console.cloud.google.com/storage/browser/gatk-best-practices;tab=objects?prefix=&forceOnObjectsSortingFiltering=false&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))  

The link above will take you to depository of useful files for hg19 and hg38.  

## Remove chr tag from CHROM column in VCF: 

If your vcf contains an alphanumeric in the chromosome column, you can run this command to remove the ‘chr’:  

awk '{gsub(/^chr/,""); print}' your.vcf > no_chr.vcf 

## Selecting Specific Columns from a BED file: 

awk '{print $1,$2,$3,$4,$5,$7}' file > output.bed  

## Downloading paired end FASTQ files from the SRA.  

The command below will download forward and reverse read FASTQ files from the NCBI Short Read Archive (SRA). This is useful for working with tools that require paired-end aligned data. 

fastq-dump --split-files –skip-technical SRA####  

Your downloaded files will look something like: 

SRR####_R1.fq 

SRR####_R2.fq 

## Combining Multiple Paired-End FASTQ files:

If you need to align several paired-end fastq files from the same sample, like seen in the image below, you will probably find it useful to combine the forward and reverse reads into a single fastq prior to aligning.

### Multiple fastq files from the same sample:

<img width="431" alt="Screen Shot 2022-11-03 at 9 32 31 AM" src="https://user-images.githubusercontent.com/105939034/199764819-576cdca7-1f61-49d4-9967-ccd151b175b3.png">

As you can imagine, it would be a time consuming, and possibly error prone, process to align each of these paired-end samples individually before combining them into a single sam/bam file. Instead you can combine all of the forward reads into a single fastq and all of the reverse reads into a single fastq prior to aligning. This can be done using the following commands:

    cat *_1.fq.gz > R1.fq.gz 
    
    cat *_2.fq.gz > R2.fq.gz
    
R1.fq.gz contains all of the forward read fastq files. R2.fq.gz contains all of the reverse read fastq files.

After creating the concatenated files, you may want to perform a quality check. Running the following commands will give you a line count for the R1 and R2 files. The line counts should match exactly for the data to undergo proper paired-end alignment. 

    zcat R1.fq.gz | wc -l > wc_R1.txt

    zcat R2.fq.gz | wc -l > wc_R2.txt

The output text files from the command above will contain the line count for each file. Again, they should match exactly. If they do, you can perform paired-end alignment with the following command:

    bwa mem -t INT ref_genome.fa R1.fq.gz R2.fq.gz | samtools view -@ INT -Sb - > bam_files/sample.bam

## Sort VCF from start position:

In an instance where I had to convert an hg19-coordinate based PON to an hg38-coordinate based PON, I had to sort a VCF so that each chromosome was organized by start position. To sort a vcf from beginning to end, run the command:

    cat in.vcf | awk '$1 ~ /^#/ {print $0;next} {print $0 | "sort -k1,1 -k2,2n"}' > out_sorted.vcf

## Reset VIM

You may encounter an issue where the arrow keys randomly stop working in vim. This is a frustrating issue that can be temporarily solved by resetting your terminal window. However, you can also reset vim itself by running the following from inside your document. *Make sure that you save your document before running this command*:

    :!reset

Your document should be temporarily cleared, then you will be asked to press Enter or any command as shown in the image below. 

<img width="361" alt="Screen Shot 2022-11-28 at 11 59 59 AM" src="https://user-images.githubusercontent.com/105939034/204359243-161d6947-8dbd-40eb-9260-fcd7c547cd5b.png">

Press Enter. The text in your document should be visible again and the arrow keys should work.

## MD5-SUM

If you are ever transferring a collection of files, you want to perform an MD5-Sum check on your files to ensure that you don't lose any data during the transfer. The following commands were used to perform an MD5 check on files that were transferred from my local desktop to the CURC Server through Globus. 

To create the md5 text file, use a terminal window to navigate to the directory on your computer where the files are stored. Then run:

    md5 * > filename.txt 

'*' is the wildcard that will create an md5 text file from all of the files contained within that specific directory. You can modify the command to suit your purposes. For example, you could run the following command to make an md5 text file for only the fq.gz files in a directory:

    md5 *.fg.gz > fastq_files.txt

After transferring the files to the server, navigate to the directory where they are stored. Transfer your md5 text file to that directory, then run:

    md5sum --check filename.txt

You should see a list of the file names in the directory appear as each file is examined for data loss, like the image below:

<img width="504" alt="Screen Shot 2022-11-28 at 12 43 32 PM" src="https://user-images.githubusercontent.com/105939034/204366706-57105425-9712-4ac2-8e4b-b8fdfe7eb3d5.png">

The 'OK' in the image above means that the file passed the md5sum check. If the file did not pass, then the md5sum check would have displayed: 'FAILED'.

## Change Java Memory Limit (For a specific toolkit in an environment)

To change the java memory in a toolkit in an environment, like picard, navigate to the /projects/$USER/software/anaconda/envs/ directory. Go to the environment directory, then the bin directory contained in the environment directory. 

<img width="513" alt="Screen Shot 2023-02-10 at 3 33 43 PM" src="https://user-images.githubusercontent.com/105939034/218213691-93842c5e-310a-4e18-9783-7900642ec107.png">

In the bin, there should be a bash file containing the tool, like picard. 

<img width="1166" alt="Screen Shot 2023-02-10 at 3 32 35 PM" src="https://user-images.githubusercontent.com/105939034/218214182-67b29f62-2691-412d-ba75-390df225bf62.png">

Open what should be the toolkit's bash file:

    vim picard

Below is a screenshot of what it looks like for picard in my DeepMosaic directory. 

<img width="1234" alt="Screen Shot 2023-02-10 at 3 34 57 PM" src="https://user-images.githubusercontent.com/105939034/218213874-2492f652-5e2c-4347-80b3-4c7a03c72e78.png">

At the bottom of the screenshot, you can see the java default memory settings. -Xms2048m sets my heap memory to 2,048 MB and -Xmx10g sets my maximum memory to 10 GB. These can be increased as needed.

## Create a Jupyter Kernel for a Custom Environment

It is not ideal to modify the base anaconda environment. In many cases you may not be able to, which is why we create custom environments. However, by default, Jupyter notebooks only interact with your base environment. If you should want to use something that's been installed on your custom environemt, like Biopython, you will need to create a new kernel. 

To do so, begin by activating your custom environment:

    conda activate your_env
    
Then run:
    
    conda install -c anaconda jupyter
    
Followed by:

    ipython kernel install --name your_env --user

After this, open Anaconda Navigator and launch Jupter Notebook. Near the top right of the browser window that opens, click the New dropdown menu and you should see the name of your environment in the list of available Kernels, like shown in the screenshot below:

<img width="236" alt="Screen Shot 2023-02-16 at 10 00 05 AM" src="https://user-images.githubusercontent.com/105939034/219435408-fde5256c-3825-4218-8f31-31eb8a8a590d.png">

Bioinformatics is the name of my custom environment.

## Convert FASTQ to FASTA format

Run

    sed -n '1~4s/^@/>/p;2~4p' INFILE.fastq > OUTFILE.fasta

## Remove Decoy Contigs from BAM/SAM/CRAM file

Run

    samtools view -o out.bam input.bam `seq 1 22 | sed 's/^/chr/'`
    
## If you encounter Device Busy when trying to delete a file or directory

Run 

    lsof +D /path

lsof stands for list open files. It will display a list in the terminal of files that are actively running, along with their corresponding Process ID.

Find the file that is preventing the delete, and kill the active process with:

    kill -9 PID

## Extract Data from a Corrupt Gzip file

If you need to extract data from a corrupted gzip file, like an incomplete VCF from HaplotypeCaller, then you can run this command:

    gunzip < corrupt_file.gz > corrupt_file.txt

For me, I ran this command:

    gunzip < WES_force_called_dilutions.vcf.gz > WES_force_called_dilutions.vcf

## Extract all CIGAR strings from BAM file

This command will create an output .txt file that contains the CIAGR strings from all reads in a BAM.

    samtools view your_bamfile.bam | cut -f 6 > your_textfile.txt

## Split Multiallelic Sites

If you need to split multiallelic sites into different rows, run this command:

    bcftools norm -N -m-any file.vcf.gz -o file_demulti.vcf.gz -O z -f ref.fa
