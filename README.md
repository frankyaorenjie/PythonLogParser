PythonLogParser
===============

This is a general method to parse log file. A workround to be 'general', easy-for-use is of less consideration.

Whole 'project' (quote because it is really tiny) consists of two parts.

1. parslog. It is core in this project.
2. BackwardsReaderIter. It's another project on Github and it isn't included here. You can get this [here](https://github.com/baniuyao/BackwardsReaderIter). It makes you can read a file backwards line by line. 

*ATTENTION*:
BackwardsReaderIter is also maintained by me and I chose to manage it on Github as well. For version control, *THIS IS NOT INCLUDED IN THIS PROJECT*.

Piece of example:

	from BackwardsReaderIter import BackwardsReaderIter
	from parselog import LogParser
	import time, re, sys
	
	if __name__ == '__main__':
		#file_name = sys.argv[1]
		file_name = 'example_access.log'
		current_time = time.time()
		key = (
			('" (2[\d]{2}) ', '2XX', 'count'),
			('" (4[\d]{2}) ', '4XX', 'count'),
			('" (5[\d]{2}) ', '5XX', 'count'),
			(' (\d*)( [^ ]*){2}$','traffic','sum'), #traffic
		)
		lp = LogParser(keyword_list=key,re_time='\d{2}\/\w{3}\/\d{4}:\d{2}:\d{2}:\d{2}', str_time='%d/%b/%Y:%H:%M:%S', period=(0,time.time()))
		bri = BackwardsReaderIter(file_name)
		for line in bri.backread():
			if lp.inPeriod(line):
				lp.parseLine(line)
				# test re is okay or not
				lp.test(line)
			else:
				break
		print lp.getResult()
