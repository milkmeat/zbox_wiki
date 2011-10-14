"""
Implement Markdown Extension

this script supports
- simple table

Simple table syntax:

    || name || desc ||
    | lee | author |

will be:

    <table>
    <tr>
        <th> name </th><th> desc </th>
    </tr>
    <tr>
        <td> lee </td><td> author </td>
    </tr>
    </table>

"""

import re


def escape_table_special_chars(text):
    escape_p = "!\|"
    p_obj = re.compile(escape_p, re.UNICODE)
    return p_obj.sub('\v', text)

def unescape_table_special_chars(text):
    return text.replace("\v", "|")


def match_table(line):
    t_p = "^\|{1,2} (.+?) \|{1,2}$"
    if re.match(t_p, line) and line.count('|') >= 2:
        return True
    else:
        return False

def parse_cells(line):
    cells_p = "^(?P<splitter>\|){1,2} (?P<cells>.+?) \|{1,2}$"
    p_obj = re.compile(cells_p, re.UNICODE)
    m_obj = p_obj.match(line)

    if m_obj:
        cells = m_obj.group('cells')
        splitter = m_obj.group('splitter')
        cells = [cell.strip()
                for cell in cells.split(splitter)
                if cell.strip()]

        is_table_header = line.startswith("||")
        if not is_table_header:
            buf = " </td> <td> ".join(cells)
            buf = "    <td> %s </td>" % buf
        else:
            buf = " </th> <th> ".join(cells)
            buf = "    <th> %s </th>" % buf

        return buf

    return line

def parse_table(text):
    text = escape_table_special_chars(text)
    resp = []

    lines = text.split("\n")
    total_lines = len(lines)

    for i in xrange(total_lines):
        last_line = None
        curr_line = lines[i]
        next_line = None

        is_first_line = i == 0
        if not is_first_line:
            last_line = lines[i - 1]

        is_latest_line = (i + 1) == total_lines
        if not is_latest_line:
            next_line = lines[i + 1]


        last_line_of_table_beginning = (not match_table(curr_line)) and next_line and match_table(next_line)
        next_line_of_table_ending = match_table(curr_line) and next_line and (not match_table(next_line))
        is_table_beginning = last_line is '' and match_table(curr_line) and (curr_line.count('||') >= 2)

        if last_line_of_table_beginning:
            resp.append("")
            resp.append("<table>")

        elif next_line_of_table_ending:
            resp.append("")
            resp.append("</table>")

        elif is_table_beginning:
            resp.append("<tr>")
            resp.append(parse_cells(curr_line))
            resp.append("</tr>")

        elif match_table(curr_line):
            resp.append("<tr>")
            resp.append(parse_cells(curr_line))
            resp.append("</tr>")

        else:
            resp.append(curr_line)

    buf = "\n".join(resp)
    buf = unescape_table_special_chars(buf)
    
    return buf

