
def mittelwert(*zahlen):
    return sum(zahlen) / len(zahlen)

def median(*zahlen):
    n = len(zahlen)
    sortiert = sorted(zahlen)
    mitte = n // 2
    if n % 2 == 0:
        return (sortiert[mitte - 1] + sortiert[mitte]) / 2
    else:
        return sortiert[mitte]