import datetime
from dateutil import relativedelta
from lxml import etree

# TODO: update this to your real birthday (year, month, day) to get an accurate Uptime counter
BIRTHDAY = datetime.datetime(2008, 1, 1)


def daily_readme(birthday):
    """
    Returns the length of time since the given birthday,
    e.g. 'XX years, XX months, XX days'
    """
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + plural(diff.years),
        diff.months, 'month' + plural(diff.months),
        diff.days, 'day' + plural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else '')


def plural(unit):
    return 's' if unit != 1 else ''


def svg_overwrite(filename, age_data):
    """
    Parse SVG and update the Uptime field with a new age string.
    """
    tree = etree.parse(filename)
    root = tree.getroot()
    justify_format(root, 'age_data', age_data, 28)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def justify_format(root, element_id, new_text, length=0):
    """
    Update text and pad the leading dots so the value stays right-justified.
    """
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    just_len = max(0, length - len(new_text))
    if just_len <= 2:
        dot_string = {0: '', 1: ' ', 2: '. '}[just_len]
    else:
        dot_string = ' ' + ('.' * just_len) + ' '
    find_and_replace(root, f"{element_id}_dots", dot_string)


def find_and_replace(root, element_id, new_text):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text


if __name__ == '__main__':
    age_data = daily_readme(BIRTHDAY)
    svg_overwrite('light_mode.svg', age_data)
    svg_overwrite('dark_mode.svg', age_data)
    print(f'Updated Uptime to: {age_data}')
