import os
import shutil
import sys

target_format = 'PNG'

if len(sys.argv) > 1:
	vignettes_dir = sys.argv[1].rstrip('/')

	if len(sys.argv) > 2:
		new_dir = sys.argv[2].rstrip('/')
	else:
		new_dir = sys.argv[1].rstrip('/')+'_sorted'

	try:
		os.mkdir(new_dir)
	except:
		print('Error dir')

	# Create a directory for each class
	for k in range(0, 10):
		try:
			os.mkdir(new_dir+'/'+str(k))
		except FileExistsError:
			print('Directory already created.')

	i = 0
	for element in os.listdir(vignettes_dir):
		try:
			# k : PR annotation (usually 1 to 6)
			k = element.split('_')[1].split('.')[0]
			vfull = vignettes_dir+'/'+element
			dest = new_dir+'/'+str(k)+'/'+str(i)+'.'+target_format
			print('Created' , dest)
			shutil.copyfile(vfull, dest)
			i += 1
		except:
			print(element, 'is not a file')
else:
	print('Please specify a directory')
