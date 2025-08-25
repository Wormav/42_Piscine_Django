TXT_FILE = "periodic_table.txt"
HTML_FILE = "periodic_table.html"
CSS_FILE = "periodic_table.css"


def parse_elements(filename):
    elements = []
    with open(filename, "r") as f:
        for line in f:
            if "=" not in line:
                continue
            name, attrs = line.strip().split("=", 1)
            name = name.strip()
            attr_dict = {}
            for attr in attrs.split(","):
                key, value = attr.strip().split(":", 1)
                attr_dict[key.strip()] = value.strip()
            attr_dict["name"] = name
            elements.append(attr_dict)
    return elements


def build_table(elements):
    max_row = 7
    max_col = 18
    table = [[] for _ in range(max_row)]
    elements = sorted(elements, key=lambda e: int(e["number"]))
    row = 0
    col_tracker = [0] * max_row
    for e in elements:
        pos = int(e["position"])
        if row == 0 and pos == 0 and col_tracker[row] != 0:
            row += 1
        while row < max_row and col_tracker[row] > pos:
            row += 1
        if row >= max_row:
            row = max_row - 1
        while len(table[row]) < pos:
            table[row].append(None)
        table[row].append(e)
        col_tracker[row] = len(table[row])
        if len(table[row]) == max_col:
            row += 1
    for r in range(max_row):
        while len(table[r]) < max_col:
            table[r].append(None)
    return table


def html_element_cell(e):
    if not e:
        return "<td></td>"
    return f"""<td class="element">
    <h4>{e["name"]}</h4>
    <ul>
      <li>No {e["number"]}</li>
      <li>{e["small"]}</li>
      <li>{e["molar"]}</li>
      <li>{e["electron"]} electron</li>
    </ul>
  </td>"""


def generate_html(table):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>periodic_table</title>
  <link rel="stylesheet" href="periodic_table.css">
</head>
<body>
  <table>
"""
    for row in table:
        html += "    <tr>\n"
        for cell in row:
            html += "      " + html_element_cell(cell) + "\n"
        html += "    </tr>\n"
    html += """  </table>
</body>
</html>
"""
    return html


def generate_css():
    return """
table {
  border-collapse: collapse;
}
td.element {
  border: 1px solid black;
  padding: 10px;
  vertical-align: top;
  min-width: 100px;
  min-height: 80px;
}
h4 {
  text-align: center;
  margin: 0 0 5px 0;
}
ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}
"""


def main():
    elements = parse_elements(TXT_FILE)
    table = build_table(elements)
    html = generate_html(table)
    css = generate_css()
    with open(HTML_FILE, "w") as f:
        f.write(html)
    with open(CSS_FILE, "w") as f:
        f.write(css)
    print(f"Files génered : {HTML_FILE}, {CSS_FILE}")


if __name__ == "__main__":
    main()
