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


def pull_UMI(fastq_files):
	dict = {} # initialize dictionary
	linenum = [0]
	UMIloc = {} #Dictionary of locations (used to append UMI repeat count)
	#spacesep = " | "
	#data = {} #Initialize file (list lines)


  	for f in fastq_files: # iterate through each fastq file
  		fp = open(f, 'r') # open each fastq file;   gzip.open if .gz files
  		for line in fp:   # iterate through lines of fastq file
  			read_id = line
  			seq = fp.next()


			#################SEARCH FOR UMI INFORMATION############
			UMI = seq[1:10]
  			if UMI not in dict: #is UMI in dictionary, if not, set counter to 1
  				dict[UMI] = 1
				UMIloc[UMI] = [] #Create empty list of locations
  			else: # if we've already seen UMI, add to the counter
  				dict[UMI] += 1


			UMIloc[UMI] = UMIloc[UMI] + linenum	#append location of UMI

			#################SEARCH FOR UMI INFORMATION############

			seq = seq[10:len(seq)] #Chop off UMI
			#newseq = seq + spacesep + UMI
  			plus = fp.next()
  			qual = fp.next()



			linenum[0] += 1	#Increase linenumber (read number, really...)

#+ spacesep + str(dict[UMI])


  		fp.close()
	return dict, UMIloc





#

spacesep = " | "



def ReWriter(fastq_files):

	BigDict = pull_UMI(fastq_files)[0]
	KeyDict = pull_UMI(fastq_files)[1]

	#Or if you want only repeats labeled...
	#KeyDict = dict(filter(lambda elem: len(elem[1]) != 1, pull_UMI(fastq_files)[1].items() ))

 	for f in fastq_files: # iterate through each fastq file
		with open(f,'r') as file:
			Lines = file.readlines()

		#Loop through the values (and their own list elements)
		for i in range(len(KeyDict.values())):
			for j in range(len(KeyDict.values()[i])):
				SeqLoc = KeyDict.values()[i][j]*4+1	#Exact line of the relevant sequence

				seq = Lines[SeqLoc][10:len(Lines[SeqLoc])-1] 		#Remove UMI and Newline
				#Replace Sequence Line with new sequence
				Lines[SeqLoc] = seq + spacesep + str(KeyDict.keys()[i]) + spacesep + str(BigDict[ KeyDict.keys()[i] ]) + "\n"

		newf = "new" + f
		with open(newf,'w+') as file1:
			file1.writelines( Lines )








def print_dict(dict):
  # iterate through UMIs and repeat counts and print those
  dups= "Repeat UMI Error"
  for k, v in dict.items():
	  if v != 1:
		  print k, dups, v
	  else:
	  	print k, v

def print_Rep(dict):
  # iterate through UMIs and repeat counts and print those
  dups= "Repeat UMI Error"
  for k, v in dict.items():
	  if len(v) != 1:
		  print k, dups, v
	  else:
	  	print k, v


#Apply the previous functions; Print UMIs and counts
if __name__ == "__main__":
  opts = parse_cmdline_params(sys.argv[1:])
  fastq_files = opts.input_files
  #read_dic = pull_UMI(fastq_files)
  #print_dict(read_dic[0])
  #print_Rep(read_dic[1])
  ReWriter(fastq_files)
  #print ReWriter(read_dic[1])
