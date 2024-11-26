from matplotlib import pyplot as plt
from collections import OrderedDict
from glob import iglob
from statistics import mean
from random import randint

from preferences import*
from generator import SetGen

class Set(SetGen):
    setType = dict.fromkeys({
        'MTH',
        'LEN',
        'AVG',
        'MIN',
        'MAX',
        })

    def __init__(self):
        self.R = React()
        super().__init__()
        self.gen = SetGen()
        self.sets = {}
        self.props = {}
        
        self.menu = {
            'rd': 'read',
            'ls': 'list',
            'fl': 'filter',
            'sr': 'sort',
            'add': 'add',
            'del': 'delete',
            'sv': 'save',
            'ex': 'exit',
        }

        self.excluded = (
            '__ranks__.txt',
            'requirements.txt',
        )

    def subMenu(self):
        try:
            section = 'SETS'
            print(f'\t{self.R.splitL} {section} section {self.R.splitR}', end = '\n\t')
            [print(f'{key}. {value}', end = ' | ')
             for key, value in self.menu.items()]
            text = 'YOUR REQUEST >>> '
            selection = input(f'{bcolors.HEADER}{text}{bcolors.ENDC}')
            selection = selection.strip().lower()
            if selection == 'ex':
                return self.R.exited(1)
            elif selection in self.menu:
                attr = self.menu[selection]
                getattr(self, attr)()
            else:
                return self.R.failed(1)
        except Exception as e:
            self.R.printException('sets menu', e)
        return -1

    def giveSet(self, id):
        return self.sets[id]

    def giveList(self):
        return list(self.sets.keys())

    def __checkFiles(self):
        try:
            print(f"{self.R.warnSplitL} {'reading sets'} {self.R.warnSplitR}")
            self.directory = [file for file in iglob('*.txt') 
                              if file not in self.excluded]
        except Exception as e:
            self.R.printException('checking files', e)
            return 0

    def __giveProps(self, source, id):
        try:
            source = self.sets if source else self.setsTemp
            item = source[id]
            if '_' in id:
                i = id.index('_')
                id = id[:i]
            method = id if id in self.gen.menu.values() else 'unknown'
            self.setType = {
                'MTH': method,
                'LEN': len(item),
                'AVG': mean(item),
                'MIN': min(item),
                'MAX': max(item),
            }
            return self.setType
        except Exception as e:
            self.R.printException('calculating sets properties', e)

    def returnProps(self):
        return self.props

    def printProps(self, source, id):
        item = ''
        source = self.props if source else self.propsTemp
        for key, value in source[id].items():
            keyText = f'{bcolors.OKCYAN}{key}{bcolors.ENDC}'
            item += f'{keyText}: {value}{" " * (15 - len(str(value)))}'
        return item[:-2]

    def read(self):
        try:
            self.__checkFiles()
            for file in self.directory:
                with open(f'{file}', 'r') as f:
                    i = 0
                    array = []
                    for line in f:
                        try:
                            array.append(int(line.strip()))
                            i += 1
                        except Exception as e:
                            text = f'reading {file} {i + 1} line'
                            self.R.printException(text, e)
                id = file[:-4].lower()
                self.sets[id] = array
                self.props[id] = self.__giveProps(True, id)
        except Exception as e:
            self.R.printException('reading sets', e)
        return -1

    def save(self):
        try:
            name = 'sets'
            print(f'\t{self.R.warnSplitL} saving {name} {self.R.warnSplitR}')
            for key, value in self.sets.items():
                with open(f'{key}.txt', 'w') as file:
                    [file.write(f'{i}\n') for i in value]
            sleep(1)
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('sets')
        except Exception as e:
            self.R.printException('saving sets', e)
        return -1

    @staticmethod
    def __checkInit(start, stop, quantity):
        if start > stop or quantity <= 0:
            print('incorrect data')
            return -1

    def __findTypes(self, method):
        try:
            def findIndex(value):
                if '_' in value:
                    i = value.index('_')
                    return value[:i]
                else:
                    return value
            typeLen = list(filter(lambda i: findIndex(i) == method, 
                                  self.sets))
            numbers = []
            for item in typeLen:
                i = item.index('_')
                val = item[i+1:]
                numbers.append(int(val))
            if len(numbers) != 0:
                i = max(numbers) + 1
            else:
                i = 1
            return i
        except Exception as e:
            self.R.printException('finding types', e)
        return -1

    def __addTempRecord(self, value, args):
        i = self.__findTypes(value)
        id = f'{value}_{i}'
        getattr(self.gen, value)(*args)
        self.setsTemp[id] = self.gen.array
        self.propsTemp[id] = self.__giveProps(False, id)
        print(f'\t\t\t{id} generated', end = '\t\t')
        print(self.printProps(False, id))

    def __genSet(self, method, args):
        try:
            self.setsTemp = {}
            self.propsTemp = {}
            if method == 'all':
                for key, value in self.gen.menu.items():
                    if key not in self.gen.menuNonUsable:
                        self.__addTempRecord(value, args)
            else:
                value = self.gen.menu[method]
                self.__addTempRecord(value, args)
                plt.hist(self.setsTemp[id], bins = 200)
                plt.show()
        except Exception as e:
            self.R.printException('generating set(s)', e)
        return -1

    def __genParams(self, method):
        try:
            if method == 'man':
                args = (None, None, None)
            else:
                section = 'MODE SELECTION'
                print(f'\t\t\t{self.R.splitL} {section} {self.R.splitR}', end = '\n\t\t\t')
                [print(f'{key}. {value}', end = ' | ') 
                 for key, value in self.gen.modesMenu.items()]
                text = 'CHOOSE MODE >>> '
                mode = input(f'{bcolors.HEADER}{text}{bcolors.ENDC}')
                mode = mode.strip().lower()
                if mode not in self.gen.modesMenu:
                    self.R.printIncorrectItem('mode')
                elif mode == 'a':
                    quantity = randint(0, 10000)
                    start = randint(0, 10000)
                    stop = randint(start, 10000)
                    args = (start, stop, quantity)
                    self.__checkInit(*args)
                else:
                    text = '\t\t\tpass number of elements: '
                    quantity = int(input(text))
                    text = '\t\t\tpass range (minimal value): '
                    start = int(input(text))
                    text = '\t\t\tpass range (maximal value): '
                    stop = int(input(text))
                    args = (start, stop, quantity)
                    self.__checkInit(*args)
            self.__genSet(method, args)
        except Exception as e:
            self.R.printException('generating set(s) parameters', e)
        return -1

    def __addMenu(self):
        try:
            section = 'SET GENERATION'
            print(f'\t\t{self.R.splitL} {section} {self.R.splitR}', end = '\n\t\t')
            [print(f'{key}. {value}', end = ' | ')
             for key, value in self.gen.menu.items()]
            text = 'CHOOSE METHOD >>> '
            method = input(f'{bcolors.HEADER}{text}{bcolors.ENDC}')
            method = method.strip().lower()
            if method == 'ex':
                return self.R.exited(0)
            elif method in self.gen.menu:
                self.__genParams(method)
            else:
                self.R.printIncorrectItem('method')
        except Exception as e:
            self.R.printException('set(s) generator submenu', e)

    def add(self):
        try:
            self.gen = SetGen()
            self.__addMenu()
            text = '\tADD to sets?'
            if self.R.printTakeAction(text) == 'y':
                self.sets.update(**self.setsTemp)
                self.props.update(**self.propsTemp)
                self.R.printActionTaken('added')
                return 1
            else:
                self.R.printActionTaken('cancelled')
                return 0
        except Exception as e:
            self.R.printException('adding set', e)
        return -1

    def delete(self):
        try:
            self.R.printRequest('delete')
            text = '\t\tpass set name: '
            id = input(text).strip().lower()
            if id in self.sets:
                text = f'DELETE from sets?'
                if self.R.printTakeAction(text) == 'y':
                    del self.sets[id]
                    text = 'deleted set from sets'
                    self.R.printActionTaken(text)
                    text = '\t\tplease delete file from folder'.upper()
                    print(text)
                    return 1
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            else:
                self.R.printIncorrectItem('file name')
        except Exception as e:
            self.R.printException('deleting set from sets', e)
        return -1

    def list(self):
        try:
            self.R.printRequest('list')
            for key in self.sets:
                props = self.printProps(True, key)
                text = f'\t\t{key}:\t{props}'
                print(text)
            self.R.printActionTaken('finished')
            return 1
        except Exception as e:
            self.R.printException('listing sets', e)
        return -1

    def sort(self):
        try:
            self.R.printRequest('sort by')
            sortable = [key for key in self.setType.keys() 
                        if not isinstance(self.setType[key], dict)]
            print(f'\t\t{" | ".join(sortable)}')
            text = '\t\tchoose item to sort by: '
            sortType = input(text).strip().upper()
            if sortType in sortable:
                sortType = sortType.upper()
                value = {}
                for key2, value2 in self.props.items():
                    value[key2] = value2
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
            self.R.printException('sorting sets', e)
        return -1

    def __showItem(self, id):
        value = self.props[id]
        item = ''
        for key2, value2 in value.items():
                key2Text = f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
                item += f'{key2Text}: {value2}\t'
        keyText = f'{bcolors.OKBLUE}{item}{bcolors.ENDC}'
        elems = self.sets[id]
        print(f'\t\t{keyText}\t{elems}')
        array = self.sets[id]
        plt.hist(array, bins = 200)
        plt.show()

    def filter(self):
        try:
            self.R.printRequest('filter by ID')
            text = '\t\tpass file name: '
            id = input(text).strip().lower()
            if id in self.sets:
                self.__showItem(id)
                self.R.printActionTaken('finished')
                return 1
            else:
                self.R.printIncorrectItem('set name')
        except Exception as e:
            self.R.printException('filtering sets', e)
        return -1

    def volume(self):
        return len(self.sets)

    def generate(self):
        try:
            args = (10, 100, 1000)
            for arg in args:
                quantity = arg
                start = 0
                stop = arg
                args = (start, stop, quantity)
                self.__genSet('all', args)
                self.sets.update(**self.setsTemp)
                self.props.update(**self.propsTemp)
            return 1
        except Exception as e:
            self.R.printException('generating sets', e)
        return -1