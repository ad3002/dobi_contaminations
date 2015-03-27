#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 16.03.2015
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import os
from settings import settings
from data_loader import get_genome_eu_files
from PyExp import runner
from PyExp import sc_iter_filepath_folder


def _checker(jf_file, settings, kmer_file, unlink=True):

    
    freq_file = "%s.freq.dat" % jf_file
    command = "cat %s | cut -f1 | %s query -i %s | sort | uniq -c > %s" % (kmer_file, settings["jf_path"], jf_file, freq_file)
    runner.run(command, verbose=False)
    with open(freq_file) as fh:
        data = fh.read()
        if "Failed to parse header of file" in data:
            print "Error in file %s jf_file"
            if unlink:
                os.unlink(jf_file)
        else:
            if "2926 0" in data:
                pass
            else:
                print data
                raw_input("Get something...")


def check_genome_eu(settings, kmer_file):
    """
    """
    tasks = get_genome_eu_files(settings)
    for jf_file in tasks:
      if not os.path.isfile(jf_file):
          continue
      print jf_file
      _checker(jf_file, settings, kmer_file)


def check_genome_pro(settings, kmer_file):
    """
    """    
    folder = settings["folder_genomes_pro"]
    print folder
    for file_name in sc_iter_filepath_folder(folder):
        if not file_name.endswith(".fna"):
            continue
        jf_file = file_name + ".23.jf"
        if not os.path.isfile(jf_file):
            continue
        print jf_file
        _checker(jf_file, settings, kmer_file)


def check_genome_wgs(settings, kmer_file):
    """
    """    
    folder = settings["folder_wgs"]
    print folder
    for file_name in sc_iter_filepath_folder(folder):
        if not "fsa_nt" in file_name:
            continue
        items = file_name.split("/")[-1].split(".")
        jf_file = os.path.join(folder, "wgs.%s.fsa_nt.23.jf" % items[1])
        if not os.path.isfile(jf_file):
            continue
        print jf_file
        _checker(jf_file, settings, unlink=False)


def check_illumina(settings):

    kmer_file = settings["kmers_illumina"]

    check_genome_eu(settings, kmer_file)
    check_genome_pro(settings, kmer_file)
    check_genome_wgs(settings, kmer_file)



if __name__ == '__main__':
    
    check_illumina(settings)



