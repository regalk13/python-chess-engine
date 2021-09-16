import re


mention = input()

m = re.search("<@!?(\d{18})>", mention)

print(m.group(0))
