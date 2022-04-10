
# pylint: skip-file

examdata = {
    # list of tuples of form (string:name, bool:studyconcept, bool:misconcept, int:weight, int:maxscore, int:minscore,
    #     int:initialvalue)
    "concepts": [
        ("Meiosis", False, False, 10, 10, 0, 0),
        ("Evolutie", True, False, 10, 10, 0, 0),
        ("Dieren", False, False, 5, 10, 0, 0),
        ("Theologisch", False, True, 5, 10, 0, 0)],
    # list of tuples of form (int:value, concept_key, int:questnum, int:answer
    # num)

    "questions": {
        1: {"question": "De efficientie van een organisatie wordt vergroot door",
            "answers": {
                "A": ("arbeidsverdeling en specialisatie.", [(1, 10)]),
                "B": ("inzet van meer middelen.", []),
                "C": ("inzet van meer personeel.", [(1, 5)]),
                "D": ("vermindering van het management.", [])
            },
            "correct": "A"},
        2: {"question": "Arbeidsverdeling vereist",
            "answers": {
                "A": ("coordinatie van taken.", [(2, 10)]),
                "B": ("autonomie van de medewerkers.", []),
                "C": ("top-down-management.", []),
                "D": ("bottom-up-informatie", []),
                "E": ("kennis van de management", [])},
            "correct": "A"},
        3: {
            "question": "Het streven naar invloed van de samenleving op de doelen en werkwijze van "
            "particuliere instellingen heet",
            "answers": {
                "A": ("externe democratisering.", [(1, 10)]),
                "B": ("bureaucratisering.", []),
                "C": ("interne democratisering.", [])},
            "correct": "A,B"},
        4: {"question": "Feedback is in essentie:",
            "answers": {
                "A": ("checken of de doelen worden bereikt en of de omgeving zich wijzigt.", [(0, 10)]),
                "B": ("vergroten van de input.", []),
                "C": ("verbeteren van de communicatie in de instelling.", []),
                "D": ("verbeteren van het management van de instelling.", [])},
            "correct": "A"},
        5: {"question": "De mate waarin de beoogde doelen worden bereikt is",
            "answers": {
                "A": ("de effectiviteit.", []),
                "B": ("de efficientie.", [(3, 10)]),
                "C": ("het ondernemerschap.", []),
                "D": ("de duurzaamheid.", [])},
            "correct": "A"},
        6: {
            "question": "De mate waarin de middelen worden ingezet voor het bereiken van de beoogde doelen "
            "is",
            "answers": {
                "A": ("de efficientie.", [(1, 10)]),
                "B": ("de effectiviteit.", []),
                "C": ("de stuurbaarheid.", []),
                "D": ("de financierbaarheid.", [(3, 10)])},
            "correct": "A"},
        7: {"question": "'Not-for-profit' wil zeggen:",
            "answers": {
                "A": ("hoewel de organisatie geen winst nastreeft, behandelt zij haar doelgroep wel als " \
                      "klanten die kwaliteit willen.", [(1, 10)]),
                "B": ("hoewel de organisatie geen winst nastreeft, maakt zij in feite wel winst door niet " \
                      "alle inkomsten te gebruiken voor de beoogde doelen.", []),
                "C": ("de klant mag niet betalen voor de ontvangen diensten.", [(3, 5)]),
                "D": ("de overheid is bereid eventuele tekorten van de organisatie aan te zuiveren.", [])},
            "correct": "A"},
        8: {"question": "Kenmerkend verschil tussen profit- en non-profitorganisaties is",
            "answers": {
                "A": ("dat bij profitorganisaties de klant direct aan de organisatie voor geleverde diensten " \
                      "betaalt, bij non-profitorganisaties is er geen directe financiele band tussen klant en " \
                      "instelling.", [(2, 10)]),
                "B": ("dat profitorganisaties een professioneel management hebben, terwijl "
                      "non-profitorganisaties worden geleid door vrijwilligers.", []),
                "C": ("dat de overheid voor profitorganisaties geen wetgevend kader geeft, terwijl dat wel "
                      "gebeurt voor non-profitorganisaties", [(2, 5)]),
                "D": ("dat bij profitorganisaties mensen in loondienst werken, terwijl dat niet mag bij "
                      "nonprofitorganisaties.", [])},
            "correct": "A"},
        9: {"question": "Bij 'ingebouwde hulpverlening'",
            "answers": {
                "A": ("is de hulpverlening niet het hoofddoel van de organisatie, maar de hoofdtaak van een "
                      "afdeling binnen die grotere organisatie.", [(2, 10)]),
                "C": ("is hulpverlening het hoofddoel van de organisatie, en zijn er andere doelen (niet "
                      "hulpverlening) van afdelingen binnen die grotere organisatie.", []),
                "B": ("heeft een organisatie een aantal hoofddoelen, waaronder hulpverlening.", []),
                "D": ("huurt een organisatie hulpverlening in indien dat nodig is voor leden van die "
                      "organisatie.", [(3, 5)])},
            "correct": "A"},
        10: {"question": "De feitelijke doelen van een organisatie zijn af te leiden uit",
             "answers": {
                 "A": ("de werkwijze van de organisatie.", [(1, 10)]),
                 "B": ("de statuten van de organisatie.", [])},
             "correct": "A"},
        11: {"question": "Volgens de auteurs is het belangrijk",
             "answers": {
                 "A": ("dat je persoonlijke doelen en de doelen van de organisatie niet geheel samenvallen.",
                       [(1, 10)]),
                 "B": ("dat je persoonlijke doelen en de doelen van de organisatie geheel samenvallen.", []),
                 "C": ("dat je persoonlijke doelen en de doelen van de organisatie nergens overlappen.", []),
                 "D": ("Iis er geen oordeel te geven over de overeenkomsten en verschillen van je "
                       "persoonlijke doelen en de doelen van de organisatie.", [(3, 5)])},
             "correct": "A"},
        12: {"question": "De structuur van een organisatie is",
             "answers": {
                 "A": ("de min of meer vaste relatie tussen de onderdelen van de organisatie.", [(0, 10)]),
                 "B": ("de opeenvolging van processen in een organisatie.", []),
                 "C": ("de richting van de communicatie in een organisatie (top-down of bottom-up).", []),
                 "D": ("de plaats van de organisatie in het krachtenveld van subsidiegevers en klanten.", [])},
             "correct": "A"},
        13: {
            "question": "Intake doen, huisbezoek afleggen en administratie bijhouden zijn voorbeelden van "
            "het structureren van de volgende zaken binnen een organisatie:",
            "answers": {
                "A": ("taken.", [(0, 10)]),
                "B": ("functies.", []),
                "C": ("afdelingen.", []),
                "D": ("hierarchie.", [])},
            "correct": "A"},
        14: {"question": "Kenmerk van een verticale organisatie is",
             "answers": {
                 "A": ("dat functionarissen en afdelingen op verschillend hierarchisch niveau staan.", [(0, 10)]),
                 "B": ("dat de uitvoerende functionarissen zich op grond van hun deskundigheid boven de " \
                       "klant stellen.", []),
                 "C": ("dat de medewerkers binnen een organisatie de leiding adviseren over het te voeren " \
                       "beleid.", []),
                 "D": ("dat de organisatie ondergeschikt is aan externe doelbepalers of subsidiegevers.", [])},
             "correct": "A"},
        15: {"question": "Kenmerk van een horizontale organisatie is",
             "answers": {
                 "A": ("dat alle functionarissen in de organisatie op gelijk niveau staan en er dus geen " \
                       "hierarchische verschillen zijn.", [(2, 10)]),
                 "B": ("dat de uitvoerende functionarissen zich niet boven of onder de klanten stellen, maar " \
                       "daarmee op gelijk niveau staan.", []),
                 "C": ("dat de leiding en de medewerkers binnen een organisatie op eenzelfde kennis- en " \
                       "opleidingsniveau zitten.", []),
                 "D": ("dat alle functionarissen in de organisatie op gelijk salarisniveau zitten.", [])},
             "correct": "A"},
        16: {"question": "Een voorbeeld van een platte organisatie is:",
             "answers": {
                 "A": ("een advocatencollectief.", [(2, 10)]),
                 "B": ("een afdeling binnen een ziekenhuis.", []),
                 "C": ("de ambtelijke structuur van een gemeentehuis.", []),
                 "D": ("het leger.", [])},
             "correct": "A"}
    }
}
