## The NCBI_scraper.py script is a rough version of a script that I used to perform web scraping on NCBI Protein BLAST tool. 

The NCBI html is a mess, so tradiitonal web scraping methods would not work. However, after extensive experimentation, I was able to get this script to download genbank files from a Protein BLAST search results. The genbank files are then parsed to identify the protein of interest. Once the protein is identified, the script pulls key information related to the protein, such as AA sequence, species, data sequenced, etc.

The results from this script were used in a larger study of a specific species of bacteria, not yet published. 
