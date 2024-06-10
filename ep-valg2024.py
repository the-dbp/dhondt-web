from dhondt import Group

TOTAL_VOTES = 2_447_749

ep_valg = Group(name="EP Valg", mandates=15, parties=[
    Group(name="EEP", parties=[
        Group(name="Liberal Alliance", votes=TOTAL_VOTES*0.070),
        Group(name="Konservative", votes=TOTAL_VOTES*0.088),
    ]),
    Group(name="Grønne og S&D", parties=[
        Group(name="Socialdemokratiet", votes=TOTAL_VOTES*0.156),
        Group(name="SF", votes=TOTAL_VOTES*0.174),
        Group(name="Alternativet", votes=TOTAL_VOTES*0.027),
    ]),
    Group(name="Liberale", parties=[
        Group(name="Moderaterne", votes=TOTAL_VOTES*0.059),
        Group(name="Radikale Venstre", votes=TOTAL_VOTES*0.071),
        Group(name="Venstre", votes=TOTAL_VOTES*0.147),
    ]),
    Group(name="Dansk Folkeparti", votes=TOTAL_VOTES*0.064),
    Group(name="Danmarksdemokraterne", votes=TOTAL_VOTES*0.074),
    Group(name="Enhedslisten", votes=TOTAL_VOTES*0.070),
])

ep_valg.distribute_mandates()

for group in ep_valg.parties:
    print(group)

ep_valg.show_figure(sort_by_mandates=True)