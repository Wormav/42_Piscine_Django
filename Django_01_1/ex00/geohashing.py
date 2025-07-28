import sys
import antigravity

def is_valid_date_format(date: str)->bool:
    if len(data) != 10:
        return FALSE
    if date[4] != '-' or date[7] != '-':
        return False
    y, m, d = date_str[:4], date_str[5:7], date_str[8:]
    if not (y.isdigit() and m.isdigit() and d.isdigit()):
        return False
    return True

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 geohashing.py latitude longitude YYYY-MM-DD")
        return
    try:
        lat = float(sys.argv[1])
        long = float(sys.argv[2])
        date = sys.argv[3]
        if not is_valid_date_format(date):
            print("Error: format date YYYY-MM-DD.")
            return

        antigravity.geohash(lat, long, date.encode())
    except ValueError:
        print("Error: latitude and longitude must be numbers.")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()