from collections import OrderedDict

from preferences import*
from sets import Set

class Rank(Set):
    rankType = dict.fromkeys({
        'SORT MTH',
        'SET ID',
        'TIME',
        'LOOPS',
        'RATING',
        })
    
    def __init__(self, sets):
        super().__init__()
        self.sets = sets
        self.ranks = {}
        self.rankFile = '__ranks__.txt'
        self.setType = sets.setType

        self.menu = {
            'ls': 'list',
            'fl': 'filter',
            'sr': 'sort',
            'del': 'delete',
            'sv': 'save',
            'ex': 'exit',
        }

    def subMenu(self):
        try:
            section = 'RANKS'
            text1 = f'\t{self.R.splitL} {section}'
            text2 = f'section {self.R.splitR}'
            print(f'{text1} {text2}', end = '\n\t')
            [print(f'{key}. {value}', end = ' | ')
             for key, value in self.menu.items()]
            text = 'YOUR REQUEST >>> '
            text = f'{bcolors.HEADER}{text}{bcolors.ENDC}'
            selection = input(text)
            selection = selection.strip().lower()
            if selection == 'ex':
                return self.R.exited(1)
            elif selection in self.menu:
                attr = self.menu[selection]
                getattr(self, attr)()
            else:
                return self.R.failed(1)
        except Exception as e:
            self.R.printException('ranks menu', e)
        return -1

    def addRecord(self, method, set, time, loops):
        try:
            volume = len(self.ranks)
            if volume != 0:
                keys = self.ranks.keys()
                i = int(list(keys)[-1]) + 1
            else:
                i = 1
            length = self.sets.volume()
            rating = length / time
            rankType = {
                'SORT MTH': method,
                'SET ID': set,
                'TIME': time,
                'LOOPS': loops,
                'RATING': rating,
            }
            self.ranks[i] = rankType
            return 1
        except Exception as e:
            self.R.printException('adding record', e)
        return -1

    def read(self):
        try:
            with open(self.rankFile, 'r') as file:
                for line in file:
                    if line == '\n':
                        continue
                    i = line.index(': ')
                    key = line[:i].strip()
                    value = line[i+1:]
                    value = value.strip().split('\t')
                    item = {}
                    for line2 in value:
                        i2 = line2.index(': ')
                        key2 = line2[:i2].strip()
                        value2 = line2[i2+1:].strip()
                        item[key2] = value2
                    self.ranks[key] = item
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('ranks')
        except Exception as e:
            self.R.printException('loading ranks', e)
        return -1

    def save(self):
        try:
            name = 'ranks'
            text1 = f'\t{self.R.warnSplitL} saving'
            text2 = f'{name} {self.R.warnSplitR}'
            print(f'{text1} {text2}')
            with open(self.rankFile, 'w') as file:
                for key, value in self.ranks.items():
                    item = ''
                    for key2, value2 in value.items():
                        item += f'{key2}: {value2}\t'
                    file.write(f'{key}: {item}\n\n')
            sleep(1)
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('ranks')
        except Exception as e:
            self.R.printException('saving ranks', e)
        return -1

    def delete(self):
        try:
            self.R.printRequest('delete')
            text = '\t\tpass record ID: '
            id = input(text).strip().lower()
            try:
                item = self.ranks[id].copy()
                print(item)
                text = f'DELETE from ranks?'
                if self.R.printTakeAction(text) == 'y':
                    del self.ranks[id]
                    text = 'deleted record from ranks'
                    self.R.printActionTaken(text)
                    return 1
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            except KeyError:
                self.R.printIncorrectItem('record ID')
        except Exception as e:
            self.R.printException('deleting record from ranks', e)

    def __printItem(self, id):
        propid = self.ranks[id]['SET ID']
        value = self.ranks[id]
        item = ''
        for key2, value2 in value.items():
            key2Text = f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
            item += f'{key2Text}: {value2}\t'
        props = self.sets.printProps(True, propid)
        keyText = f'{bcolors.OKBLUE}{id}{bcolors.ENDC}'
        print(f'\t\t{keyText}: {item}\t{props}\n')

    def list(self):
        try:
            self.R.printRequest('list')
            for key in self.ranks.keys():
                self.__printItem(key)
            self.R.printActionTaken('finished')
            return 1
        except Exception as e:
            self.R.printException('listing ranks', e)
        return -1

    def sort(self):
        try:
            props = self.sets.returnProps()
            self.R.printRequest('sort by')
            rank = self.rankType
            sortable = [key for key in rank.keys()]
            additional = list(self.setType)
            sortable.extend(additional)
            print(f'\t\t{' | '.join(sortable)}')
            text = '\t\tchoose item to sort by: '
            sortType = input(text).strip().upper()
            if sortType in sortable:
                sortType = sortType.upper()
                value = {}
                for key2, value2 in self.ranks.items():
                    value[key2] = {**value2, **props[value2['SET ID']]}
                if sortType == 'RATING':
                    value = OrderedDict(reversed(sorted(value.items(), 
                            key = lambda v: float(v[1][sortType]))))
                else:
                    try:
                        value = OrderedDict(sorted(value.items(), 
                                key = lambda v: float(v[1][sortType])))
                    except:
                        value = OrderedDict(sorted(value.items(), 
                                key = lambda v: v[1][sortType]))
                for i, (k, v) in enumerate(value.items()):
                    kText = f'{bcolors.OKBLUE}{sortType}{bcolors.ENDC}'
                    additionalText = f'{kText}: {v[sortType]}\t'
                    for key, value in v.items():
                        if key != sortType:
                            keyText = f'{bcolors.OKBLUE}{key}{bcolors.ENDC}'
                            additionalText += f'{keyText}: {value}\t'
                    print(f'\t\t{i + 1}. {k}: \t{additionalText}\n')
                self.R.printActionTaken('finished')
                return 1
            else:
                self.R.printIncorrectItem('item')
        except Exception as e:
            self.R.printException('sorting ranks', e)
        return -1

    def filter(self):
        try:
            self.R.printRequest('filter by id')
            text = '\t\tpass rank ID: '
            key = input(text).strip().lower()
            try:
                self.__printItem(key)
                self.R.printActionTaken('finished')
                return 1
            except KeyError:
                self.R.printIncorrectItem('rank ID')
        except Exception as e:
            self.R.printException('filtering ranks', e)
        return -1

    def volume(self):
        return len(self.ranks)