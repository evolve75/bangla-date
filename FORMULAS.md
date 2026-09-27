# Formulas, Calculations, and Citations

This document records the astronomical formulas, constants, and citations behind
`bangla_date/_drik.py`, and how the test reference data is produced.

## Calendar rule

The runtime applies this project's chosen rule: a solar month is the Sun's
sidereal sign at local sunrise. The reference location is Kolkata, West Bengal
(22.5726 N, 88.3639 E). The Bengali year increments when Boishakh begins.

This is a project convention. It follows the general Indian/Bengali solar
calendar tradition of astronomical month lengths and sunrise-based days, but no
single authoritative source for this exact regional convention has been
established.

## Formula sources

| Component | Source |
| --- | --- |
| Solar longitude | Jean Meeus, *Astronomical Algorithms*, 2nd ed., ch. 25. The mean-longitude, mean-anomaly, equation-of-center, and aberration terms used here appear as equations 47-51 in R. Colonna and V. Tramutoli, "A New Model of Solar Illumination of Earth's Atmosphere during Night-Time", *Earth* 2021, 2(2), 191-207, [doi:10.3390/earth2020012](https://doi.org/10.3390/earth2020012), section 2.1.1; the coefficients were checked against that paper. |
| Sunrise geometry | NOAA, [General Solar Position Calculations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF), p. 2: the sunrise hour angle and `sunrise = 720 - 4*(longitude + ha) - eqtime`, with a 90.833-degree zenith. NOAA states its calculators are based on Meeus ([calculation details](https://gml.noaa.gov/grad/solcalc/calcdetails.html)); NOAA is a U.S. Government work. |
| Equation of time | Mean longitude minus right ascension, converted to hours (Meeus, ch. 28). |
| Obliquity | Meeus, ch. 22: 23°26'21.448" and -46.8150"/century. Colonna and Tramutoli eq. 52 lists the later 2010 Astronomical Almanac values (23°26'21.406", -46.836769"/century); this project retains the older values. |
| Ayanamsa | The runtime uses a project linear approximation: 23.85322 degrees at J2000 plus 50.2888"/year. It is compared approximately against a local evaluation of the `SE_SIDM_LAHIRI` precession model (Swiss Ephemeris `sweph.h`: t0 = JD 2435553.5, ayan_t0 = 23.250182778 - 0.004658035 degrees, IAU 1976 precession; from the Indian Astronomical Ephemeris 1989, p. 556). See "Lahiri comparison (approximate)" below. |
| Month boundary | The project's chosen rule: the Sun's sidereal sign at sunrise. The Wikipedia article [Bengali calendars](https://en.wikipedia.org/wiki/Bengali_calendar) provides background only (West Bengal month lengths as astronomical "exact periods", sunrise-based days); it does not establish this exact convention. |

## Constants used by the runtime

- Solar longitude (Meeus/NOAA, with `T` in Julian centuries from J2000):
  - mean longitude `280.46646 + 36000.76983 T + 0.0003032 T^2`
  - mean anomaly `357.52911 + 35999.05029 T - 0.0001537 T^2`
  - equation of center `(1.914602 - 0.004817 T - 0.000014 T^2) sin M + (0.019993 - 0.000101 T) sin 2M + 0.000289 sin 3M`
  - apparent longitude `true longitude - 0.00569 - 0.00478 sin(125.04 - 1934.136 T)`
- Obliquity: `23.439291 - 0.0130042 T` degrees.
- Ayanamsa: `23.85322 + (50.2888 / 3600) * years_from_J2000` degrees.
- Sunrise zenith: `90.833` degrees; the sunrise instant is solved by three
  fixed-point iterations of the hour angle.

## Lahiri comparison (approximate)

`tools/check_lahiri_fit.py` compares the runtime ayanamsa
(`bangla_date._drik._lahiri_ayanamsa`) with a local evaluation of the
`SE_SIDM_LAHIRI` precession model, sampled at January 1 for each year from 2000
to 2050:

- Runtime (imported from the package):
  `23.85322 + (50.2888 / 3600) * (JD - 2451545.0) / 365.25` degrees.
- Reference (local approximation): `ayan_t0 + (P(T) - P(T0)) / 3600` degrees,
  where `P(T) = 5029.0966 T + 1.11113 T^2 - 0.000006 T^3` arcseconds is the IAU
  1976 general precession in longitude (Lieske et al., 1977; also Meeus,
  *Astronomical Algorithms*, ch. 21), `T` is Julian centuries from J2000.0, `T0`
  corresponds to the `SE_SIDM_LAHIRI` epoch, and `ayan_t0 = 23.250182778 -
  0.004658035`.

Result: the maximum sampled difference is 14.33 arcseconds (0.00398 degrees), at
January 1, 2050. This is an approximate comparison against a local precession
model, not a verified Swiss Ephemeris computation; it bounds only the sampled
instants, not every instant in the interval.

A month is `floor(sidereal_longitude / 30)`, so the ayanamsa difference does not
by itself bound month-boundary changes: any difference, however small, can move a
month when sunrise falls close to a 30-degree sign boundary. Boundary-level
agreement is exercised separately by the reference rows (see "Test reference
data").

Swiss Ephemeris parameters were obtained by reading `sweph.h` at revision
`aloistr/swisseph@3feab6e88f1e642789028c6b8e6986f94b39bbff` (2023-11-29). Swiss
Ephemeris was not executed, and no Swiss Ephemeris code was copied or
redistributed; only published numerical facts are referenced, so no AGPL
obligation attaches.

## Test reference data

`tests/drik_reference.tsv` is generated independently of the runtime engine.

`tests/generate_drik_reference.py` computes, with PyEphem:

- local sunrise at Kolkata;
- the Sun's apparent ecliptic longitude of date;
- a True Chitrapaksha ayanamsa: Spica is fixed at sidereal longitude 180 degrees.

A solar month is the sign the Sun occupies at that sunrise.

The generator's True Chitrapaksha construction is distinct from the runtime's
`SE_SIDM_LAHIRI` approximation. It is an independent approximation, and its
agreement with the runtime does not validate the runtime's exact Lahiri
definition or the project's month-boundary convention.

Generate or verify it with CPython 3.13.7 and PyEphem 4.2.1 in an isolated
environment:

```bash
uv run --no-project --python 3.13.7 --with ephem==4.2.1 python tests/generate_drik_reference.py --check
```

`--check` compares the generated UTF-8/LF bytes with the committed file without
writing it and exits nonzero on a difference. To write a copy elsewhere for
diffing:

```bash
uv run --no-project --python 3.13.7 --with ephem==4.2.1 python tests/generate_drik_reference.py --output /tmp/drik_reference.tsv
diff -u tests/drik_reference.tsv /tmp/drik_reference.tsv
```

Omit `--check` and `--output` to regenerate the tracked file. Do not edit
reference rows manually. The generator prints the Python/PyEphem versions and the
SHA-256 digest.

The verified baseline is 240 data rows with SHA-256
`8a400aba62a6aab25c39083e702ac7ef2c785a745682675c3d802a2560be7181`.

## Dependency licensing

The reference generator uses [PyEphem](https://pypi.org/project/ephem/) 4.2.1.
Its `LICENSE` grants MIT terms for both the libastro component (Elwood Downey) and
the Python package/updates (Brandon Rhodes). The
[source distribution](https://files.pythonhosted.org/packages/37/f0/a38e882d3c73bb8bcc37a0a27c9a7b8fceb7906312006fb03c01d0a098b3/ephem-4.2.1.tar.gz)
has SHA-256 `920cb30369c79fde1088c2060d555ea5f8a50fdc80a9265832fd5bf195cf147f`.
PyEphem is a reference-generation-only dependency, not a runtime dependency.
