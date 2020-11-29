import csv
import glob
import re

page_types = {}
page_types['Tim Hooven'] = 0
page_types['Sarie Toste and David R. Couch'] = 1
page_types['Tom Chapman'] = 2
page_types['Dan Hauser'] = 3
page_types['John Ash'] = 4
page_types['Gaye Gerdts'] = 5
page_types['Erin Maureen Taylor'] = 6
page_types['Sarie Toste (right)'] = 7
page_types['Sarie Toste and Dan Hauser'] = 8
page_types['Emil Feierabend and Jerry Hansen'] = 9
page_types['Sarie Toste (left)'] = 10
page_types['Kerry Gail Watty'] = 11
page_types['Sherry Dalziel'] = 12
page_types['Sarie Toste Zachary B. Thoma and Dan Hauser'] = 13
page_types['Natalie Zall'] = 14
page_types['Michael Caldwell'] = 15
page_types['Nicole Chase'] = 16
page_types['Kathleen A. Fairchild'] = 17
page_types['David R. Couch'] = 18
page_types['Zachary B. Thoma and Dan Hauser'] = 19


reader = csv.reader(open('pages.csv', 'r'))

ballots = []

files = glob.glob("bubbles_final/*")

# maps jpg_number to page_type
for row in reader:
	k, v = row
	ballot_string = k.zfill(6)
	r = re.compile("bubbles_final\/{}_*".format(ballot_string))
	if v in page_types and len(list(filter(r.match, files))) == 0:
		print(k)
		ballots.append(k)

with open('unparsed_ballots.txt', 'w') as f:
    for item in ballots:
        f.write("%s\n" % item)



# mylist = ["dog", "cat", "wildcat", "thundercat", "cow", "hooo"]
# r = re.compile(".*cat")
# newlist = list(filter(r.match, mylist)) # Read Note
# print(newlist)

# ['cat', 'wildcat', 'thundercat']

