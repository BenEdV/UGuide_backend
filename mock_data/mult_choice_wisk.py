
# pylint: skip-file

examdata = {
    # list of tuples of form (string:name, bool:studyconcept, bool:misconcept, int:weight, int:maxscore, int:minscore, int:initialvalue)
    "concepts": [],
    # list of tuples of form (int:value, concept_key, int:questnum, int:answer num)

    "questions": {
        1: {
            'question': "Een cirkel heeft een diameter van 3 meter. Hoe groot is de oppervlakte van de cirkel, afgerond"
                        " op gehele m2 ?",
            'answers': {
                "A": ("19 m2", []),
                "B": ("9 m2", []),
                "C": ("7 m2", []),
                "D": ("28 m2", [])
            },
            'correct': 'A'},
        2: {
            'question': "Het aantal konijnen N in een bepaald heidegebied neemt toe volgens de formule N=42 x 1,12t. "
                        "Hierin stelt t het aantal maanden voor. Bij t=0 hoort 1 januari 2008. Met hoeveel procent is "
                        "het aantal konijnen toegenomen op 1 juni 2008, in vergelijking met 1 januari 2008?",
            'answers': {
                "A": ("76%", []),
                "B": ("74%", []),
                "C": ("32%", []),
                "D": ("97%", [])
            },
            'correct': 'A'},
        3: {'question': "Zie de schets van de driehoek hiernaast. Hoeveel graden is A?",
            'answers': {
                "A": ("35o", []),
                "B": ("55o", []),
                "C": ("30o", []),
            },
            'correct': 'A'},
        4: {
            'question': "Zie nogmaals de schets van de driehoek hiernaast. Hoe lang is AB in een decimaal nauwkeurig?",
            'answers': {
                "A": ("33,0", []),
                "B": ("8,1", []),
                "C": ("5,7", [])
            },
            'correct': 'A'},
        5: {'question': "Bij een winkel is een trui in prijs verhoogd met 21% tot 54,39. Wat was de oude prijs?",
            'answers': {
                "A": ("44,95", []),
                "B": ("42,97", []),
                "C": ("geen van beide", [])
            },
            'correct': 'A'},
        6: {
            'question': "Een taxichauffeur rekent per rit een vast bedrag van 5 en daarnaast nog een bedrag van 1,50 "
                        "per gereden kilometer. Hoe ziet de woordformule eruit waarmee deze chauffeur de totale "
                        "ritprijs berekent?",
            'answers': {
                "A": ("ritprijs=5,00 x aantal kilometers + 1,50", []),
                "B": ("ritprijs=1,50 x aantal kilometers + 5,00", []),
                "C": ("ritprijs=5 x 1,50 aantal kilometers", [])
            },
            'correct': 'A'},
        7: {
            'question': "Een fabrikant van flessen cola maakt flessen waarin precies een liter cola past. Een nieuw "
                        "type fles heeft dezelfde vorm als het oude model maar is tweemaal zo groot. Hoeveel liter "
                        "cola past er in dit nieuwe type fles?",
            'answers': {
                "A": ("8 liter", []),
                "B": ("6 liter", []),
                "C": ("4 liter", []),
                "D": ("2 liter", [])
            },
            'correct': 'A'},
        8: {
            'question': "Elma zit in een restaurant. Ze kiest een voorgerecht, een hoofdgerecht en een nagerecht. Er "
                        "staan op de kaart 5 voorgerechten, 8 hoofdgerechten en 10 nagerechten. Hoeveel verschillende "
                        "menu's kan Elma hieruit samenstellen?",
            'answers': {
                "A": ("23", []),
                "B": ("400", []),
                "C": ("280", [])
            },
            'correct': 'A'}
    }
}
