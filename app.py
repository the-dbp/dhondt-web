from flask import Flask, request, jsonify, render_template
from dhondt import Group

TOTAL_VOTES = 2447749
def get_valg():
    return Group(name="Eksempel Valg", mandates=15, parties=[
        Group(name="EEP", parties=[
            Group(name="Liberal Alliance", votes=TOTAL_VOTES * 0.070),
            Group(name="Konservative", votes=TOTAL_VOTES * 0.088),
        ]),
        Group(name="Grønne og S&D", parties=[
            Group(name="Socialdemokratiet", votes=TOTAL_VOTES * 0.156),
            Group(name="SF", votes=TOTAL_VOTES * 0.174),
            Group(name="Alternativet", votes=TOTAL_VOTES * 0.027),
        ]),
        Group(name="Liberale", parties=[
            Group(name="Moderaterne", votes=TOTAL_VOTES * 0.059),
            Group(name="Radikale Venstre", votes=TOTAL_VOTES * 0.071),
            Group(name="Venstre", votes=TOTAL_VOTES * 0.147),
        ]),
        Group(name="Dansk Folkeparti", votes=TOTAL_VOTES * 0.064),
        Group(name="Danmarksdemokraterne", votes=TOTAL_VOTES * 0.074),
        Group(name="Enhedslisten", votes=TOTAL_VOTES * 0.070),
    ])

def flatten_parties(group: Group):
    if hasattr(group, 'parties') and group.parties:
        # Recursively get all subgroups
        flattened = []
        for sub in group.parties:
            flattened.extend(flatten_parties(sub))
        return flattened
    else:
        # Leaf node (actual party)
        return [group]
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    print(data)
    total_votes = data["total_votes"]
    mandates = data["mandates"]
    groups_input = data["groups"]
    print("total votes", total_votes)
    print("mandates", mandates)
    print("groups input", groups_input)


    valg = Group(name="Valg", mandates=mandates, parties=[])
    for group in groups_input:
        parties = []
        for party in group["parties"]:
            parties.append(Group(name=party["name"], votes=total_votes * party["percentage"]/100))
        if "percentage" in group:
            valg.parties.append(Group(name=group["name"], votes=total_votes * group["percentage"]/100))
        else:
            valg.parties.append(Group(name=group["name"], parties=parties))
    print("valg____________________")
    print(valg)
    valg.distribute_mandates()

    # Flatten the party results
    flat_parties = flatten_parties(valg)
    results = [{
        "name": p.name,
        "votes": getattr(p, "votes", 0),
        "mandates": p.mandates,
    } for p in flat_parties]
    results.sort(key=lambda x: (-x["mandates"], -x["votes"]))
    print(results)
    return jsonify(results)



@app.route("/result")
def results():
    valg   = get_valg()
    print("valg____________________")
    print(valg)
    valg.distribute_mandates()

    flat_parties = flatten_parties(valg)
    results = [{
        "name": p.name,
        "votes": getattr(p, "votes", 0),
        "mandates": p.mandates,
    } for p in flat_parties]
    results.sort(key=lambda x: (-x["mandates"], -x["votes"]))
    return render_template("result.html", results=results)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')