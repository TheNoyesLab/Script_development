import os
import sys
import gzip
import argparse
import glob
import time
import platform
import multiprocessing
from multiprocessing import Pool

    ###Parsing command line prompts###
def parse_cmdline_params(cmdline_params):
    info = "Removes duplicate FASTQ entries from a FASTQ file"
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('-i', '--input_files', nargs='+', required=True,
                            help='Use globstar to pass a list of sequence files, (Ex: *.fastq.gz)')
    return parser.parse_args(cmdline_params)
    ###Parsing command line prompts###



def multi_func(q):  #Collect Q information  #Function to run in parallel
    nucLen = len(q) - 1	    #The length of the sequence; exclude new line character

    Q_scores = [ord(q[i]) - 33 for i in range(nucLen)]   #Translate to numbers and subtract 33
    Prob = (10 ** (-Q_scores[i] / 10) for i in range(nucLen))   #Convert Q to Probabilities

    #Extract the mean Q and P and Read Length for each Read
    return sum(Q_scores) / nucLen, sum(Prob) / nucLen, nucLen



#Extract Quality Scores and other sequence information
def Pull_Phred(fastq_files):
    for f in fastq_files: # iterate through each fastq file
        p = Pool(6)       #multiprocessing.cpu_count())
        fp = open(f, 'r')

        Lines = fp.readlines()
        Line4 = Lines[3::4] #Every 4th line (Quality scores) starting with line 4 (index 3)
        readnum=len(Line4) #number of reads in file

        res = p.map(multi_func, Line4)


        qs = (listy[0] for listy in res) #Extract Q's as 1st element
        ps = (listy[1] for listy in res) #Extract P's as 2nd element
        readlen = (listy[2] for listy in res) #Extract read length as 3rd element

        print("\n Number of Reads = ", readnum)
        print("Mean Quality Score = ",sum(qs) / readnum)
        print("Mean Probability of Error = ",sum(ps) / readnum)
        print("Mean readlength = ", sum(readlen) / readnum)

    fp.close()


if __name__ == '__main__':
    opts = parse_cmdline_params(sys.argv[1:])
    fastq_files = opts.input_files  #parse input files

    Pull_Phred(fastq_files) #run Phred collection
