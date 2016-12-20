import datetime
import argparse

parser = argparse.ArgumentParser()                                              
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

from datetime import datetime

try:
	o = open('output.qif','w')

	#The list of word to look for in the downloaded transaction description and replace with short N quicken description
	long_word_list = 'sainsburys oyster fantastic tfl sitters deliveroocouk co-op tailscom'
	long_word_set = set(long_word_list.split())

	with open(args.file) as f:
		for line in f:

			#Check if line and the word set intersect, if so, it'll return which word is the intersection
			contained_string= set(line.lower().split()) & long_word_set

			#print("the line has D?" + str(line[0:1] == 'D'))
			#For the date, flip d/m to work for my quicken setting
			if line[0:1] == "D":
  				#D16/12/2016
  				date = line[1:].rstrip()
				newdate = datetime.strptime(date, '%d/%m/%Y').strftime('%m/%d/%Y')
  				#print("D" + newdate)
				o.write("D" + newdate + "\n")
			#Change any descriptions that match my list
			elif len(contained_string) > 0:
				text = next(iter(contained_string))
				if text == 'tfl': text = 'Oyster'
				o.write("P" + text.title() + "\n")

				#Add category for the known text
				if text == 'sainsburys': o.write("LGroceries\n") 
				if text == 'oyster' or text == 'tfl': o.write("LTransportation\n") 
				if text == 'deliveroo': o.write("LFood out\n") 
				if text == 'co-op': o.write("LGroceries\n") 
				if text == 'tails': o.write("LDog:Food\n") 
				if text == 'sitters': o.write("LKids:Babysitting\n") 
				if text == 'fantastic': o.write("LMisc\n") 
			#Everything else, output as is
			else:
  				#print(line.rstrip())
				#o.write(line.rstrip())
				o.write(line)

except IOError:
	print("can't open output file")

finally:
	o.close()
