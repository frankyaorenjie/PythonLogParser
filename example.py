#!/usr/bin/env python

from backReader import BackwardsReader as BackReader
from parselog import LogParser
import time, re, sys

if __name__ == '__main__':
	file_name = sys.argv[1]
	current_time = time.time()
	key = (
		('[ ,](20[06])[^\d]','2XX','count'), #2XX
		('[ ,](4[90][349])[^\d]','4XX','count'), #4XX
		('[ ,](50[023])[^\d]','5XX','count'), #5XX
		(' (\d*)( [^ ]*){3}$','resp','sum'), #resp
		(' (\d*)( [^ ]*){2}$','traffic','sum'), #traffic
	)
	lp = LogParser(keyword_list=key,re_time='\d{2}\/\w{3}\/\d{4}:\d{2}:\d{2}:\d{2}', str_time='%d/%b/%Y:%H:%M:%S')
	o = open(file_name)
	br = BackReader(o)
	ip_set = set()
	while True:
		line = br.readline().strip()
		if lp.inPeriod(line):
			lp.parseLine(line)
		else:
			break
	o.close()
