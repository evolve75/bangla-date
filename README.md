## বাংলা তারিখ রূপান্তরকারী (Bangla Date)

এই প্রজেক্টটি গ্রেগরিয়ান তারিখকে বাংলা তারিখে রূপান্তর করে এবং সংশ্লিষ্ট ঋতুসহ বাংলা সংখ্যায় প্রদর্শন করে। এটি একটি importable Python module এবং একটি সহজ CLI - দুটোই সরবরাহ করে।

এটি পশ্চিমবঙ্গে প্রচলিত বাংলা পঞ্জিকা (দৃক সিদ্ধান্ত) ব্যবহার করে; মাস নির্ধারিত হয় কলকাতার সূর্যোদয়ের সময় সূর্যের সায়ন রাশি অনুসারে, তাই মাসের দৈর্ঘ্য ২৯ থেকে ৩২ দিন পর্যন্ত পরিবর্তিত হয়। এটি বাংলাদেশের ২০১৯-সংশোধিত জাতীয় পঞ্জিকার সমান নয়।

### বৈশিষ্ট্যসমূহ

- গ্রেগরিয়ান তারিখ থেকে বাংলা তারিখে রূপান্তর।
- বাংলা মাস ও ঋতু নির্ণয় (পশ্চিমবঙ্গের প্রচলিত দৃক সিদ্ধান্ত পঞ্জিকা অনুসারে)।
- আউটপুটে বাংলা সংখ্যা ব্যবহার।
- সূর্যোদয়ের সময় সূর্যের সায়ন রাশি অনুসারে পরিবর্তনশীল মাসের দৈর্ঘ্য (২৯–৩২ দিন) গণনা (রেফারেন্স স্থান: কলকাতা)।

### প্রয়োজনীয়তা

- Python 3.13 বা নতুনতর

### ইনস্টলেশন

1. এই রিপোজিটরি ক্লোন করুন।
2. আপনার সিস্টেমে Python 3.13+ ইনস্টল করুন।
3. ডেভেলপমেন্ট নির্ভরতাসহ পরিবেশ প্রস্তুত করুন:

```bash
uv sync
```

`uv` ছাড়া ঐচ্ছিকভাবে editable install করতে পারেন:

```bash
python3 -m pip install -e .
```

### ব্যবহারবিধি

টার্মিনালে নিচের যেকোনো একটি কমান্ড চালান:

```bash
python3 -m bangla_date
```

অথবা compatibility wrapper ব্যবহার করতে চাইলে:

```bash
python3 bangla-date.py
```

ইনস্টল করা entrypoint থাকলে:

```bash
bangla-date
```

সাহায্য বা সংস্করণ দেখতে চাইলে:

```bash
python3 -m bangla_date --help
python3 -m bangla_date --version
```

কমান্ডটি বর্তমান দিনের বাংলা তারিখ এবং ঋতু প্রদর্শন করবে।

### কাস্টম ইনপুট

নির্দিষ্ট কোনো গ্রেগরিয়ান তারিখের বাংলা তারিখ জানতে চাইলে module থেকে helper function import করতে পারেন। উদাহরণস্বরূপ:

```python
from datetime import datetime

from bangla_date import english_to_bangla_digits
from bangla_date import gregorian_to_bangla_date

# নির্দিষ্ট গ্রেগরিয়ান তারিখ
gregorian_date = datetime(2024, 11, 10)
bangla_day, bangla_month, bangla_year, bangla_season = gregorian_to_bangla_date(gregorian_date)

print(
    f"{english_to_bangla_digits(bangla_day)} {bangla_month}, "
    f"{english_to_bangla_digits(bangla_year)} বঙ্গাব্দ - ঋতু: {bangla_season}"
)
```

সরাসরি প্রস্তুত আউটপুট চাইলে `format_bangla_date` ব্যবহার করুন:

```python
from datetime import datetime

from bangla_date import format_bangla_date

print(format_bangla_date(datetime(2024, 11, 10)))
```

Bangla-named function গুলোও backward compatibility এর জন্য রাখা হয়েছে:

```python
from bangla_date import গ্রেগরিয়ান_থেকে_বাংলা_তারিখ
from bangla_date import ইংরেজি_থেকে_বাংলা_সংখ্যা
```

### টেস্ট

```bash
uv run pytest
```

`uv` ছাড়া standard library runner দিয়েও চালানো যায়:

```bash
python3 -m unittest discover -s tests
```

### অবদান

যদি আপনি এই প্রকল্পে অবদান রাখতে চান, অনুগ্রহ করে একটি পুল রিকোয়েস্ট জমা দিন বা ইস্যু তৈরি করুন।

### Formulas and provenance

The astronomical formulas, constants, and citations used by the engine, and the
method and command for reproducing the test reference data, are documented in
[FORMULAS.md](FORMULAS.md).

In summary: the engine uses the project's rule (the Sun's sidereal sign at
Kolkata sunrise), the Meeus/NOAA solar longitude series, and a linear
approximation of the Lahiri ayanamsa.

### লাইসেন্স

এই প্রকল্পটি MIT লাইসেন্স এর অধীনে প্রকাশিত।
