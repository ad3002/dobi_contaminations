#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 16.03.2015
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from data_loader import *
from settings import settings

if __name__ == '__main__':

	# 1. Get data
	load_wgs()
	load_tsa()
	load_genomes()
	# 2. Compute kmers
	compute_jf_for_tsa(settings)
	compute_jf_for_wgs(settings)
	compute_jf_for_genomes_pro(settings)
	compute_jf_for_genome_eu(settings)
	

