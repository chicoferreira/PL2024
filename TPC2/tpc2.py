import fileinput
import re


def apply_title_rules(s):
    regex = r"^\s*(#{1,6})\s+(.*)$"
    m = re.match(regex, s)
    if m:
        header_size = len(m.group(1))
        return f"<h{header_size}>{m.group(2).strip()}</h{header_size}>\n"
    return s


def apply_bold_rules(s):
    regex = r"(\*\*|__)([^\*]*?)\1"
    # [^\*] needed in capture because of order in ***text*** (italic and bold)
    # otherwise it would result in <b>*text<b>* instead of *<b>text<b>*
    return re.sub(regex, r"<b>\2</b>", s)


def apply_italic_rules(s):
    regex = r"(\*|_)(.*?)\1"
    return re.sub(regex, r"<i>\2</i>", s)


def apply_image_rules(s):
    regex = r"\!\[(.*?)\]\((.*?)\)"
    return re.sub(regex, r'<img src="\2" alt="\1"/>', s)


def apply_link_rules(s):
    regex = r"\[(.*?)\]\((.*?)\)"
    return re.sub(regex, r'<a href="\2">\1</a>', s)


def insert_ol_tag(lines: list[str]):
    previous_has_il = False
    for i, line in enumerate(lines):
        is_li = line.startswith("<li>")
        if is_li and not previous_has_il:
            lines.insert(i, "<ol>\n")
        elif not is_li and previous_has_il:
            lines.insert(i, "</ol>\n")
        previous_has_il = is_li

    return lines


def apply_numbered_list_rules(s):
    regex = r"^\s*\d+\.\s+(.*)$"
    m = re.match(regex, s)
    if m:
        return f"<li>{m.group(1).strip()}</li>\n"
    return s


def convert_markdown_to_html(markdown):
    markdown = [apply_title_rules(line) for line in markdown]
    markdown = [apply_bold_rules(line) for line in markdown]
    markdown = [apply_italic_rules(line) for line in markdown]
    markdown = [apply_image_rules(line) for line in markdown]
    markdown = [apply_link_rules(line) for line in markdown]
    markdown = [apply_numbered_list_rules(line) for line in markdown]
    markdown = insert_ol_tag(markdown)
    return markdown


def main():
    print("".join(convert_markdown_to_html(fileinput.input())))


if __name__ == "__main__":
    main()
