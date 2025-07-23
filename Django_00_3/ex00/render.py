import re
import settings
import sys

#Error for number of arguments
if len(sys.argv) < 2:
    print("Usage: python3 render.py <template_file>")
    sys.exit(1)

#file
template_file = sys.argv[1]

#Check if extension file is .template
if not template_file.endswith('.template'):
    print("Error: File must have .template extension")
    sys.exit(1)

#Try read file, and error if not exist or if read file is not possible
try:
    with open(template_file, 'r') as f:
        template = f.read()
except Exception as e:
    print(f"Error: Cannot open file '{template_file}': {e}")
    sys.exit(1)

#open and read template file
with open(template_file, 'r') as f:
    template = f.read()

#function for search and replace variable in value
def replace_var(match):
    var_name = match.group(1)
    value = getattr(settings, var_name, '')
    return str(value)

#Store result replace all variables in template
result = re.sub(r'\{(\w+)\}', replace_var, template)

#Add html structure
html_result = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>My amazing CV</title>
</head>
<body>
{result}
</body>
</html>
"""

#Read file.html with result
try:
    with open('file.html', 'w') as f:
        # écriture dans le fichier
        f.write(html_result)
except PermissionError:
    print("Error: Permission denied to write to 'file.html'")