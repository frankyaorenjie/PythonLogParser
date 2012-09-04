#!/usr/bin/env python

from backReader import BackwardsReader as BackReader
import time, re

class TimeParser(object):

	def __init__(self, re_time, str_time, period):
		self.__re_time = re.compile(re_time)
		self.__str_time = str_time
		self.__period = period

	def __get(self, line):
		t= re.search(self.__re_time, line).group(0)
		return time.mktime(time.strptime(t, self.__str_time))

	def inPeriod(self, line):
		t = self.__get(line)
		return (t > self.__period[0] and t < self.__period[1])

class LogParser(object):
	'''
	__keyword_result
	{' (\\d*)( [^ ]*){2}$': {'re_pattern': <_sre.SRE_Pattern object at 0x2b4676c90b30>, 'handle': 'sum', 'name': 'traffic', 'result': 0}
	'''

	def __init__(self, keyword_list={}, re_time='', str_time='', period=(time.time()-300,time.time())):
		self.__count = 0
		self.__method = {'count' : self.count, 'sum' : self.sum}
		self.__keyword_result = {}
		for keyword in keyword_list:
			re_keyword,name,method = keyword
			keyword_compiled_tmp = re.compile(re_keyword)
			self.__keyword_result[re_keyword] = {'re_pattern':keyword_compiled_tmp, 'name':name, 'handle':method, 'result':0}
		if re_time != '':
			self.__check_time = True
		else:
			False
		if self.__check_time:
			self.__TimeParser = TimeParser(re_time, str_time, period)

	def count(self, keyword, *args):
		self.__keyword_result[keyword]['result'] += 1

	def sum(self, keyword, *args):
		self.__keyword_result[keyword]['result'] += args[0]

	def test(self, line):
		for keyword in self.__keyword_result:
			result = self.__keyword_result[keyword]['re_pattern'].search(line)
			if result:
				print "%s\nre: '%s' --> FOUND: '%s'" % (line, keyword, result.group(1))

	def inPeriod(self, line):
		return (not self.__check_time or self.__TimeParser.inPeriod(line))

	def parseLine(self,line):
		self.__count += 1
		for keyword in self.__keyword_result:
			result = self.__keyword_result[keyword]['re_pattern'].search(line)
			if result:
				value = float(result.group(1))
				handle = self.__method[self.__keyword_result[keyword]['handle']]
				handle(keyword, value)

	def getResult(self):
		tmp_dict = {}
		for keyword in self.__keyword_result:
			name = self.__keyword_result[keyword]['name']
			tmp_dict[name] = self.__keyword_result[keyword]['result']
		return tmp_dict

	def getCount(self):
		return self.__count
