# Rarefaction Plots 

This is a command-line tool to plot rarefaction subsampling data 

## Setup 

In order to use rfplot, the subsampling data should be stored in the form of .tsv files, each with two columns: the percent of the sample covered by the subsample and the corresponding number of unique features identified. 

Each sample should have five .tsv files: one each for gene, group, mech, type, class, and type. The form of a valid gene filename would be: `<samplename>.gene.tsv`. All of the .tsv files should be stored in one directory. 

## Usage 

Running rfplot requires Python 3 to be installed, along with the packages [matplotlib](https://pypi.org/project/matplotlib/) and [argparse](https://pypi.org/project/argparse/). 

The format of the rfplot command: 
```
python rfplot.py [-h] [-nd] dir sd 

positional arguments:
  dir         path to the directory with the sample files
  sd          path to directory in which to save output; enter "none" to not save
options:
  -h, --help  show this help message and exit
  -nd         no display: disables display of the generated graphs
```

The positional arguments are replaced by their corresponding values. 

## Examples 

Examples of command usage follow. Suppose a directory contains rfplot.py and two subdirectories: `data`, in which the .tsv files are stored, and `plots`, where the plots are to be saved. 

To generate graphs from the data in `data` and save to `plots` without displaying the output: 
```
python rfplot.py -nd ./data ./plots 
```

To generate graphs from the data and display without saving: 
```
python rfplot.py ./data none 
```

To generate graphs from the data and save in the parent directory with display: 
```
python rfplot.py ./data . 
```