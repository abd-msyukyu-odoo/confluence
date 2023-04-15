import calendar, datetime, pytz, random
from django.conf import settings

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

def generate_syllable(seed=int('111', 2)):
    """Generate a random syllable"""
    seed = seed or random.randint(int('1', 2), int('111', 2))
    c1 = ((seed & int('100', 2)) and random.choice(CONSONANTS)) or ''
    v = ((seed & int('010', 2)) and random.choice(VOWELS)) or ''
    c2 = ((seed & int('001', 2)) and random.choice(CONSONANTS)) or ''
    return ''.join([c1, v, c2])

def generate_word(syllable_count):
    """Generate a random word with the specified number of syllables"""
    syllable_count = syllable_count if syllable_count > 1 else 2
    return ''.join(
        [generate_syllable(0)] +
        [generate_syllable() for _ in range(syllable_count - 2)] +
        [generate_syllable(0)]
    )

def generate_random_word(min_syllables=2, max_syllables=4):
    """Generate a random word with a random number of syllables between min_syllables and max_syllables"""
    syllable_count = random.randint(min_syllables, max_syllables)
    return generate_word(syllable_count)

def generate_random_phone():
    """Generate a random belgian phone number"""
    prefix = '+32'
    root = f"{random.randint(0, 999):03}"
    suffix = f"{random.randint(0, 999999):06}"
    return ''.join([prefix, root, suffix])

def generate_random_email():
    """Generate a random belgian email"""
    prefix = '.'.join(generate_random_word() for _ in range(2))
    root = '@'
    suffix = generate_random_word()
    domain = '.be'
    return ''.join([prefix, root, suffix, domain])

def generate_random_date(year_range=60, year_offset=-65):
    now = datetime.date.today()
    year = now.year + year_offset + random.randint(0, year_range)
    month = random.randint(1, 12)
    day = random.randint(1, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def generate_random_datetime(year_range=2, year_offset=-1, after=None, before=None):
    tz = pytz.timezone(settings.TIME_ZONE)
    hour = random.randint(0, 23)
    hour_delta = random.randint(1, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    delta = datetime.timedelta(hours=hour_delta, minutes=minute, seconds=second)
    if after:
        return after - delta
    elif before:
        return before + delta
    else:
        date = generate_random_date(year_range, year_offset)
        return datetime.datetime.combine(date, datetime.time(hour, minute, second), tzinfo=tz)

def generate_random_positive_integer(max=30):
    return random.randint(0, max)

def generate_random_boolean():
    return random.choice([True, False])
