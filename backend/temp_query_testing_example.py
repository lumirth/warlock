from app.models import load_pickles, parse_string_into_parameters

pickles = load_pickles("backend/data")
print(parse_string_into_parameters("cs 225", pickles))

example_queries = [
    "cs",
    "adv comp",
    "CS 222",
    "math257",
    "pysch 101",
    "MACS, western",
    "hrs:1, is:online",
    "gen:HUM",
    "adv comp, pot:b",
    "prof: wade",
    "keyword: data",
    "life sciences",
    "natural sciences, quant1",
    "PSYC, non-western",
    "fall, 2021, cs 128",
    "anthropology, 2019",
    "2005, mathematics, hrs:2",
    "design lab",
    "math, quant 1",
    "math, quant 2",
    "cs 2",
    "k: data structures",
    "math, quant",
    "nat sci tech, quant",
    "nat sci tech, quant 1",
    "nat sci tech, g:QR1"
    # "crn: 12345, gen ed: Humanities - Hist & Phil",
    # "id: 101, subj: ece, pot: first, instructor: John Smith",
]
# TODO: investigate why quant is buggy.

for query in example_queries:
    print(query)
    print(parse_string_into_parameters(query, pickles))
    print()