import re

# ab = '检具号：P201-107'
# ab = '检具号：P201-107-52'
# ab = '检具号：1P201-10eqwe7-qeqweq12-qwe5q4'
# ab = 'GL-312检具号：'
# ab = 'GL-312'
# ab = '|GL-312'
# ab = '检具号'
ab = 'GL9123'

p1 = r'[a-zA-Z]+.*-.*\d+'
p2 = r'[a-zA-Z]+.*-.+-.*\d+'
p3 = r'[a-zA-Z]+.*-.+-.+-.*\d+'
result = re.compile(pattern=p3).search(ab)
if result is not None:
    result = result.group()
else:
    result = re.compile(pattern=p2).search(ab)
    if result is not None:
        result = result.group()
    else:
        result = re.compile(pattern=p1).search(ab)
        if result is not None:
            result = result.group()
        else:
            result = 'None'

print(result)

