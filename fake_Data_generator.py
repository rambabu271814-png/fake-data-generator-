import pandas as pd
import random
import re
import string
from faker import Faker

faker = Faker()

SENSITIVE_COLUMNS = ['email address', 'pancard', 'Phone Number', 'IFSC Code', 'credit-card']

def generate_regex_pattern(value, keep_prefix=2):
    """Return a pattern string where first `keep_prefix` chars are literal and the rest are typed."""
    if pd.isna(value):
        return ""

    value = str(value)
    if len(value) <= keep_prefix:
        return value  # too short, just return as-is

    first_part = value[:keep_prefix]
    pattern_part = ""

    for char in value[keep_prefix:]:
        if char.isdigit():
            pattern_part += r'\d'
        elif char.isupper():
            pattern_part += '[A-Z]'
        elif char.islower():
            pattern_part += '[a-z]'
        elif char.isspace():
            pattern_part += ' '
        elif char in '.,()$+*{}%@<>#-':
            pattern_part += '\\' + char
        else:
            pattern_part += re.escape(char)

    # pattern is literally: first two chars + encoded rest
    return first_part + pattern_part


def generate_fake_data(regex_pattern, column_name, name=None):
    # Special handling for email
    if column_name.lower() == 'email address':
        return generate_fake_email(name)

    if not regex_pattern:
        return ""

    first_char = regex_pattern[0]
    second_char = regex_pattern[1]
    placeholders = []

    special_characters = '-.,()$+*{}%@<>#'

    # Everything after first two characters is pattern
    for match in re.finditer(r'(\[A-Z\]|\[a-z\]|\\d|[-.,()$+*{}%@<>#])',
                             regex_pattern[2:]):
        placeholders.append(match.group())

    fake_tail = ""

    for placeholder in placeholders:
        if placeholder == '[A-Z]':
            fake_tail += random.choice(string.ascii_uppercase)
        elif placeholder == '[a-z]':
            fake_tail += random.choice(string.ascii_lowercase)
        elif placeholder == r'\d':
            fake_tail += str(random.randint(0, 9))
        elif placeholder in special_characters:
            fake_tail += placeholder
        else:
            fake_tail += placeholder

    return first_char + second_char + fake_tail


def generate_fake_email(name):
    # Build local part from name
    if name and not pd.isna(name):
        words = str(name).split()
        first_word = re.sub(r'[^a-zA-Z0-9]', '', words[0]).lower()

        second_word = ""
        if len(words) > 1:
            second_word = re.sub(r'[^a-zA-Z0-9]', '', words[1]).lower()

        choices = [first_word]
        if second_word:
            choices.append(first_word + second_word)
            choices.append(first_word + second_word[0])

        local_part = random.choice(choices)
    else:
        # fallback to faker username
        local_part = faker.user_name()

    # optional digits
    num_digits = random.choices(
        [0, 2, 3, 4, 5, 6],
        weights=[0.3, 0.2, 0.1, 0.2, 0.1, 0.1]
    )[0]
    local_part += ''.join(random.choices(string.digits, k=num_digits))

    # domain
    domain_choices = (
        ['gmail.com'] * 18 +
        ['yahoo.com'] * 6 +
        ['aol.com', 'gmx.com', 'icloud.com',
         'mail.com', 'protonmail.com', 'zoho.com']
    )
    domain = random.choice(domain_choices)

    return f"{local_part}@{domain}"


def mask_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column_name in SENSITIVE_COLUMNS:
        if column_name not in df.columns:
            continue

        df[column_name] = df.apply(
            lambda row: generate_fake_data(
                generate_regex_pattern(row[column_name]),
                column_name,
                name=row.get('name')
            ),
            axis=1
        )

    return df
