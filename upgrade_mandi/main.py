import time
from os.path import join
from pathlib import Path

from utils.read import readExcel

path = join(Path(__file__).parent, "utils", "heavy.xlsx")

start = time.time()
df = readExcel(file=path, sheetName="Sheet1")
end = time.time()


print(df)
print()
print()

print(end - start)
