import re
from datetime import date, datetime
import sys

text=str(sys.argv[1]).replace("\\n", "\n")
text2="inside \n script"
print("argument:", text)
print("inside:",text2)
