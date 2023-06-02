#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.parse, urllib.error
import re
import ssl
import sys, json
import calendar
import numpy as np
import pandas as pd
#pd.show_versions()
from Bio import Entrez
from Bio import SeqIO
import os


# In[162]:


#df = pd.read_csv('/Users/jonlusk/Desktop/borrelia_ncbi.csv')
#df = pd.read_csv('/Users/jonlusk/Downloads/Z7S5UA03016-Alignment-Descriptions.csv')
#species = 'Borrelia'
#species = 'Borreliella'
#species = 'Leptospira'
species = 'Treponema'
df_pull = pd.read_csv('/Users/jonlusk/Downloads/'+species+'-Alignment-Descriptions.csv')
#df_pull= pd.read_csv('/Users/jonlusk/Downloads/0W6K3K7301N-Alignment-Descriptions.csv')
df_pull


# In[163]:


df_pull[['hyperlink', 'Accession Val']] = df_pull['Accession  '].str.split(',', expand=True)
df_pull[['quote1','Accession Values','quote2']] = df_pull['Accession Val'].str.split('"', expand=True)
df_pull


# In[164]:


df_pull.to_csv('/Users/jonlusk/Desktop/'+species+'_descriptions_with_accession_values.csv')


# In[165]:


accession_list = list(df_pull['Accession Values'])
print(accession_list)
print(len(accession_list))


# In[166]:


locus = []


for i in range(len(accession_list)):
    url_ipg = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=ipg&retmode=xml&rettype=gb&id=acc"
    
    seq = str(accession_list[i])
    url_mod = url_ipg.replace('acc', str(accession_list[i]))

    response = requests.get(url_mod)
    with open('feed.xml', 'wb') as file:
        file.write(response.content)
    
    df = pd.read_csv('feed.xml', delimiter='\t')
    df.rename(columns={"<?xml version=\"1.0\" encoding=\"UTF-8\"  ?>": "total"}, inplace=True)
    #df
    
    
    df2 = pd.DataFrame()
    df2 = df['total'][6]
    split = df2.split(" ")
    #split_2 = split.str.split("/")

    print(split)

    assembly = []

    for i in split:
        #print(i)
        #i.split('/')
        #print(i)
        if 'accver' in i:
            print(i)
            assembly.append(i)
    print(assembly)
    df3 = pd.DataFrame(assembly)
    print(df3)
    
    #df3[['accver','locus','end']] = df[0].str.split('"', expand=True)
    
    df3[['accver','locus','end']] = df3[0].str.split('"', expand=True)
    print(df3)

    #locus = []

    x = df3['locus'][0]

    print(x)
    
    locus.append(x)


# In[167]:


print(len(locus))


# In[169]:


records = []
for i in range(len(locus)):
    Entrez.email = 'jonathan.pitsch@cuanschutz.edu'
    Entrez.tool = "Biopython_NCBI_Entrez_downloads.ipynb"
    handle = Entrez.efetch(db="nuccore", rettype="gbwithparts", retmode="text",
                          id=locus[i])
    #url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&retmode=xml&rettype=gb&id=seq"
#    handle = Entrez.efetch(db="protein", rettype="gb", retmode="xml",
 #                         id=accession_list[i])
#    print(handle)
    records.append(SeqIO.read(handle, 'genbank'))
    SeqIO.write(records[i], os.path.join('/Users/jonlusk/Downloads/genbank files', species+'_'+str(locus[i])+'_'+str(i)+".gbk"), "genbank")
    
    
    
    


# In[170]:


def get_source_feature_with_qualifier_value(seq_record):
    
    
    for feature in genome_record.features:
        if feature.type == 'source':
            return feature.qualifiers


# In[180]:


source_muts2_prot = []
source_muts2_AA_Seq = []
genome_description = []
host_org = []
country_list = []
collection_date = []
collected_by = []
isolation_source = []
strain = []


for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Downloads/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")
    des = genome_record.description
    #print(genome_record)
    genome_description.append(des)
    #for p in product:
        #genome_record = SeqIO.read("/Users/jonlusk/Desktop/borrelia_CP000395.gbk", "genbank")
        #cds_feature = get_cds_feature_with_qualifier_value(genome_record, "old_locus_tag", "ECA0662")
    for j in range(0,1): #muts2
        source_feature = get_source_feature_with_qualifier_value(genome_record)
        if source_feature == None:
            print("NO CDS HERE")
            #prot_id == 'NaN'
            y = 'N/A'
            source_muts2_prot.append(y)
            x = 'NaN'
            source_muts2_AA_Seq.append(x)
            continue
        else:
            print(len(source_feature.keys()))
            print(source_feature.keys())
            print(len(source_feature))
            print(source_feature)
            my_list = [elem[0] for elem in source_feature.values()]
            print(str(source_feature.values()))
            df = pd.DataFrame.from_dict(source_feature, orient='index').T
            print(my_list)
            #df = pd.DataFrame()
            #df = pd.DataFrame(source_feature, columns=source_feature.keys())
            #print(df)
            try:
                host = df['host'][0]
                host_org.append(host)
            except:
                host = 'N/A'
                host_org.append(host)
            try:
                stra = df['strain'][0]
                strain.append(stra)
            except:
                stra = 'N/A'
                strain.append(stra)
            try:
                countr = df['country'][0]
                country_list.append(countr)
            except:
                countr = 'N/A'
                country_list.append(host)
            try:
                coll_date = df['collection_date'][0]
                collection_date.append(coll_date)
            except:
                coll_date = 'N/A'
                collection_date.append(coll_date)
            try:
                coll_by = df['collected_by'][0]
                collected_by.append(coll_by)
            except:
                coll_by = 'N/A'
                collected_by.append(coll_by)
            try:
                iso_source = df['isolation_source'][0]
                isolation_source.append(iso_source)
            except:
                iso_source = 'N/A'
                isolation_source.append(iso_source)


# In[173]:


def get_cds_feature_with_qualifier_value(seq_record, name, value):
    entry_id = []
    descript = []
    """Function to look for CDS feature by annotation value in sequence record.
    
    e.g. You can use this for finding features by locus tag, gene ID, or protein ID.
    """
    # Loop over the features
    #print(genome_record.id)
    #entry_id.append(genome_record.id)
    #print(genome_record.description)
    #print(genome_record.annotations)
    #anno = list(genome_record.annotations.items())
    #print(anno)
    #df_anno = pd.DataFrame(anno)
    #print(df_anno)
    #print(genome_record.seq)
    for feature in genome_record.features:
        if feature.type == 'CDS' and value in feature.qualifiers.get(name, []):
            #print(feature)
            entry_id.append(genome_record.id)
            descript.append(genome_record.description)
            return feature.qualifiers


# In[174]:


muts2 = ['endonuclease MutS2']

muts2_prot = []
muts2_AA_Seq = []
genome_description = []


for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Downloads/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")
    des = genome_record.description
    genome_description.append(des)
    
    
    for j in muts2:
        cds_feature = get_cds_feature_with_qualifier_value(genome_record, "product", j)
        if cds_feature == None:
            print("NO CDS HEREEEEEEEE")
            #prot_id == 'NaN'
            y = 'N/A'
            muts2_prot.append(y)
            x = 'NaN'
            muts2_AA_Seq.append(x)
            continue
        else:
            print(len(cds_feature.keys()))
            df = pd.DataFrame.from_dict(cds_feature, orient='index').T
            print(df)
            #if df['product'].str.contains('mutS2').any() or df['product'].str.contains('MutS2').any():
            if df['product'].str.contains('MutS2').any():
                prot_id = df['protein_id'][0]
                muts2_prot.append(prot_id)
                x = df['translation'][0]
                muts2_AA_Seq.append(x)


# In[186]:


muts2 = ['endonuclease MutS2']
muts = ['DNA mismatch repair protein mutS']
Muts = ['DNA mismatch repair protein MutS']

muts_prot = []
muts_AA_Seq = []

for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Downloads/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")
    
    
    for j in muts:
        cds_feature = get_cds_feature_with_qualifier_value(genome_record, "product", j)
        if cds_feature == None:
            print("NO CDS HEREEEEEEEE")
            #prot_id == 'NaN'
            y = 'NA'
            muts_prot.append(y)
            x = 'NaN'
            muts_AA_Seq.append(x)
            continue
        else:
            print(len(cds_feature.keys()))
            df = pd.DataFrame.from_dict(cds_feature, orient='index').T
            print(df)
            #if df['product'].str.contains('mutS2').any() or df['product'].str.contains('MutS2').any():
            if df['product'].str.contains('mutS').any():
                prot_id = df['protein_id'][0]
                muts_prot.append(prot_id)
                x = df['translation'][0]
                muts_AA_Seq.append(x)
    
        #print(cds_feature)


# In[187]:


muts2 = ['endonuclease MutS2']
muts = ['DNA mismatch repair protein mutS']
Muts = ['DNA mismatch repair protein MutS']


Muts_prot = []
Muts_AA_Seq = []

for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Downloads/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")

    for j in Muts:
            cds_feature = get_cds_feature_with_qualifier_value(genome_record, "product", j)
            if cds_feature == None:
                print("NO CDS HEREEEEEEEE")
                #prot_id == 'NaN'
                y = 'NA'
                Muts_prot.append(y)
                x = 'NaN'
                Muts_AA_Seq.append(x)
                continue
            else:
                print(len(cds_feature.keys()))
                df = pd.DataFrame.from_dict(cds_feature, orient='index').T
                print(df)
                #if df['product'].str.contains('mutS2').any() or df['product'].str.contains('MutS2').any():
                if df['product'].str.contains('MutS').any():
                    try:
                        prot_id = df['protein_id'][0]
                        Muts_prot.append(prot_id)
                        x = df['translation'][0]
                        Muts_AA_Seq.append(x)
                    except:
                        prot_id = 'N/A'
                        Muts_prot.append(prot_id)
                        x = 'N/A'
                        Muts_AA_Seq.append(x)
                        
                        
                        
                        
                        
                        


# In[188]:


muts2 = ['endonuclease MutS2']
muts = ['DNA mismatch repair protein mutS']
Muts = ['DNA mismatch repair protein MutS']
Muts2 = ['MutS2 protein']


Muts2_prot = []
Muts2_AA_Seq = []

for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Downloads/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")

    for j in Muts2:
            cds_feature = get_cds_feature_with_qualifier_value(genome_record, "product", j)
            if cds_feature == None:
                print("NO CDS HEREEEEEEEE")
                #prot_id == 'NaN'
                y = 'NA'
                Muts2_prot.append(y)
                x = 'NaN'
                Muts2_AA_Seq.append(x)
                continue
            else:
                print(len(cds_feature.keys()))
                df = pd.DataFrame.from_dict(cds_feature, orient='index').T
                print(df)
                #if df['product'].str.contains('mutS2').any() or df['product'].str.contains('MutS2').any():
                if df['product'].str.contains('MutS2').any():
                    try:
                        prot_id = df['protein_id'][0]
                        Muts2_prot.append(prot_id)
                        x = df['translation'][0]
                        Muts2_AA_Seq.append(x)
                    except:
                        prot_id = 'N/A'
                        Muts2_prot.append(prot_id)
                        x = 'N/A'
                        Muts2_AA_Seq.append(x)


# In[189]:


muts2 = ['endonuclease MutS2']
muts = ['DNA mismatch repair protein mutS']
Muts = ['DNA mismatch repair protein MutS']
Muts2 = ['MutS2 protein']
smr = ['Smr/MutS family protein']


smr_prot = []
smr_AA_Seq = []

for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Downloads/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")

    for j in smr:
            cds_feature = get_cds_feature_with_qualifier_value(genome_record, "product", j)
            if cds_feature == None:
                print("NO CDS HEREEEEEEEE")
                #prot_id == 'NaN'
                y = 'NA'
                smr_prot.append(y)
                x = 'NaN'
                smr_AA_Seq.append(x)
                continue
            else:
                print(len(cds_feature.keys()))
                df = pd.DataFrame.from_dict(cds_feature, orient='index').T
                print(df)
                #if df['product'].str.contains('mutS2').any() or df['product'].str.contains('MutS2').any():
                if df['product'].str.contains('Smr/MutS').any():
                    try:
                        prot_id = df['protein_id'][0]
                        smr_prot.append(prot_id)
                        x = df['translation'][0]
                        smr_AA_Seq.append(x)
                    except:
                        prot_id = 'N/A'
                        smr_prot.append(prot_id)
                        x = 'N/A'
                        smr_AA_Seq.append(x)


# In[154]:


print(len(Muts2_prot))


# In[148]:


muts2 = ['endonuclease MutS2']
muts = ['DNA mismatch repair protein mutS']
Muts = ['DNA mismatch repair protein MutS']
hypo = ['hypothetical protein']


hypo_prot = []
hypo_AA_Seq = []

for i in range(len(locus)):
    genome_record = SeqIO.read("/Users/jonlusk/Desktop/genbank files/"+species+'_'+str(locus[i])+'_'+str(i)+".gbk", "genbank")

    for j in hypo:
            cds_feature = get_cds_feature_with_qualifier_value(genome_record, "product", j)
            if cds_feature == None:
                print("NO CDS HEREEEEEEEE")
                #prot_id == 'NaN'
                y = 'NA'
                hypo_prot.append(y)
                x = 'NaN'
                hypo_AA_Seq.append(x)
                continue
            else:
                print(len(cds_feature.keys()))
                df = pd.DataFrame.from_dict(cds_feature, orient='index').T
                print(df)
                #if df['product'].str.contains('mutS2').any() or df['product'].str.contains('MutS2').any():
                if df['product'].str.contains('hypothetical protein').any():
                    try:
                        prot_id = df['protein_id'][0]
                        hypo_prot.append(prot_id)
                        x = df['translation'][0]
                        hypo_AA_Seq.append(x)
                    except:
                        prot_id = 'N/A'
                        hypo_prot.append(prot_id)
                        x = 'N/A'
                        hypo_AA_Seq.append(x)
                        


# In[155]:


print(len(hypo_prot))


# In[190]:


#df_ncbi = pd.read_csv('/Users/jonlusk/Desktop/borrelia_ncbi.csv')
df_ncbi = pd.read_csv('/Users/jonlusk/Desktop/'+species+'_descriptions_with_accession_values.csv')


# In[191]:


#print(host_org)


# In[192]:


df_ncbi_mass_pull = pd.DataFrame()
df_ncbi_mass_pull['Scientific Name'] = df_ncbi['Scientific Name']
df_ncbi_mass_pull['Strain'] = strain
df_ncbi_mass_pull['NCBI Accession Locus'] = locus
df_ncbi_mass_pull['Country Isolated In'] = country_list
df_ncbi_mass_pull['Collection Date'] = collection_date
df_ncbi_mass_pull['Collected By'] = collected_by
df_ncbi_mass_pull['Host Organism'] = host_org
df_ncbi_mass_pull['Isolation Source'] = isolation_source
df_ncbi_mass_pull['Percent Identitcal'] = df_pull['Per. ident']
df_ncbi_mass_pull['protein ID: endonuclease MutS2'] = muts2_prot
df_ncbi_mass_pull['AA Sequence: endonuclease MutS2'] = muts2_AA_Seq
df_ncbi_mass_pull['protein ID: DNA mismatch repair protein mutS'] = muts_prot
df_ncbi_mass_pull['AA Sequence: DNA mismatch repair protein mutS'] = muts_AA_Seq
df_ncbi_mass_pull['protein ID: DNA mismatch repair protein MutS'] = Muts_prot
df_ncbi_mass_pull['AA Sequence: DNA mismatch repair protein MutS'] = Muts_AA_Seq
df_ncbi_mass_pull['protein ID: MutS2 Protein'] = Muts2_prot
df_ncbi_mass_pull['AA Sequence: MutS2 Protein'] = Muts2_AA_Seq
df_ncbi_mass_pull['protein ID: Smr/MutS family protein'] = smr_prot
df_ncbi_mass_pull['AA Sequence: Smr/MutS family protein'] = smr_AA_Seq

print(df_ncbi_mass_pull)


# In[193]:


url_seq = 'https://www.ncbi.nlm.nih.gov/nuccore/seq'

seq_url = []

for i in range(len(locus)):
    seq = str(locus[i])
    url_mod = url_seq.replace('seq', str(locus[i]))
    print(url_mod)
    seq_url.append(url_mod)


# In[194]:


df_ncbi_mass_pull['NCBI GenBank URL'] = seq_url


# In[195]:


df_ncbi_mass_pull.to_csv('/Users/jonlusk/Desktop/NCBI_'+species+'_mass_pull_new.csv', index=False)


# In[ ]:





# In[ ]:





# In[186]:


import pandas as pd

from Bio.Seq import Seq 

from Bio import pairwise2

from Bio.pairwise2 import format_alignment

from Bio import pairwise2


# In[251]:


control = 'MQDEQDKYLKNIDFYEILSLVSKYVSNPDTVNLLSNQKILKTKESLEKIFSFVSLIRMLFESCKGYPNSFINSLKYPISLLLKENSRVSIENLRDIIVFLDEVLRINLFLHKNSDIKHLNVQILSDLLFLNPELKNLLNELKEHIDVDALELKSGVVKEYDSIEFEIKNLNRRVENQIKKIISLNAEYLTSNFVCYKSNKYTLALKSNFKGKIKGNIISISSSGETFYIEPNDIVNANNRLNYLSLEKERIILKILRNLSAKVHSNIVLLDNLYNNFLYYDSLKARAIYGIKTKGVFPEISNVLNIFDAHHPLLKDSKAITFTPAENRVVIITGPNAGGKTVTLKTIGLLSAMFQFGIPIVVGESSTFKIFDNIFIDIGDEQSISNSLSTFSSHMSNISYILKHTTKDSLVIFDEFCSGTDIDQGQALAISILEYLININSYVLISTHYNALKYFAYTHEGVVNASMRMDLETMQPNYNLIFSIPGESYAFNVASKALIDRSIVIRANEIYSSQKTEINEILEKLIEKEKDLLLIKESMDKKLIQIELQEKELENFYQDLLLREKNIETKLLNEQNEFLKNSRKVLENLVREIKEGNINVAKNKAFISDLEKNVDLKTNKVNSLNNKRNVVADFKIGDKVRIVNSNAKGKIVGISKKKITVNVGAFNVSVSSSEISLENFKEKKENGKNFNFSIDYNKENLLSFTIDIRGMRSVDALDFLNKKIDNIILNGINKFEIIHGKGEGHLMREVHNLLKELKFIRKYYFAHPSDGGSGKTIVEI'

muts2 = 'MSEHYEALNTPVMRQYMEVKEQHPDGIVFFRMGDFYEMFLDDAKIAAQILDITLTKRQNQIPMAGIPYHATESYISRLIAAGKKVVVCEQTKPDDPKAKIMSREVVRIITPGTVVEDNLLGGYQNNYLSLYYKEKTSVYLAFADVSTSELLYFFFSENETERINDTIKRFSPKEIIFTDEIPPIAKESKIILSKIPQDYLPKKRGAGIDTVVHVLDAYLQYNYRKQNFVFQSPRRIDESEYLVLDEQTVSHLELVDNPNDKNHTLFAVLNRCITATGKRYLKQRILFPTRDENKIKAHWDKIEILSANKKKDSKSKNY'

muts22 = 'DNIILNGINKFEIIHGKGEGHLMREVHNLLKELKFIRKYYFAHPSDGGSGKTIVEI'


# In[252]:


alignments = pairwise2.align.globalxx(control, muts2, score_only=True)
alignments = pairwise2.align.globalxx(control, muts22, score_only=True)
print(alignments)
#for alignment in alignments:
#    print(format_alignment(*alignment))


# In[253]:


score = alignments/len(control)*100
print(score)


# In[173]:


#df_new = pd.read_csv('/Users/jonlusk/Downloads/Re_ NCBI Scraper - Strain column added/NCBI_Borrelia_mass_pull_new_with_percentmatch.csv')
#df_new = df_new = pd.read_csv('/Users/jonlusk/Downloads/Re_ NCBI Scraper - Strain column added/NCBI_Borreliella_mass_pull_new_with_percentmatch.csv')
#df_new = df_new = pd.read_csv('/Users/jonlusk/Downloads/Re_ NCBI Scraper - Strain column added/NCBI_Leptospira_mass_pull_new_with_percentmatch.csv')
df_new = df_new = pd.read_csv('/Users/jonlusk/Downloads/Re_ NCBI Scraper - Strain column added/NCBI_Treponema_mass_pull_new_with_percentmatch.csv')

df_new


# In[85]:


control = 'MQDEQDKYLKNIDFYEILSLVSKYVSNPDTVNLLSNQKILKTKESLEKIFSFVSLIRMLFESCKGYPNSFINSLKYPISLLLKENSRVSIENLRDIIVFLDEVLRINLFLHKNSDIKHLNVQILSDLLFLNPELKNLLNELKEHIDVDALELKSGVVKEYDSIEFEIKNLNRRVENQIKKIISLNAEYLTSNFVCYKSNKYTLALKSNFKGKIKGNIISISSSGETFYIEPNDIVNANNRLNYLSLEKERIILKILRNLSAKVHSNIVLLDNLYNNFLYYDSLKARAIYGIKTKGVFPEISNVLNIFDAHHPLLKDSKAITFTPAENRVVIITGPNAGGKTVTLKTIGLLSAMFQFGIPIVVGESSTFKIFDNIFIDIGDEQSISNSLSTFSSHMSNISYILKHTTKDSLVIFDEFCSGTDIDQGQALAISILEYLININSYVLISTHYNALKYFAYTHEGVVNASMRMDLETMQPNYNLIFSIPGESYAFNVASKALIDRSIVIRANEIYSSQKTEINEILEKLIEKEKDLLLIKESMDKKLIQIELQEKELENFYQDLLLREKNIETKLLNEQNEFLKNSRKVLENLVREIKEGNINVAKNKAFISDLEKNVDLKTNKVNSLNNKRNVVADFKIGDKVRIVNSNAKGKIVGISKKKITVNVGAFNVSVSSSEISLENFKEKKENGKNFNFSIDYNKENLLSFTIDIRGMRSVDALDFLNKKIDNIILNGINKFEIIHGKGEGHLMREVHNLLKELKFIRKYYFAHPSDGGSGKTIVEI'

print(len(control))


# In[180]:


count = []

for i in range(len(df_new['% Match Borreliella MutS2 Sequence: endonuclease MutS2'])):
    try:
        x = df_new['% Match Borreliella MutS2 Sequence: endonuclease MutS2'][i]*(len(df_new['AA Sequence: endonuclease MutS2'][i])/100)
        #print(int(x))
        y = int(x)
        #print(y/len(control))
        #y/len(control)
        count.append(y)
        #print(len(df_new['AA Sequence: endonuclease MutS2'][i]))
    except:
        y = 0
        #print(y/len(control))
        count.append(y)
        pass
print(count)


# In[6]:


count = []

for i in range(len(df_new['% Match Borreliella MutS2 Sequence: endonuclease MutS2'])):
    try:
        x = df_new['% Match Borreliella MutS2 Sequence: DNA mismatch repair protein mutS'][i]*(len(df_new['AA Sequence: DNA mismatch repair protein mutS'][i])/100)
        #print(int(x))
        y = int(x)
        count.append(y)
        #print(len(df_new['AA Sequence: endonuclease MutS2'][i]))
    except:
        y = 0
        count.append(y)
        pass
print(count)


# In[7]:


count = []

for i in range(len(df_new['% Match Borreliella MutS2 Sequence: endonuclease MutS2'])):
    try:
        x = df_new['% Match Borreliella MutS2 Sequence: DNA mismatch repair protein mutS'][i]*(len(df_new['AA Sequence: DNA mismatch repair protein mutS'][i])/100)
        #print(int(x))
        y = int(x)
        count.append(y)
        #print(len(df_new['AA Sequence: endonuclease MutS2'][i]))
    except:
        y = 0
        count.append(y)
        pass
print(count)


# In[8]:


for (colname,colval) in df_new.iteritems():
    print(colname, colval.values)


# In[174]:


match = []
name = []
protein = []
AA = []
best_match = []
best_name = []
best_prot = []
best_AA = []

for i in range(len(df_new['Strain'])):
    for j in df_new.columns:
        #print(column)
        if '%' in j:
            #name.append(j)
            #print(column)
            x = df_new[j][i]
            match.append(x)
            #print(x)
        if 'protein ID' in j:
            y = df_new[j][i]
            name.append(j)
            protein.append(y)
        if 'AA Sequence' in j:
            z = df_new[j][i]
            AA.append(z)
    z = max(match)
    best_match.append(z)
    best_match_index = match.index(max(match))
    g = name[best_match_index]
    best_name.append(g)
    p = protein[best_match_index]
    best_prot.append(p)
    a = AA[best_match_index]
    best_AA.append(a)

    match.clear()
    name.clear()
    protein.clear()
    AA.clear()
            #match = []
            #name = []
            
            
            #for k in range(len(match)):
            #    z = match[k]
            #    if z < match[k+1]:
            #        z = match[k+1]
            ##        highest_name = name[k]
            #        best_match.append(z)
            #        best_name.append(highest_name)
            #    else:
            #        z = k
            #        highest_name = name[k]
            #        best_match.append(z)
            #        best_name.append(highest_name)
    
    #best_match = max(match)
    #print(best_match)
    #name_highest = 
#match = []
#name = []
#print(match)
            #break
            #y = df_new[column+3][i]
            
            #print(x)
            #print(y)
            #if x 
            #y = x
            
            
            


# In[175]:


#print(best_match)
##print(len(best_match))
#print(best_name)
#print(len(best_name))


# In[176]:


#best_name.replace('')


# In[177]:


#df_new['Full Name'] = best_name
df_new['Best Match Product'] = best_name
df_new['% Match of Best Match'] = best_match
df_new['Best Match Protein ID'] = best_prot
df_new['Best Match AA'] = best_AA


# In[178]:


df_new


# In[63]:


df_new[['% match','Name of Best Match']] = df_new['Full Name'].str.split(':', expand=True)

df_new


# In[131]:


df_drop = df_new.drop(['Full Name', '% match'], axis=1)

df_drop


# In[179]:


#df_drop.to_csv('/Users/jonlusk/Desktop/NCBI_Treponema_mass_pull_new_with_bestmatch.csv')
#df_new.to_csv('/Users/jonlusk/Desktop/NCBI_Borrelia_mass_pull_new_with_bestmatch_new.csv')
#df_new.to_csv('/Users/jonlusk/Desktop/NCBI_Borreliella_mass_pull_new_with_bestmatch_new.csv')
#df_new.to_csv('/Users/jonlusk/Desktop/NCBI_Leptospira_mass_pull_new_with_bestmatch.csv')
#df_new.to_csv('/Users/jonlusk/Desktop/NCBI_Treponema_mass_pull_new_with_bestmatch.csv')


# In[ ]:




