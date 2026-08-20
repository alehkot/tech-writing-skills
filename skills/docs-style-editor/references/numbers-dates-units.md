# Numbers, Dates, and Units

## Use When

Load this reference for the numeric pass: numbers, dates, times, units of measure, mathematical notation, and phone-number formatting.

## Scope Notes

- Never change a number, unit, or date that carries a fact. Reformat it; if the correct form depends on information the source does not supply, such as a time zone or a byte system, flag the value instead of choosing one.
- Reproduce numbers inside commands, code, sample output, and quoted strings exactly as the source shows them.

## Numbers

- Spell out zero through nine in body prose, and use numerals from 10 upward.
- Use numerals at any size for versions, technical quantities, memory and storage sizes, rates, limits, prices, step and page numbers, percentages, decimals, dimensions, measurements, negatives, and ranges.
- When numbers below 10 and above nine share a sentence, write them all as numerals: `18 checks ran and 4 failed.`
- Do not open a sentence with a numeral: spell the number out or restructure the sentence. A four-digit year may open a sentence when no restructuring reads well.
- Spell out a number that immediately precedes a numeral: `twelve 4 KB blocks`.
- Write ordinals as words: `second`, `ninth`, `twenty-first`, never `2nd` or `21st`.
- Avoid Roman numerals except as procedure sub-step labels.
- Prefer decimals to fractions, and hyphenate a spelled-out fraction: `two-thirds`.
- Put a zero before a bare decimal point, and treat a decimal quantity as plural: `0.5 seconds`, `1.0 seconds`.
- Attach `%` directly to the numeral with no space, and spell out both the number and `percent` only at the start of a sentence.
- Group digits with commas from four digits up, use a period as the decimal mark, and add no separators after the decimal point: `12,480` and `0.004512`.
- Write a numeric range as numeral-hyphen-numeral with no spaces: `4-8 replicas`. Use suspended hyphens when several hyphenated number compounds share a base: `one-, two-, or four-node clusters`.
- Format US currency with a leading `$`, comma thousands separators, and digits only after the decimal point: `$14,200`, `$0.0043`.
- Write dimensions as numerals joined by a lowercase `x` with no spaces: `512x512`.
- Keep a number and the noun or unit it modifies on one line with a nonbreaking space where wrapping would separate them.
- Never invent a real-world implication for a number. Cite the source that supplies the context, or state the number alone.

## Dates

- Spell out the month and use a four-digit year: `March 14, 2026`. If a weekday appears, put it first: `Saturday, March 14, 2026`.
- Use no comma between a month and a year alone: `in March 2026`. Add a comma after the year when a full date sits mid-sentence: `the March 14, 2026, release`.
- Never write a slash- or period-separated numeric date. When a numeric-only date is required, use ISO 8601: `2026-03-14`.
- Abbreviate a date only where space is tight, and then abbreviate every part of it — three letters, capitalized, no period — and abbreviate consistently across the document: `Sat, Mar 14, 2026`.
- Choose an example date whose day number is greater than 12 so the day cannot be read as a month.
- Put the date before the time when both appear: `March 14, 2026, at 3 PM`. Use a 24-hour time only under the documented-interface exception: `2026-03-14 at 15:00 UTC`.

## Times

- Use the 12-hour clock with capitalized `AM` or `PM`, one preceding space, and no minutes on a round hour: `4 PM`, `4:30 PM`. Match a documented 24-hour interface instead, and then use 24-hour time throughout the page.
- Write a time range with a hyphen and no spaces: `2-6 minutes`.
- Avoid naming a time zone. When one is required, name the region the zone belongs to, spell the zone out, and append the UTC offset: `US and Canadian Eastern Standard Time (UTC-5)`. Never abbreviate the zone name, and never leave the region out, because one zone name can cover several regions.
- Never use a season to express timing; name a month or a quarter.

## Units of Measure

- Separate a numeral from its unit abbreviation with a space, ideally one that does not break across lines, and leave the abbreviation singular: `16 GB`, not `16GB` or `16 GBs`.
- Close up currency symbols, percent signs, and angle degrees against the numeral: `$18`, `40%`, `90°`.
- Put a space before a temperature degree symbol and none between the symbol and the scale letter: `35 °C`. Write Kelvin with a space and no degree symbol: `450 K`.
- Do not hyphenate a number and an abbreviated unit that modify a noun: `a 200 GB volume`. Hyphenate the spelled-out form: `a 64-bit build`.
- Repeat the unit on every endpoint of a range and join the endpoints with `to`, because a hyphen reads as a minus sign: `-20 °C to 60 °C`.
- Hyphenate a unit formed by multiplying two units: `12 GPU-hours`, `9 engineer-days`.
- Close up a lowercase `k` for thousands against the number and name the counted noun: `20k read operations`.
- Prefix an ambiguous currency amount with a country indicator: `US$40`.
- Write rates with `per` in prose and keep the slash for space-constrained tables; use established rate abbreviations such as `Mbps`, never `Mb/s`.
- Use the byte system the documented technology actually uses, decimal or binary; a wrong byte unit is a factual error (canonical ruling: reference-docs-writer).
- Write version ranges as `2.2 or later` and `2.2 or earlier` (canonical ruling: reference-docs-writer), and remember that the highest version number is not necessarily the most recent release.

## Mathematical Notation

- Italicize variables and leave operators upright: *a* − *b*.
- Write a minus sign as a true minus, not a hyphen.
- Never mark exponentiation with a caret or multiplication with a bare asterisk in prose. Use superscript notation, a multiplication sign, or unambiguous juxtaposition.
- Keep a short expression inline and give a long or wrap-prone equation its own line; keep the operands and operator together so the expression does not wrap.
- Choose notation only when it reads unambiguously, and switch to words when symbols would be ambiguous or ungrammatical. Avoid: Compute w × h for the region. Prefer: Multiply the width by the height.

## Phone Numbers

- Draw every example phone number from the reserved fictional range (values: [safe-example-values.md](safe-example-values.md)).
- Join the groups of a number with nonbreaking hyphens so it never wraps: `415-555-0132`.
- Put a plus sign directly against the country code of an international number: `+1-415-555-0132`.
- Append an extension as a comma, the word `extension`, and the number: `415-555-0132, extension 987`.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
