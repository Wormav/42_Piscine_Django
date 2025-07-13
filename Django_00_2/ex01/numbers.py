def read_and_diplay_number():
	try:
		with open('numbers.txt', 'r') as file:
			content = file.read()
			numbers = content.split(',')
			for number in numbers:
				print(number.strip())
	except FileNotFoundError:
		print("Error: number.txt not found!")
	except IOError:
		print("Error: read number.txt is not possible!")

if __name__ == "__main__":
	read_and_diplay_number()
