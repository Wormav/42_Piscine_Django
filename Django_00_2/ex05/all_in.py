import sys

def all_in():
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

	input_string = sys.argv[1]

	if ",," in input_string:
		return

	expressions = input_string.split(",")

	for expression in expressions:
		clean_expr = expression.strip()

		if not clean_expr:
			continue

		state_found = None
		for state_name, state_code in states.items():
			if state_name.lower() == clean_expr.lower():
				state_found = state_name
				capital = capital_cities[state_code]
				print(f"{capital} is the capital of {state_found}")
				break

		if not state_found:
			capital_found = None
			state_code_found = None
			for state_code, capital_name in capital_cities.items():
				if capital_name.lower() == clean_expr.lower():
					capital_found = capital_name
					state_code_found = state_code
					break

			if capital_found:
				for state_name, code in states.items():
					if code == state_code_found:
						print(f"{capital_found} is the capital of {state_name}")
						break
			else:
				print(f"{clean_expr} is neither a capital city nor a state")

if __name__ == "__main__":
    all_in()
