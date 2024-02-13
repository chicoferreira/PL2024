import fileinput


class EMD:
    # _id,index,dataEMD,nome/primeiro,nome/último,idade,género,morada,modalidade,clube,email,federado,resultado
    def __init__(self,
                 _id: str,
                 index: int,
                 data_emd: str,
                 primeiro_nome: str,
                 ultimo_nome: str,
                 idade: int,
                 genero: str,
                 morada: str,
                 modalidade: str,
                 clube: str,
                 email: str,
                 federado: bool,
                 resultado: bool):
        self._id = _id
        self.index = index
        self.data_emd = data_emd
        self.primeiro_nome = primeiro_nome
        self.ultimo_nome = ultimo_nome
        self.idade = idade
        self.genero = genero
        self.morada = morada
        self.modalidade = modalidade
        self.clube = clube
        self.email = email
        self.federado = federado
        self.resultado = resultado


def parse_emd_from_array(arr: list[str]) -> EMD:
    return EMD(arr[0],
               int(arr[1]),
               arr[2],
               arr[3],
               arr[4],
               int(arr[5]),
               arr[6],
               arr[7],
               arr[8],
               arr[9],
               arr[10],
               arr[11] == 'true',
               arr[12] == 'true')


def read_csv_emd(file) -> list[EMD]:
    emd = []
    file.readline()  # skip header
    for line in file:
        emd.append(parse_emd_from_array(line.strip().split(',')))
    return emd


def list_modalidades_ordered_alphabetically(emd: list[EMD]) -> list[str]:
    return sorted(set([e.modalidade for e in emd]))


def percentage_apt_and_inapt(emd: list[EMD]) -> tuple[float, float]:
    total = float(len(emd))
    apt = (sum([1 for e in emd if e.resultado]))
    inapt = total - apt
    return apt / total, inapt / total


def percentual_distribution_by_age(emd: list[EMD], interval=5) -> list[tuple[int, int], float]:
    ages = [e.idade for e in emd]
    min_age = min(ages)
    max_age = max(ages)

    start = min_age - (min_age % interval)
    end = max_age + (interval - (max_age % interval))

    intervals = [(i, i + interval - 1) for i in range(start, end, interval)]

    age_count = [0] * len(intervals)
    for age in ages:
        for i, (min_a, max_a) in enumerate(intervals):
            if min_a <= age <= max_a:
                age_count[i] += 1

    # noinspection PyTypeChecker
    return list(zip(intervals, age_count))


def main():
    emd = read_csv_emd(fileinput.input())

    print("Modalidades: ", list_modalidades_ordered_alphabetically(emd))
    print("Percentagem (aptos, inaptos): ", percentage_apt_and_inapt(emd))
    print("Distribuição de idades: ", percentual_distribution_by_age(emd))


if __name__ == '__main__':
    main()
