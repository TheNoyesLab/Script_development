import matplotlib.pyplot as plt 
import csv 
import os 
import argparse 

# TODO: Add Shebang line? 

# retrieves the command-line arguments and flags 

parser = argparse.ArgumentParser(description='Generates rarefaction feature graphs for given subsampling data', 
                                 usage='python %(prog)s [-h] [-nd] dir sd') 

parser.add_argument('dir', type=str, help='path to the directory with the sample files')
parser.add_argument('sd', type=str, help='path to directory in which to save output; enter "none" to not save')
parser.add_argument('-nd', action='store_true', help='no display: disables display of the generated graphs')

args = parser.parse_args()

# empty initializations that are later filled with values 
types, data, names = [], [], []

# gets data from sample files in directory 

dir = args.dir if args.dir[-1] == '/' else args.dir + '/' 

for fn in os.listdir(dir): 

    f = fn.split('.') # subdivides string at . in filename 

    if (f[-1] != 'tsv'): # ensures the file is a .tsv
        continue
    
    if f[0] not in names: 
        names.append(f[0]) # adds the sample name to the list 

    # adds the feature type to the list 
    if f[-2] not in types: 
        types.append(f[-2])
        data.append([[],[]]) 
        x, y = data[-1][0], data[-1][1]
    else: 
        i = types.index(f[-2])
        x, y = data[i][0], data[i][1] 

    # adds a new empty list to the feature type for the sample 
    x.append([])
    y.append([])

    # writes the data from the file to the list 
    with open(dir + fn) as file: 
        tsv = csv.reader(file, delimiter='\t')
        for i in tsv: 
            x[-1].append(int(i[0]))
            y[-1].append(int(i[1]))

# displays retrieved data using PyPlot

sps = [] 
for i in range (len(data)): 
    sps.append(plt.subplots()) # creates a list of tuples with the figure and axes objects

# plots the data from each sample list 
for d in range(len(data)): 
    for i in range (len(names)): 
        sps[d][1].plot(data[d][0][i], data[d][1][i], label=names[i])

    # sets the graph formatting 

    sps[d][1].set_xlabel('% of data subsampled')
    sps[d][1].set_ylabel('unique features identified')
    sps[d][1].legend(bbox_to_anchor=(1.05,1.0), loc='upper left')
    sps[d][1].set_xlim(left=0) 
    sps[d][1].set_ylim(bottom=0)

    sps[d][0].set_facecolor('white')
    sps[d][0].set_tight_layout(True) 

    # sets the graph titles 
    
    sps[d][1].set_title(f'{types[d]} Subsampling Features')

# displays graphing windows 
if (not args.nd): 
    plt.show() 

# saves the plots x 
if args.sd != 'none': 
    sd = args.sd if args.sd[-1] == '/' else args.sd + '/'  

    for d in range(len(data)): 
        sps[d][0].savefig(f'{sd}{types[d]}.png')