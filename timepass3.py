import re
from datetime import date, datetime
finalText="Reliance Drugs\n KALPETTA\n Stock & Sales Statement for the month of 01-01-20 date: 02-02-21 03-03-26"
stripped = finalText.split("Report Updated Till", 1)[0]
print(stripped)