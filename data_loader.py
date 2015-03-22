#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 16.03.2015
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import os
from settings import settings
from PyExp import runner
from PyExp import sc_iter_filepath_folder
import tempfile
from collections import defaultdict

def load_wgs(): 
    command = "~/.aspera/connect/bin/ascp -i ~/.aspera/connect/etc/asperaweb_id_dsa.putty -k3 -Q -T -l100m anonftp@ftp.ncbi.nlm.nih.gov:/genbank/wgs ."
    runner.run(command)

def load_tsa():
    command = "~/.aspera/connect/bin/ascp -i ~/.aspera/connect/etc/asperaweb_id_dsa.putty -k3 -Q -T -l100m anonftp@ftp.ncbi.nlm.nih.gov:/genbank/tsa ."
    runner.run(command)

def load_genomes():
    command = "~/.aspera/connect/bin/ascp -i ~/.aspera/connect/etc/asperaweb_id_dsa.putty -k3 -Q -T -l100m anonftp@ftp.ncbi.nlm.nih.gov:/genbank/genomes ."
    runner.run(command)

def compute_jf_for_tsa(settings):
    """ Compute jf files for tsa datasets.
    """
    folder_tsa = settings["folder_tsa"]
    print folder_tsa
    for file_name in sc_iter_filepath_folder(folder_tsa):
        print file_name
        if not "fsa_nt" in file_name:
            continue
        output_file = file_name + ".23.jf"
        if os.path.isfile(output_file):
            print "File exists", output_file
            continue
        command = "/home/akomissarov/libs/jellyfish-2.2.0/bin/jellyfish count -m 23 -t 20 -s 5G -C -o %s %s" % (output_file, file_name)
        runner.run(command)

def compute_jf_for_wgs(settings):
    """ Compute jf files for wgs datasets.
    """
    folder = settings["folder_wgs"]
    print folder
    tasks = defaultdict(list)
    for file_name in sc_iter_filepath_folder(folder):
        print file_name
        if not "fsa_nt" in file_name:
            continue
        items = file_name.split(".")
        output_file = "wgs.%s.fsa_nt.23.jf" % items[1]
        tasks[output_file].append(file_name)

    for output_file, files in tasks.items():
        if os.path.isfile(output_file):
            print "File exists", output_file
            continue
        file_name = " ".join(files)
        command = "/home/akomissarov/libs/jellyfish-2.2.0/bin/jellyfish count -m 23 -t 20 -s 10G -C -o %s %s" % (output_file, file_name)
        runner.run(command)

def compute_jf_for_genomes_pro(settings):
    """ Compute jf files for prokaryotics genomes.
    """
    folder = settings["folder_genomes_pro"]
    print folder
    for file_name in sc_iter_filepath_folder(folder):
        if not file_name.endswith(".fna"):
            continue
        print file_name
        output_file = file_name + ".23.jf"
        if os.path.isfile(output_file):
            print "File exists", output_file
            continue
        command = "/home/akomissarov/libs/jellyfish-2.2.0/bin/jellyfish count -m 23 -t 20 -s 10G -C -o %s %s" % (output_file, file_name)
        runner.run(command)


def compute_jf_for_genome_eu(settings):
    """ Compute jf files for eukaryotics genomes.
    
    Information from NCBI README:

    vertebrates_mammals/Homo_sapiens/HuRef

    Each assembly-unit directory will also contain one or more of the 
    following directories (depending on the particular assembly):
         assembled_chromosomes/
         placed_scaffolds/
         unlocalized_scaffolds/
         unplaced_scaffolds/
         alt_scaffolds/ (only in alternate loci and patch assembly-units)
         pseudoautosomal_region/ (only for mammmals)

        ----------------------------------
    Files containing genomic sequences
    ----------------------------------
    FILENAME                         CONTENT
    chr?.fa.gz                       chromosome sequence
    chr?.placed.scaf.fa.gz           placed scaffold sequences
    chr?.unlocalized.scaf.fa.gz      unlocalized scaffold sequences
    unplaced.scaf.fa.gz              unplaced scaffold sequences
    alt.scaf.fa.gz                   alternate loci or patch scaffold 
                                     sequences
    """

    folder = settings["folder_genomes_eu"]
    print folder
    tasks = defaultdict(list)
    for file_name in sc_iter_filepath_folder(folder):
        if not ".fa." in file_name:
            continue
        if not "Primary" in file_name:
            continue
        genome_path = file_name.split(folder)[-1][1:]
        section, taxon, assembly = genome_path.split("/")[:3]
        # print section, taxon, assembly, file_name
        output_file = os.path.join(folder, section, taxon, assembly, "primary_assembly.23.jf")
        tasks[output_file].append(file_name)

    for output_file, files in tasks.items():
        if os.path.isfile(output_file):
            print "File exists", output_file
            continue
        # check duplication betweeb placed and assembled
        has_primary = False
        for file_name in files:
            if "placed_scaffolds" in file_name:
                has_primary = True
                break
        if has_primary:
            files = [x for x in files if not "assembled_chromosomes" in x]

        with open(output_file, "w") as fh:
            for i, file_name in enumerate(files):
                if file_name.endswith(".gz"):
                    fh.write("%s\n" % file_name)
                    files[i] = file_name[:-3]
        command = "cat %s | xargs -n 1 -P %s gzip -d" % (output_file, len(files))
        runner.run(command)
        os.unlink(output_file)

        file_name = " ".join(files)
        print output_file
        print file_name
        command = "/home/akomissarov/libs/jellyfish-2.2.0/bin/jellyfish count -m 23 -t 40 -s 15G -C -o %s %s" % (output_file, file_name)
        runner.run(command)
        

if __name__ == '__main__':
    pass

