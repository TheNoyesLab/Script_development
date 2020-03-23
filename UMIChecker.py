import os
import sys
import gzip
import argparse
import glob
import sys
import gzip
import csv

def parse_cmdline_params(cmdline_params):
	info = "Removes duplicate FASTQ entries from a FASTQ file"
	parser = argparse.ArgumentParser(description=info)
	parser.add_argument('-i', '--input_files', nargs='+', required=True,
        	                help='Use globstar to pass a list of sequence files, (Ex: *.fastq.gz)')
	return parser.parse_args(cmdline_params)


def pull_read_headers(fastq_files):
  dict = {} # initialize dictionary
  for f in fastq_files: # iterate through each fastq file
  	fp = open(f, 'r') # open each fastq file;   gzip.open if .gz files
  	for line in fp:   # iterate through lines of fastq file
  		read_id = line
  		seq = fp.next()
  		UMI = seq[1:10]
  		plus = fp.next()
  		qual = fp.next()
  		if UMI not in dict: #is UMI in dictionary, if not, set counter to 1
  			dict[UMI] = 1
  		else: # if we've already seen UMI, add to the counter
  			dict[UMI] += 1
  	fp.close()
  return dict

def print_dict(dict):
  # iterate through UMIs and repeat counts and print those
  for k, v in dict.items():
	  print k, v


#Apply the previous functions; Print UMIs and counts
if __name__ == "__main__":
  opts = parse_cmdline_params(sys.argv[1:])
  fastq_files = opts.input_files
  read_dic = pull_read_headers(fastq_files)
  print_dict(read_dic)
