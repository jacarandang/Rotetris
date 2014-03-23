for i in xrange(1, 13):
	string = ""
	for j in xrange(1, 13):
		if(j!=1): string += " "
		if(i == j): string += "0"
		else: string += str((12+6)*i+6*j)

	print string