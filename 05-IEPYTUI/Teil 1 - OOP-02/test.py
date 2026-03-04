class Tier:
    def ausgabe(self):
        print("Ich bin ein Tier!")


class Baer(Tier):
    def ausgabe(self):
        print("Ich bin ein Bär!")


class Hund(Tier):
    def ausgabe(self):
        print("Ich bin ein Hund!")


def ausgabe_tier(tierart):
    tierart.ausgabe()


anrei = Hund()
balu = Baer()

ausgabe_tier(anrei)
ausgabe_tier(balu)
