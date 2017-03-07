import os, csv, hashlib
from os import path
from functools import partial

# utils

def _mkpath(*paths):
	dirs = ''
	for p in paths:
		dirs = path.join(dirs, p)
		if not path.exists(dirs):
			os.makedirs(dirs)
	return dirs

'''
	Calculate file name by data.
		@param {dictionary} data - data for hashing file name
		@returns {string} file   - md5 file name
'''
def _csvFilename(data):
	# md5
	m = hashlib.md5()
	m.update( repr(data).encode() )
	# make file name
	file = '%s.csv' % m.hexdigest()
	return file

'''
	Write Csv file.
		@param {dictionary} data
		@param {list of string} paths - list of directory
		@param {string} filename      - if filename is not specified, it will hash a filename by _csvFilename().
		@param {boolean} dictOpt      - dictionary or list
		@returns {string} file        - file name
'''
def _writeCsvInterface(data, paths = ['.'], filename = None, dictOpt = False):
	dirs = _mkpath(*paths)
	# generate a hash filename when it is not specified
	file = _csvFilename(data) if filename is None else filename
	# write csv
	csvfile = open(path.join(dirs, file), 'w', encoding = 'utf-8')
	# write data into csv
	if len(data) > 0:
		# select DictWriter or writer
		if dictOpt:
			writer = csv.DictWriter( csvfile, sorted(data[0].keys()) )
			writer.writeheader()
		else:
			writer = csv.writer(csvfile, quoting = csv.QUOTE_NONNUMERIC)
		# write data
		for row in data:
			writer.writerow(row)
	# close csv
	csvfile.close()
	# return filename
	return file

# exports

mkpath       = _mkpath
writeCsv     = partial(_writeCsvInterface, dictOpt = False)
writeCsvDict = partial(_writeCsvInterface, dictOpt = True)