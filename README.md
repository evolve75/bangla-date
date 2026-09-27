## বাংলা তারিখ রূপান্তরকারী (Bangla Date)

[![CI](https://github.com/evolve75/bangla-date/actions/workflows/ci.yml/badge.svg)](https://github.com/evolve75/bangla-date/actions/workflows/ci.yml)

এই প্রজেক্টটি গ্রেগরিয়ান তারিখকে বাংলা তারিখে রূপান্তর করে এবং সংশ্লিষ্ট ঋতুসহ বাংলা সংখ্যায় প্রদর্শন করে। এটি একটি importable Python module এবং একটি সহজ CLI - দুটোই সরবরাহ করে।

এটি পশ্চিমবঙ্গে প্রচলিত বাংলা পঞ্জিকা (দৃক সিদ্ধান্ত) ব্যবহার করে; মাস নির্ধারিত হয় কলকাতার সূর্যোদয়ের সময় সূর্যের সায়ন রাশি অনুসারে, তাই মাসের দৈর্ঘ্য ২৯ থেকে ৩২ দিন পর্যন্ত পরিবর্তিত হয়। এটি বাংলাদেশের ২০১৯-সংশোধিত জাতীয় পঞ্জিকার সমান নয়।

### বৈশিষ্ট্যসমূহ

- গ্রেগরিয়ান তারিখ থেকে বাংলা তারিখে রূপান্তর।
- বাংলা মাস ও ঋতু নির্ণয় (পশ্চিমবঙ্গের প্রচলিত দৃক সিদ্ধান্ত পঞ্জিকা অনুসারে)।
- আউটপুটে বাংলা সংখ্যা ব্যবহার।
- সূর্যোদয়ের সময় সূর্যের সায়ন রাশি অনুসারে পরিবর্তনশীল মাসের দৈর্ঘ্য (২৯–৩২ দিন) গণনা (রেফারেন্স স্থান: কলকাতা)।
- কোনো runtime dependency নেই।

### প্রয়োজনীয়তা

- Python 3.13 বা নতুনতর

### ইনস্টলেশন

`uv` দিয়ে CLI টুল হিসেবে সরাসরি ইনস্টল:

```bash
uv tool install "git+https://github.com/evolve75/bangla-date"
```

লোকাল ক্লোন থেকে ইনস্টল:

```bash
git clone https://github.com/evolve75/bangla-date
cd bangla-date
uv tool install .
```

ডেভেলপমেন্টের জন্য নির্ভরতাসহ পরিবেশ প্রস্তুত:

```bash
uv sync
```

`uv` ছাড়া ঐচ্ছিকভাবে editable install:

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
bangla-date --help
bangla-date --version
```

কমান্ডটি বর্তমান দিনের বাংলা তারিখ এবং ঋতু প্রদর্শন করবে।

### কাস্টম ইনপুট ও উদাহরণ

নির্দিষ্ট কোনো গ্রেগরিয়ান তারিখের বাংলা তারিখ জানতে module থেকে helper function ব্যবহার করুন। উদাহরণ — পহেলা বৈশাখ (১৫ এপ্রিল ২০২৬):

```python
from datetime import date

from bangla_date import english_to_bangla_digits, gregorian_to_bangla_date

# পহেলা বৈশাখ ১৪৩৩
gregorian_date = date(2026, 4, 15)
bangla_day, bangla_month, bangla_year, bangla_season = gregorian_to_bangla_date(gregorian_date)

print(
    f"{english_to_bangla_digits(bangla_day)} {bangla_month}, "
    f"{english_to_bangla_digits(bangla_year)} বঙ্গাব্দ — ঋতু: {bangla_season}"
)
```

আউটপুট:

```
১ বৈশাখ, ১৪৩৩ বঙ্গাব্দ — ঋতু: গ্রীষ্ম
```

সরাসরি প্রস্তুত আউটপুট চাইলে `format_bangla_date` ব্যবহার করুন:

```python
from datetime import date

from bangla_date import format_bangla_date

print(format_bangla_date(date(2026, 4, 15)))
```

public API-তে বাংলা-নামক ফাংশন এবং ইংরেজি alias — দুটোই আছে:

```python
from bangla_date import gregorian_to_bangla_date, english_to_bangla_digits
from bangla_date import গ্রেগরিয়ান_থেকে_বাংলা_তারিখ, ইংরেজি_থেকে_বাংলা_সংখ্যা
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

### সূত্র ও উৎস (Formulas and provenance)

ইঞ্জিনে ব্যবহৃত জ্যোতির্বিজ্ঞান সূত্র, ধ্রুবক এবং তাদের সূত্রনির্দেশ, এবং টেস্ট রেফারেন্স ডেটা পুনরুৎপাদনের পদ্ধতি ও কমান্ড — সবই [FORMULAS.md](FORMULAS.md)-এ নথিবদ্ধ।

সংক্ষেপে: ইঞ্জিনটি এই প্রকল্পের নির্বাচিত নিয়ম (কলকাতার সূর্যোদয়ের সময় সূর্যের সায়ন রাশি), Meeus/NOAA সৌর দ্রাঘিমা সিরিজ, এবং লাহিড়ী অয়নাংশের একটি রৈখিক আসন্ন মান ব্যবহার করে।

### লাইসেন্স

এই প্রকল্পটি MIT লাইসেন্স এর অধীনে প্রকাশিত।
