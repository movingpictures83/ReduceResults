#!/usr/bin/python3.10

# Copyright (c) 2021 Christian Balbin
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

#import os
#import json
#import sqlite3
#import tempfile
#from functools import partial
#import subprocess
#from multiprocessing import Pool

#from rich.progress import track

#from epitopedia.app import config
#from epitopedia.app.blastparser import BLASTParser
#from epitopedia.app.config import console
#from epitopedia.app.hitparser import parseHit
#from epitopedia.app.MMCIFSeqs import MMCIFSeqs
from reduce import reduce_results
import sys
#from epitopedia.utils.utils import remove_previous_files

# from epitopedia.viz.serve import write_html, serve_html
#from epitopedia.app.args import args
#pdb_input_str = "6VXX_A"

inputfile = sys.argv[1]
###################################################################################################
#reduce_results(f"EPI_PDB_fragment_pairs_{pdb_input_str}.json")
reduce_results(f"{inputfile}")
###################################################################################################

####################################################################################################
#with open(f"{config.OUTPUT_DIR}/EPI_PDB_fragment_pairs_{pdb_input_str}_best.json") as input_handle:
#            data = json.load(input_handle)
#print(f"{config.OUTPUT_DIR}/EPI_PDB_fragment_pairs_{pdb_input_str}_best.json")
