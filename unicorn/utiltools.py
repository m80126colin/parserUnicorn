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

def _csvFilename(paths, data):
	# md5
	m = hashlib.md5()
	m.update( repr(data).encode() )
	# make file name
	file = '%s.csv' % m.hexdigest()
	return file

# write a csv file with md5 filename

def _writeCsvInterface(data, paths = ['.'], filename = None, dictOpt = False):
	dirs = _mkpath(*paths)
	if filename is None:
		file = _csvFilename(paths, data)
	else:
		file = filename
	# write csv
	csvfile = open(path.join(dirs, file), 'w', encoding = 'utf-8')
	# write data into csv
	if len(data) > 0:
		# select DictWriter or writer
		if dictOpt:
			writer = csv.DictWriter( csvfile, sorted(data[0].keys()) )
			writer.writeheader()
		else:
			writer = csv.writer(csvfile)
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