from sys import argv, exit

from app.utils import upload_csv

if __name__ == '__main__':

    original_file = None
    try:
        original_file = argv[1]
    except IndexError:
        print("Please, provide correct CSV file!")
        print("Example: 'python converter.py /path/to/file.csv'")
        exit(-1)

    upload_csv(original_file)
