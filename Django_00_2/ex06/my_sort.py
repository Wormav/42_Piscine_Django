def	sort_dict():
	d = {
		('Hendrix', '1942'),
        ('Allman', '1946'),
        ('King', '1925'),
        ('Clapton', '1945'),
        ('Johnson', '1911'),
        ('Berry', '1926'),
        ('Vaughan', '1954'),
        ('Cooder', '1947'),
        ('Page', '1944'),
        ('Richards', '1943'),
        ('Hammett', '1962'),
        ('Cobain', '1967'),
        ('Garcia', '1942'),
        ('Beck', '1944'),
        ('Santana', '1947'),
        ('Ramone', '1948'),
        ('White', '1975'),
        ('Frusciante', '1970'),
        ('Thompson', '1949'),
        ('Burton', '1939'),
	}

	my_dict_by_year = {}
	for name, year in d:
		if year in my_dict_by_year:
			my_dict_by_year[year] += f" {name}"
		else:
			my_dict_by_year[year] = name
	print("By years:\n")

	for year in sorted(my_dict_by_year.keys()):
		print(f"{year} : {my_dict_by_year[year]}")

	my_dict_by_name = {}
	for name, year in d:
		my_dict_by_name[name] = year

	print("\nBy alphabetical order:\n")
	for name in sorted(my_dict_by_name.keys()):
		print(f"{name} : {my_dict_by_name[name]}")

if __name__ == "__main__":
	sort_dict()
