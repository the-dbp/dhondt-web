
class Group:
    name: str
    votes: int = 0
    mandates: int = 0
    parties: list = []
    divisor: int = 0
    increment: float = 0.0

    def __init__(self, name: str, *args, votes: int = 0, mandates: int = 0, parties: list = [], **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.votes = votes if votes else sum([party.votes for party in parties])
        self.mandates = mandates
        self.parties = parties
        self.next_inc()

    def next_inc(self):
        self.divisor += 1
        self.increment = self.votes / self.divisor
        return self.current_inc

    def add_mandate(self):
        self.mandates += 1
        self.next_inc()

    def distribute_mandates(self):
        if not self.parties:
            raise ValueError("No parties in group")
        if not self.mandates:
            raise ValueError("No mandates to distribute")

        self.parties = dhondt(self.parties, self.mandates)

        for i in range(len(self.parties)):
            if self.parties[i].parties:
                self.parties[i].distribute_mandates()

    def __repr__(self) -> str:
        s = f"* {self.name}: {self.mandates}"
        for party in self.parties:
            s += f"\n   - {party.name}: {party.mandates}"
        return s

    @property
    def current_inc(self) -> float:
        return self.votes / self.divisor

    def get_parties(self) -> list:
        parties = []
        if self.parties:
            for party in self.parties:
                parties.extend(party.get_parties())
        else:
            parties.append(self)
        return parties

    def show_figure(self, sort_by_mandates: bool = True):
        from matplotlib import pyplot as plt

        parties = self.get_parties()
        parties.sort(key=lambda x: x.mandates, reverse=True)
        names = [party.name for party in parties]
        values = [party.mandates for party in parties]

        plt.figure()
        plt.bar(names, values)
        plt.title(self.name)
        plt.xlabel("Partier")
        plt.ylabel("Mandater")
        plt.xticks(rotation=90)
        plt.yticks(range(0, max(values) + 1))
        plt.tight_layout()
        plt.show()

def dhondt(groups: list[Group], mandates: int) -> list[Group]:
    for _ in range(mandates):
        group_max = 0
        for i in range(len(groups[1:])):
            if groups[i+1].current_inc > groups[group_max].current_inc:
                group_max = i+1
        groups[group_max].add_mandate()
    return groups
