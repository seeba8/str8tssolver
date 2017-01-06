import argparse
from field import Field

def ValuesString(v):
	import re  # Unless you've already imported re previously
	try:
		return re.match("^\d{81}$", v).group(0)
	except:
		raise argparse.ArgumentTypeError("String '%s' does not match required format"%(v,))
	else:
		return v
	
def main():
	parser = argparse.ArgumentParser(description="Solves some str8ts.")
	parser.add_argument("-v", "--values", nargs=2,type=ValuesString, metavar=("values", "blacks"), help="Two 81-char strings with pre-set values.\n"+
						"The first contains the pre-set values, 0 for an empty square.\n" + 
						"The second contains the black squares, 1 for black, 0 for empty.")
	parser.add_argument("--preset", choices=[1,2,3], type=int, help="A pre-defined str8t to test")
	args = parser.parse_args()
	
	if args.preset == 1:
		# The Daily Str8ts, #2971, by Andrew Stuart (http://www.str8ts.com)
		blacks = "100110001000100000001001100100010000100000001000010001001100100000001000100011001"
		values = "600070010007000003780000100000000021000090000100480500009000006000040000000000005"
		f = Field({"blacks":blacks, "values":values})
	elif args.preset == 2:
		# The Daily Str8ts, #2972, by Andrew Stuart (http://www.str8ts.com)
		blacks = "110000100000000000001001000000100100110000011001001000000100100000000000001000011"
		values = "000000090000002600000409000500000000000000002000000000078000104000000000005000000"
		f = Field({"blacks":blacks, "values":values})
	elif args.preset == 3:
		# The Weekly Extreme Str8ts Puzzle, #341, by Andrew Stuart (http://www.str8ts.com)
		blacks = "001001001000000000000000100000011001000000100001100001000100000000000000000010000"
		values = "000000003000302000000000708000008000004000000309000000090100500000000000000000000"
		f = Field({"blacks":blacks, "values":values})
	elif args.values != None:
		f = Field({"blacks":args.values[1], "values":args.values[0]})
	else:
		f = Field()
	f.collect_streets()
	f.show()
	last_perf = 0
	current_perf = 1
	while(last_perf != current_perf):
		last_perf = f.get_total_length()
		f.eliminate_possibilities()
		current_perf = f.get_total_length()
	f.show_hints()


if __name__ == "__main__":
	main()