import sys
import re

tab = []
file = "learning.txt"


def savetofile(dataset):
    with open("learned_"+file, "w+") as save_to:
        for line in dataset:
            string = ''
            for num, value in enumerate(line):
                if num == len(dataset[0])-1:
                    string += "{}\n".format(value)
                else:
                    string += "{};".format(value)
            save_to.write(string)


def savenewvalues(testvalues, result_dict):
    with open("learned_"+file, "a") as save_to:
        string = ''
        for value in testvalues:
            string += "{};".format(value)
        string += result_dict+"\n"
        save_to.write(string)


def open_exist(file):
    with open("learned_"+file, "r") as f:
        lines = f.readlines()
        for line in lines:
            inside = []
            line = line.replace('\n', '')
            line = line.split(";")
            for value in line:
                try:
                    value = value.replace(',', '.')
                    inside.append(float(value))
                except Exception as e:
                    inside.append(value)
            tab.append(inside)
        return tab


def file_open(filename):
    length = 0
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            for num, line in enumerate(lines):
                line = re.sub('[^A-Za-z0-9.|;,-]+', '', line)
                line = line.replace('|', ';')
                line = line.split(";")
                inside = []
                if len(line) != length and tab:
                    pass
                else:
                    for value in line:
                        try:
                            value = value.replace(',', '.')
                            inside.append(float(value))
                        except Exception as e:
                            inside.append(value)
                    if not tab:
                        length = len(inside)
                    if inside not in tab:
                        tab.append(inside)
            savetofile(tab)
            return tab
    except Exception:
        print("Nie znaleziono pliku")
        sys.exit(0)


def proposal_values(dataset):
    tab = []
    for i in range(len(dataset[0])):
        unique = []
        for num, line in enumerate(dataset):
            if dataset[num][i] not in unique:
                unique.append(dataset[num][i])
        unique.sort()
        tab.append(unique)
    print('\nWystępujące wartości:')
    for i in range(len(dataset[0])):
        if i == len(dataset[0])-1:
            print("decyzja\t\t", tab[i], '\n')
        else:
            print("wartości {}\t".format(i+1), tab[i])
    return tab[len(dataset[0])-1]


def get_test_values(dataset):
    testvalues = []
    i = 0
    while i < len(dataset[0])-1:
        try:
            if isinstance(tab[i][0], float):
                val = float(input("Podaj wartość {}:   ".format(i + 1)))
                testvalues.append(val)
            elif isinstance(tab[i][0], str):
                val = input("Podaj wartość {}:   ".format(i + 1))
                testvalues.append(val)
            i += 1
        except ValueError:
            print('Wprowadzono wartość nie pasuącą do wartości wewnątrz kolumny wartości')
    return testvalues


def decision_ratio(dataset, decisions):
    ratio_dict = {}
    for decision in decisions:
        count = 0
        for values in dataset:
            if values[len(dataset[0])-1] == decision:
                count += 1
        ratio_dict[decision] = count/len(dataset)
    return ratio_dict


def classifier(dataset, testvalues, decisions):
    result = {}
    for decision in decisions:
        main_decisions = 1
        for numa, vala in enumerate(testvalues):
            count_decisions = 0
            count_values = 0
            for numb, valb in enumerate(dataset):
                if dataset[numb][len(dataset[0])-1] == decision:
                    count_decisions += 1
                    if vala == valb[numa]:
                        count_values += 1
            try:
                main_decisions *= count_values / count_decisions
            except ZeroDivisionError:
                main_decisions = 0
        try:
            result[decision] = main_decisions
        except ZeroDivisionError:
            result[decision] = 0
    return result


def comparedicts(testvalues, decision_dict, probability_dict, dataset):
    result_dict = ''
    max = 0
    for key, value in decision_dict.items():
        result = value * probability_dict[key]
        if result > max:
            result_dict = key
            max = result
    if max > 0:
        # savenewvalues(testvalues, result_dict)
        return "decyzja = {} o wartości {}".format(result_dict, max)
    return "nie znaleziono odpowiedniej decyzji"


def naive_bayes_classifier_main(dataset, testvalues, decisions):
    decision_dict = decision_ratio(dataset, decisions)
    probability_dict = classifier(dataset, testvalues, decisions)
    print("\nDla wartości ", testvalues, comparedicts(testvalues, decision_dict, probability_dict, dataset))


if __name__ == '__main__':
    while True:
        try:
            dataset = open_exist(file)
        except:
            dataset = file_open(file)
        decisions = proposal_values(dataset)
        test_values = get_test_values(dataset)
        naive_bayes_classifier_main(dataset, test_values, decisions)

