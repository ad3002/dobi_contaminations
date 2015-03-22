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

    
