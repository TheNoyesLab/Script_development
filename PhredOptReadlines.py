import os
import sys
import gzip
import argparse
import glob
import sys
import gzip
import csv



#Website used to help optimize    https://stackify.com/20-simple-python-performance-tuning-tips/

##################HELPER FUNCTIONS##################

def parse_cmdline_params(cmdline_params):
    info = "Removes duplicate FASTQ entries from a FASTQ file"
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('-i', '--input_files', nargs='+', required=True,
                            help='Use globstar to pass a list of sequence files, (Ex: *.fastq.gz)')
    return parser.parse_args(cmdline_params)


###my_mean function can use Generators; much faster than numpy
def my_mean(data):
    n = 0
    mean = 0.0

    for x in data:
        n += 1
        mean += (x - mean)/n

    if n < 1:
        return float('nan');
    else:
        return mean

##################HELPER FUNCTIONS##################




#Extract Quality Scores and other sequence information
def pull_Phred(fastq_files):

    for f in fastq_files: # iterate through each fastq file
        Plist=[]
        Qlist=[]

        Seqlen_list=[]
        num_reads = 0

        fp = open(f, 'r') # open each fastq file;   gzip.open if .gz files
        numlines=sum(1 for line in fp)   #Count the number of lines
        fp.close()


        fp = open(f, 'r')  # open each fastq file;   gzip.open if .gz files
        Lines = fp.readlines()
        Lines = iter(Lines)

        for Li in range(int(numlines/4)):   # iterate through lines of fastq file
            Ordqual=[]

            read_id = next(Lines)
            seq = next(Lines)

            #seq = seq[10:len(seq)] # Let's not chop off the umi here since we would be checking the quality after UMI removal and not all samples have UMIs

            Seqlen_list.append(len(seq)-1)
            #newseq = seq + spacesep + UMI
            plus = next(Lines)
            qual = next(Lines)



            #Generator Expressions! Translate Quality Scores
            Ordqual=[ord(qual[i]) for i in range(len(qual)-1)]   #Change letters to numbers
            Q=[Ordqual[i]-33 for i in range(len(qual)-1)]       #Keep list for future use
            QGen=(Ordqual[i]-33 for i in range(len(qual)-1))    #Change numbers to qualities
            PGen=(10**(-Q[i]/10) for i in range(len(qual)-1))      #Change qualities to probabilities


            #Q=[Ordqual[i]-33 for i in range(len(qual)-1)]		#10-fold speedup w/generator
            #P=[10**(-Q[i]/10) for i in range(len(qual)-1)]		#10-fold speedup w/generator

            #For loop form!
            # for i in range(len(qual)-1): #Exclude the return character
            #     Ordqual.append(ord(qual[i]))
            #     Q.append(Ordqual[i]-33)
            #     P.append(10**(-Q[i]/10))


            Qlist.append(sum(QGen)/(len(seq) - 1))
            Plist.append(sum(PGen)/(len(seq) - 1))
            #print(timeit.timeit(lambda: Qlist.append(my_mean(Q))))
            #print(timeit.timeit(lambda: Plist.append(my_mean(P))))
            num_reads += 1

        QlistGen=iter(Qlist)
        PlistGen=iter(Plist)  #Make some super speedy iterators!
        Seqlen_listGen=iter(Seqlen_list)

        print(f,"mean_probability_nucleotide_error",sum(PlistGen)/len(Seqlen_list))
        print(f,"mean_phred_score",sum(QlistGen)/len(Seqlen_list))
        print(f,"total_reads",num_reads)
        print(f,"mean_read_length",sum(Seqlen_listGen)/len(Seqlen_list),"\n")


        ########################
        ########################Other Code for Benchmarking/Optimization
        ########################



                        ######TIME BENCHMARKING#####
        # print("Seqlist",timeit.timeit(lambda: numpy.mean(Seqlen_list),number=3))
        # print("Seqlist",timeit.timeit(lambda: sum(Seqlen_list)/len(Seqlen_list),number=3))
        # print("SeqlistGen",timeit.timeit(lambda: my_mean(Seqlen_listGen),number=1))
        # Seqlen_listGen=iter(Seqlen_list)
        # print("SeqlistGen2",timeit.timeit(lambda: sum(Seqlen_listGen)/len(Seqlen_list),number=1))
        #
        # print("Qlist",timeit.timeit(lambda: numpy.mean(Qlist),number=3))
        # print("Qlist",timeit.timeit(lambda: sum(Qlist)/len(Seqlen_list),number=3))
        # print("QlistGen",timeit.timeit(lambda: my_mean(QlistGen),number=1))
        # QlistGen=iter(QlistGen)
        # print("QlistGen2",timeit.timeit(lambda: sum(QlistGen)/len(Seqlen_list),number=1))
        #
        # print("Plist: ",timeit.timeit(lambda: numpy.mean(Plist),number=3))
        # print("Plist: ",timeit.timeit(lambda: sum(Plist)/len(Plist),number=3))
        # print("PlistGen",timeit.timeit(lambda: my_mean(PlistGen),number=1))
        # PlistGen=iter(PlistGen)
        # print("PlistGen2",timeit.timeit(lambda: sum(PlistGen)/len(Seqlen_list),number=1))
        #
        # print("Q",timeit.timeit(lambda: Ordqual[2]-33,number=3))
        # print("P",timeit.timeit(lambda: 10**(-Q[2]/10),number=3),"\n")
        #
        #
        # ##Comparing Generators vs List form
        # print("Qnumpy",numpy.mean(Q))
        # print("Qmymeany", my_mean(QGen))
        # print("QnumpyT",timeit.timeit(lambda: numpy.mean(Q),number=3))
        # print("QmymeanyT",timeit.timeit(lambda: my_mean(QGen),number=3))
                        ######TIME BENCHMARKING#####

        ########################
        ########################End Other Code for Benchmarking/Optimization
        ########################



        print(numlines)
        fp.close()









def print_dict(dict):
  # iterate through UMIs and repeat counts and print those
  dups= "Repeat UMI Error"
  for k, v in dict.items():
      if v != 1:
          print( k, dups, v)
      else:
          print(k, v)

def print_Rep(dict):
  # iterate through UMIs and repeat counts and print those
  dups= "Repeat UMI Error"
  for k, v in dict.items():
      if len(v) != 1:
          print(k, dups, v)
      else:
          print(k, v)


#Apply the previous functions; Print UMIs and counts
if __name__ == "__main__":
  opts = parse_cmdline_params(sys.argv[1:])
  fastq_files = opts.input_files

  pull_Phred(fastq_files)
