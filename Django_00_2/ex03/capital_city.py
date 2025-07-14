import sys

def search_capital():
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

	state_name = sys.argv[1]

	if state_name in states:
		state_code = states[state_name]
		capital = capital_cities[state_code]
		print(capital)
	else:
		print("Unknown state")


if __name__ == "__main__":
    search_capital()
