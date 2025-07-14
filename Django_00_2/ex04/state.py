import sys

def	search_state():
	states = {
	"Oregon" : "OR",
	"Alabama" : "AL",
	"New Jersey": "NJ",
	"Colorado" : "CO"
	}

	capital_cities = {
	"OR": "Salem",
	"AL": "Montgomery",
	"NJ": "Trenton",
	"CO": "Denver"
	}

	if len(sys.argv) != 2:
		return

	capital_name = sys.argv[1]

	state_code = None
	for code, capital in capital_cities.items():
		if capital == capital_name:
			state_code = code
			break

	if state_code:
		for state_name, code in states.items():
			if code == state_code:
				print(state_name)
				return
	else:
		print("Unknown capital city")

if __name__ == "__main__":
    search_state()
