## The NCBI_scraper.py script is a rough version of a script that I used to perform web scraping on results from the NCBI Protein BLAST tool. 

The NCBI HTML is a mess, so traditional web scraping methods would not work. However, after extensive experimentation, I was able to get this script to download GenBank files from Protein BLAST search results. The GenBank files are then parsed to identify the protein of interest. Once the protein is identified, the script pulls key information related to the protein, such as AA sequence, species, data sequenced, etc. 

After gathering key data about each result from the Protein BLAST search, the script sorts the data into a CSV. The percent match to the source sequence is then calculated for each entry. The main goal of this script is to determine how much any given search result from the Protein BLAST tool has deviated from the source sequence. That information is later used to construct a cladogram. 

The results from this script were used in a larger study of a specific species of bacteria, not yet published. 
