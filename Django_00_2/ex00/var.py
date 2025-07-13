def my_var():
	int_var = 42
	string_var = "42"
	string_var_letter = "quarante-deux"
	float_var = 42.0
	true_var = True
	list_var = [42]
	dict_var = {42: 42}
	tuple_var = (42,)
	set_var = set()

	print(f"{int_var} has a type {type(int_var)}")
	print(f"{string_var} has a type {type(string_var)}")
	print(f"{string_var_letter} has a type {type(string_var_letter)}")
	print(f"{float_var} has a type {type(float_var)}")
	print(f"{true_var} has a type {type(true_var)}")
	print(f"{list_var} has a type {type(list_var)}")
	print(f"{dict_var} has a type {type(dict_var)}")
	print(f"{tuple_var} has a type {type(tuple_var)}")
	print(f"{set_var} has a type {type(set_var)}")



if __name__ == "__main__":
	my_var()
