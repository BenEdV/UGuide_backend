
# pylint: skip-file

# http://ubv.info/wp-content/uploads/2011/10/N1Moleculaire_Biologie_meerkeuzevragen.pdf
examdata = {
    # list of tuples of form (string:name, bool:studyconcept, bool:misconcept, int:weight, int:maxscore, int:minscore,
    # int:initialvalue, concept_key)
    "concepts": [("Structuur van biomoleculen", False, False, 10, 10, 0, 0),
                 ("Celprocessen", True, False, 10, 10, 0, 0),
                 ("Membranen", False, False, 5, 10, 0, 0),
                 ("Fotosynthese", True, False, 5, 10, 0, 0),
                 ("Celcycli", True, True, 5, 10, 0, 0),
                 ("Genen, DNA en ontwikkeling", True, True, 10, 10, 0, 0),
                 ("DNA replicatie en transcriptie", False, True, 5, 10, 0, 0),
                 ("RNA processing en translatie", False, True, 5, 10, 0, 0),
                 ("Mutatie", False, True, 5, 10, 0, 0),
                 ("Moleculaire celbiologische technieken", True, False, 5, 10, 0, 0)
                 ],

    # Answers have a list of concept values tuples of form (concept_id, value) with concept_id being the order above
    "questions": {
        1: {
            "question": "Na het mengen van door hitte gedode bacterien van een fluorescerende stam"
                        "met levende bacterien van een niet-fluorescerende stam, ontdek je dat"
                        "sommige van de levende cellen nu fluorescerend zijn Welke observaties"
                        "zouden het beste bewijs leveren dat het vermogen tot fluorescentie een"
                        "erfelijke eigenschap is?",
            "answers": {
                "A": ("Afstammelingen van de levende cellen zijn ook fluorescerend", [(1, 5), (2, 10)]),
                "B": ("DNA is verplaatst van de hitte gedode stam naar de levende stam", []),
                "C": ("Zowel DNA als eiwit verplaatsten zich van de hitte gedode stam naar de levende stam", [(2, 5)]),
                "D": ("Eiwit is overgedragen van de hitte gedode stam naar de levende stam", [(1, 5)]),
                "E": ("De fluorescentie in de levende stam is uitzonderlijk helder", [])
            },
            'correct': 'A'},
        2: {
            "question": "Wanneer T2 fagen bacterien infecteren en meer virussen maken in de"
                        "aanwezigheid van radioactief zwavel, wat is dan het resultaat?",
            "answers": {
                "A": ("Het bacteriele DNA zal radioactief worden", [(3, 10)]),
                "B": ("De virale eiwitten zullen radioactief worden", [(3, 10)]),
                "C": ("Het virale DNA zal radioactief worden", []),
                "D": ("Zowel A als B", [(5, 10)]),
                "E": ("Zowel A als C", [])
            },
            'correct': 'B'},
        3: {
            "question": "Om welke redenen verschilt replicatie in prokaryoten van replicatie in eukaryoten?",
            "answers": {
                "A": ("Prokaryoten hebben telomeren, eukaryoten niet", [(2, 5)]),
                "B": ("Prokaryotische chromosomen hebben een enkele oorsprong van" \
                      "replicatie (='ori'), terwijl eukaryotische chromosomen er meerdere" \
                      "hebben", [(2, 5), (3, 5)]),
                "C": ("De prokaryotische chromosomen hebben histonen, eukaryotische chromosomen hebben er geen", [(4, 5)]),
                "D": ("Prokaryoten produceren Okazaki-fragmenten gedurende DNAreplicatie, eukaryoten hebben er geen", []),
                "E": ("De snelheid van elongatie gedurende DNA-replicatie is langzamer in prokaryoten dan in eukaryoten", [])
            },
            'correct': 'B,E'},
        4: {
            "question": "Welke van de volgende nucleotiden-tripletten vertegenwoordigt het best een codon?",
            "answers": {
                "A": ("Een sequentie in tRNA aan het 3'einde", [(1, 5)]),
                "B": ("Een triplet dat geen corresponderend aminozuur bezit", [(6, 5)]),
                "C": ("Een triplet ruimtelijk gescheiden van andere tripletten", [(8, 5)]),
                "D": ("Een triplet in hetzelfde leesraam als een upstream AUG", [(2, 10), (1, 10)]),
                "E": ("Een triplet aan het tegenoverliggende einde van tRNA van de attachment site van het aminozuur", [])
            },
            'correct': 'D'},
        5: {
            "question": "Welk enzym veroorzaakt een covalente binding tussen lysine en de polypeptide keten?",
            "answers": {
                "A": ("ligase", []),
                "B": ("peptidyl transferase", [(0, 5), (2, 5)]),
                "C": ("lysine synthetase", []),
                "D": ("RNA-polymerase", []),
                "E": ("ATPase", [(5, 10)])
            },
            'correct': 'B'},
        6: {
            "question": "Wat is het effect van een nonsense mutatie in een gen?",
            "answers": {
                "A": ("Het verandert het leesraam van het mRNA", []),
                "B": ("Het voorkomt dat introns verwijderd worden", [(1, 10)]),
                "C": ("Het heeft geen effect op de volgorde van het aminozuur van het gecodeerde eiwit", []),
                "D": ("Het verandert een aminozuur in het gecodeerde eiwit", [(5, 5)]),
                "E": ("Het introduceert een voortijdig stopcodon in het mRNA", [(1, 10), (0, 10)])
            },
            'correct': 'E'},
        7: {
            "question": "Het verschijnsel waarbij RNA-moleculen in een cel worden vernietigd"
                        "wanneer ze een sequentie bezitten, complementair aan een geintroduceerd"
                        "dubbelstrengs RNA wordt genoemd:",
            "answers": {
                "A": ("RNA blocking", [(8, 10), (9, 10)]),
                "B": ("RNA obstructie", [(3, 10)]),
                "C": ("RNA interferentie", [(3, 10), (2, 10), (9, 10), (0, 5)]),
                "D": ("RNA targeting", [(0, 5)]),
                "E": ("RNA disposal", [])
            },
            'correct': 'C,D,E'},
        8: {
            "question": "Wat is de functie van 'reverse transcriptase' in retrovirussen?",
            "answers": {
                "A": ("Het hydrolyseert het DNA van de gastheer;", []),
                "B": ("Het zet het RNA van de cel van de gastheer om in viraal DNA;", [(3, 5)]),
                "C": ("Het gebruikt viraal RNA als een matrijs ('template') voor DNA-synthese", [(3, 10), (2, 10)]),
                "D": ("Het gebruikt viraal RNA als een matrijs om complementaire RNAstrengen te maken", []),
                "E": ("Het zet viraal RNA om in eiwit", [(5, 10)])
            },
            'correct': 'C'},
        9: {
            "question": "DNA-fragmenten worden van een gel overgebracht naar een nitrocellulose"
                        "papier gedurende de procedure die Southern blotting wordt genoemd, Wat is"
                        "de bedoeling van het overdragen van het DNA van een gel naar een"
                        "nitrocellulose drager?",
            "answers": {
                "A": ("om het DNA voor te bereiden op digestie met restrictie-enzymen", [(6, 5)]),
                "B": ("om de PCR's te verwijderen;", []),
                "C": ("om de twee complementaire DNA-strengen te scheiden;", [(0, 10), (1, 10)]),
                "D": ("om alleen het DNA over te brengen dat van belang is;", [(6, 5)]),
                "E": ("om de DNA-fragmenten aan een permanent substraat te laten hechten", [])
            },
            'correct': 'C,A'}
    },
    "results": {
        1: {"user_id": "person_1",
            "exam_id": 1,
            "date": "01/01/2001",
            "score": 90,
            "grade": 10,
            "question_results": {
                1: {"score": 10, "given_answer_id": "A"},
                2: {"score": 10, "given_answer_id": "B"},
                3: {"score": 10, "given_answer_id": "B"},
                4: {"score": 10, "given_answer_id": "D"},
                5: {"score": 10, "given_answer_id": "B"},
                6: {"score": 10, "given_answer_id": "E"},
                7: {"score": 10, "given_answer_id": "C"},
                8: {"score": 10, "given_answer_id": "C"},
                9: {"score": 10, "given_answer_id": "C"}}
            },
        2: {"user_id": "person_2",
            "exam_id": 1,
            "date": "01/01/2001",
            "score": 70,
            "grade": 7.78,
            "question_results": {
                1: {"score": 10, "given_answer_id": "A"},
                2: {"score": 10, "given_answer_id": "B"},
                3: {"score": 10, "given_answer_id": "B"},
                4: {"score": 10, "given_answer_id": "D"},
                5: {"score": 10, "given_answer_id": "B"},
                6: {"score": 10, "given_answer_id": "E"},
                7: {"score": 0, "given_answer_id": "A"},
                8: {"score": 0, "given_answer_id": "A"},
                9: {"score": 0, "given_answer_id": "A"}}
            },
        3: {"user_id": "person_3",
            "exam_id": 1,
            "date": "01/01/2001",
            "score": 50,
            "grade": 3.33,
            "question_results": {
                1: {"score": 10, "given_answer_id": "A"},
                2: {"score": 10, "given_answer_id": "B"},
                3: {"score": 10, "given_answer_id": "B"},
                4: {"score": 0, "given_answer_id": "A"},
                5: {"score": 0, "given_answer_id": "A"},
                6: {"score": 0, "given_answer_id": "A"},
                7: {"score": 0, "given_answer_id": "A"},
                8: {"score": 0, "given_answer_id": "A"},
                9: {"score": 0, "given_answer_id": "A"}}
            }
    },
    "persons": {
        1: {"user_name": "person_1",
            "display_name": "Test Person 1",
            "mail": "test_1@person.nl",
            "role": "student"},
        2: {"user_name": "person_2",
            "display_name": "Test Person 2",
            "mail": "test_2@person.nl",
            "role": "student"},
        3: {"user_name": "person_3",
            "display_name": "Test Person 3",
            "mail": "test_3@person.nl",
            "role": "student"}
    }
}

