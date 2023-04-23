# Query Parsing Design Document

This document explains the query parsing process in detail for the given Python script. The parsing process aims to convert an input string into an `AdvancedSearchParameters` object, which can be used to filter search results.

## Overview

A query is a comma-separated list of arguments. Arguments can be in the following forms:

1. Colon-separated key-value pairs
2. Course subject and number
3. Token with optional digits
4. Year, Semester, or CRN tokens

Each argument type is parsed and processed, eventually updating the `AdvancedSearchParameters` object accordingly.

## Argument Types

### Colon-separated Key-Value Pairs

These arguments have the format `key:value`. Valid keys are defined in the `COLON_ARGS` and `IS_ARGS` dictionaries. They are parsed by the `parse_colon_arguments` function. For example:

- Year: `year:2012`, `yr:2012`, `yr:23`
- Semester: `sem:spring`, `sem:sp`, `sem:fall`, `sem:fa`
- Part of Term: `pot:a`, `pot:b`
- Department: `dep:chem`, `subj:chem`

### Course Subject and Number

These arguments are a combination of a subject (a string of alphabetic characters) and a course number (a string of digits). They are parsed by the `parse_subject_and_course_number` function. Fuzzy matching is used to match the input subject to a valid subject in the `SUBJECTS` dictionary if the input is not an exact match. For example:

- `CS 101`
- `math 241`

### Token with Optional Digits

These arguments are a string of alphabetic characters, optionally followed by digits. They are parsed by the `parse_optional_digits_pattern` function. Fuzzy matching is used to match the input token to a valid gen ed or subject in the `GEN_EDS` and `SUBJECTS` dictionaries, respectively. If the input token matches a gen ed, it will be added to the `gened_reqs` property of the `AdvancedSearchParameters` object. For example:

- `MACS`
- `western`

### Year, Semester, or CRN tokens

These arguments are specific tokens that can be identified by the `token_is_year`, `token_is_semester`, and `token_is_crn` functions. For example:

- Year: `2012`
- Semester: `spring`, `sp`, `fall`, `fa`
- CRN: `12345`

## Parsing Process

The main parsing process is implemented in the `parse_advanced_query_string` function. It splits the input string by commas and iterates through each token, calling the `parse_token` function to process each token.

The `parse_token` function checks the format of the token and delegates the processing to the appropriate parsing function for each argument type. The parsing functions then update the `AdvancedSearchParameters` object accordingly.

Fuzzy matching is employed in the `parse_subject_and_course_number` and `parse_optional_digits_pattern` functions to find the best match for the input token among the valid gen eds and subjects. The `fuzz.token_set_ratio` scoring method from the `fuzzywuzzy` library is used to measure similarity.

After all tokens are processed, the `align_to_pattern` function is called to ensure that the `AdvancedSearchParameters` object conforms to the expected format.

## Example Query

An example query could look like this:

- `MACS, western, is:online`

This query would be parsed into an `AdvancedSearchParameters` object with the following properties:

  - subject             : MACS
  - gened_reqs          : ['1WCC']
  - online              : True