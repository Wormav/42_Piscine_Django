#!/usr/bin/python3

from elem import Elem, Text
from elements import *


class Page:
    def __init__(self, elem):
        if not isinstance(elem, Elem):
            raise TypeError("L'élément doit être une instance d'Elem ou de ses classes dérivées")
        self.elem = elem

    def __str__(self):
        result = ""
        if isinstance(self.elem, Html):
            result += "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result

    def write_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(str(self))
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier : {e}")

    def is_valid(self):
        return self._validate_element(self.elem)

    def _validate_element(self, elem):
        allowed_types = [Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                         Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text]

        if not any(isinstance(elem, t) for t in allowed_types):
            return False

        if isinstance(elem, Html):
            if len(elem.content) != 2:
                return False
            if not isinstance(elem.content[0], Head) or not isinstance(elem.content[1], Body):
                return False

        elif isinstance(elem, Head):
            if len(elem.content) != 1 or not isinstance(elem.content[0], Title):
                return False

        elif isinstance(elem, (Body, Div)):
            allowed_in_body_div = [H1, H2, Div, Table, Ul, Ol, P, Span, Text]
            for child in elem.content:
                if not any(isinstance(child, t) for t in allowed_in_body_div):
                    return False

        elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
            if len(elem.content) != 1 or not isinstance(elem.content[0], Text):
                return False

        elif isinstance(elem, P):
            for child in elem.content:
                if not isinstance(child, Text):
                    return False

        elif isinstance(elem, Span):
            for child in elem.content:
                if not isinstance(child, (Text, P)):
                    return False

        elif isinstance(elem, (Ul, Ol)):
            if len(elem.content) == 0:
                return False
            for child in elem.content:
                if not isinstance(child, Li):
                    return False

        elif isinstance(elem, Tr):
            if len(elem.content) == 0:
                return False

            has_th = any(isinstance(child, Th) for child in elem.content)
            has_td = any(isinstance(child, Td) for child in elem.content)

            if has_th and has_td:
                return False

            for child in elem.content:
                if not isinstance(child, (Th, Td)):
                    return False

        elif isinstance(elem, Table):
            for child in elem.content:
                if not isinstance(child, Tr):
                    return False

        if hasattr(elem, 'content'):
            for child in elem.content:
                if isinstance(child, Elem) and not self._validate_element(child):
                    return False

        return True

def test_page():
    print("=== Tests Page class ===\n")

    # Test 1 : Valid HTML page
    print("Test 1 : Valid HTML page")
    valid_page = Page(Html([
        Head(Title(Text("Test Page"))),
        Body([
            H1(Text("Main title")),
            P(Text("A test paragraph."))
        ])
    ]))
    print(f"Is valid: {valid_page.is_valid()}")
    print("Generated HTML:")
    print(valid_page)
    print("\n" + "=" * 50 + "\n")

    # Test 2 : Invalid HTML page (head without title)
    print("Test 2 : Invalid HTML page (head without title)")
    invalid_page = Page(Html([
        Head([]),
        Body([H1(Text("Test"))])
    ]))
    print(f"Is valid: {invalid_page.is_valid()}")
    print("\n" + "=" * 50 + "\n")

    # Test 3 : Write to file
    print("Test 3 : Write to file")
    valid_page.write_to_file("test_output.html")
    print("File 'test_output.html' created")
    print("\n" + "=" * 50 + "\n")

    # Test 4 : Valid table
    print("Test 4 : Valid table")
    table_page = Page(Html([
        Head(Title(Text("Table Test"))),
        Body([
            Table([
                Tr([Th(Text("Header 1")), Th(Text("Header 2"))]),
                Tr([Td(Text("Data 1")), Td(Text("Data 2"))])
            ])
        ])
    ]))
    print(f"Valid table: {table_page.is_valid()}")

    # Test 5 : Invalid table (th and td in same row)
    print("Test 5 : Invalid table (th and td in same row)")
    invalid_table = Page(Html([
        Head(Title(Text("Invalid Table"))),
        Body([
            Table([
                Tr([Th(Text("Header")), Td(Text("Data"))])
            ])
        ])
    ]))
    print(f"Invalid table: {invalid_table.is_valid()}")

if __name__ == '__main__':
    test_page()