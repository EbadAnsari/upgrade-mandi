from os.path import abspath

from reader import reader

df = reader.read_excel("./heavy.xlsx", "Sheet1")

print(df)
