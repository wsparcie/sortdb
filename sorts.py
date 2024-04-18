import time

from preferences import*
from ranks import Rank

class Sort(Rank):
    def __init__(self, sets, ranks):
        super().__init__(sets)
        self.sets = sets
        self.ranks = ranks

        self.menu = {
            'all': 'choose all methods',
            'mrg': 'mergesort',
            'qck': 'quicksort',
            'bck': 'bucketsort',
            'bbl': 'bubblesort',
            'ins': 'insertsort',
            'sel': 'selectsort',
            'ex': 'exit',
        }

        self.menuNonUsable = (
            'all',
            'ex',
        )

    def __countTime(self, methodSelection, setSelection):
        try:
            self.array = self.sets.giveSet(setSelection)
            t0 = time.perf_counter()
            loops = getattr(self, methodSelection)()
            record = time.perf_counter() - t0
            if record < 1:
                milliSec = record * 1000
                sec = '\t\t'
            else:
                milliSec = '\t\t'
                sec = record
            self.ranks.addRecord(methodSelection, setSelection, record, loops)
            methodText = f'{bcolors.OKBLUE}{methodSelection}{bcolors.ENDC}'
            setText = f'{bcolors.OKCYAN}{setSelection}{' '*(20 - len(str(setSelection)))}{bcolors.ENDC}'
            loopsText = f'{loops}{' '*(10 - len(str(loops)))}'
            recordMilliSecText = f'{bcolors.OKGREEN}{milliSec}{bcolors.ENDC}'
            recordSecText = f'{bcolors.FAIL}{sec}{bcolors.ENDC}'
            propsText = self.sets.printProps(True, setSelection)
            text1 = f'{methodText}\t|{setText}  \t|{loopsText}\t|'
            text2 = f'{recordMilliSecText}\t|{recordSecText}\t|{propsText}'
            text = f'{text1}{text2}'
            print(text)
        except Exception as e:
            text1 = f'counting time using {methodSelection} '
            text2 = f'method and {setSelection} set'
            self.R.printException(f'{text1}{text2}', e)
        return -1

    def __selectMethod(self, methodSelection, setSelection):
        try:
            if methodSelection == 'all':
                for key, value in self.menu.items():
                    if key not in self.menuNonUsable:
                        self.__countTime(value, setSelection)
            else:
                methodSelection = self.menu[methodSelection]
                self.__countTime(methodSelection, setSelection)
        except Exception as e:
            self.R.printException('selecting method', e)
        return -1

    def __selectSet(self, methodSelection, setSelection):
        try:
            methodText = f'{bcolors.OKBLUE}algorithm{bcolors.ENDC}'
            setText = f'{bcolors.OKCYAN}name{bcolors.ENDC}'
            loopsText = f'loops'
            recordSecsText = f'{bcolors.FAIL}time [seconds]{bcolors.ENDC}'
            recordMilliSecsText = f'{bcolors.OKGREEN}time [milliseconds]{bcolors.ENDC}'
            setPropsText = f'{bcolors.OKCYAN}properties{bcolors.ENDC}'
            text1 = f'{methodText}\t|{setText}\t\t\t|{loopsText}\t\t|{recordMilliSecsText}\t|'
            text2 = f'{recordSecsText}\t\t|{setPropsText}\t\t'
            text = f'{text1}{text2}'
            line = f'{(len(text) + 50) * '-'}'
            print(text)
            print(line)
            if setSelection == 'all':
                for value in self.sets.giveList():
                    self.__selectMethod(methodSelection, value)
            else:
                self.__selectMethod(methodSelection, setSelection)
            self.R.printActionTaken('finished')
            sleep(1)
        except Exception as e:
            self.R.printException('selecting set', e)
        return -1

    def subMenu(self):
        try:
            section = 'SORT'
            text1 = f'\t{self.R.splitL} {section}'
            text2 = f'section {self.R.splitR}'
            print(f'{text1} {text2}', end = '\n\t')
            [print(f'{key}. {value}', end = ' | ') 
             for key, value in self.menu.items()]
            text = 'CHOOSE METHOD >>> '
            text = f'{bcolors.HEADER}{text}{bcolors.ENDC}'
            methodSelection = input(text)
            methodSelection = methodSelection.strip().lower()
            if methodSelection == 'ex':
                return self.R.exited(1)
            elif methodSelection not in self.menu:
                return self.R.failed(1)
            self.sets.list()
            print(f'\t\tall. choose all sets')
            sleep(1)
            text = 'CHOOSE SET >>> '
            text = f'\t\t{bcolors.HEADER}{text}{bcolors.ENDC}'
            setSelection = input(text)
            setSelection = setSelection.strip().lower()
            condition1 = setSelection != 'all'
            condition2 = setSelection not in self.sets.giveList()
            if condition1 and condition2:
                return self.R.failed(1)
            else:
                self.__selectSet(methodSelection, setSelection)
        except Exception as e:
            self.R.printException('sort menu', e)
        return -1


    def __merge(self, leftIndex, pivot, rightIndex, arraySub):
        ifLoop = True
        for i in range(leftIndex, rightIndex + 1):
            arraySub[i] = self.array[i]
            self.loops += 1 if not ifLoop else 0
            ifLoop = False
        leftSideIndex, rightSideIndex = leftIndex, pivot + 1
        index = leftIndex
        while leftSideIndex <= pivot and rightSideIndex <= rightIndex:
            if arraySub[leftSideIndex] >= arraySub[rightSideIndex]:
                self.array[index] = arraySub[leftSideIndex]
                leftSideIndex += 1
            else:
                self.array[index] = arraySub[rightSideIndex]
                rightSideIndex += 1
            index += 1
            self.loops += 1 if not ifLoop else 0
            ifLoop = False
        while leftSideIndex <= pivot:
            self.array[index] = arraySub[leftSideIndex]
            index += 1
            leftSideIndex += 1
            self.loops += 1 if not ifLoop else 0
            ifLoop = False
        self.loops += 1 if ifLoop else 0

    def __mergeSub(self, leftIndex, rightIndex, arraySub):
        if leftIndex != rightIndex:
            pivot = (leftIndex + rightIndex) // 2
            self.__mergeSub(leftIndex, pivot, arraySub)
            self.__mergeSub(pivot + 1, rightIndex, arraySub)
            self.__merge(leftIndex, pivot, rightIndex, arraySub)

    def mergesort(self):
        self.loops = 0
        length = len(self.array)
        if length == 0:
            return None
        self.__mergeSub(0, length - 1, [0] * length)
        return self.loops


    def __pivot(self, leftIndex, rightIndex):
        pivotIndex = rightIndex
        border = leftIndex
        for i in range(leftIndex, rightIndex + 1):
            if self.array[i] > self.array[pivotIndex]:
                self.array[i], self.array[border] = self.array[border], self.array[i]
                border += 1
            self.loops += 1
        self.array[border], self.array[pivotIndex] = self.array[pivotIndex], self.array[border]
        return border

    def __quickSub(self, leftIndex, rightIndex):
        if leftIndex < rightIndex:
            pivotIndex = self.__pivot(leftIndex, rightIndex)
            self.__quickSub(leftIndex, pivotIndex - 1)
            self.__quickSub(pivotIndex + 1, rightIndex)
        return self.loops

    def quicksort(self):
        self.loops = 0
        self.__quickSub(0, len(self.array) - 1)
        return self.loops


    def __maxValue(self):
        maxVal = self.array[0]
        for i in self.array:
            if i > maxVal:
                maxVal = i
            self.loops += 1
        return maxVal

    def bucketsort(self):
        self.loops = 0
        maxRecord = self.__maxValue()
        buckets = [0] * (maxRecord + 1)
        for element in self.array:
            buckets[element] += 1
            self.loops += 1
        index = 0
        for i in range(maxRecord + 1):
            ifLoop = True
            if buckets[i] > 0:
                for _ in range(buckets[i]):
                    self.array[index] = i
                    index += 1
                    self.loops += 1 if not ifLoop else 0
                    ifLoop = False
            self.loops += 1 if ifLoop else 0
        return self.loops


    def bubblesort(self):
        loops = 0
        for i in range(len(self.array)):
            for j in range(len(self.array) - 1):
                if self.array[j] < self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                loops += 1
        return loops


    def insertsort(self):
        loops = 0
        for i in range(1, len(self.array)):
            ifLoop = True
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
                loops += 1 if not ifLoop else 0
                ifLoop = False
            self.array[j + 1] = key
            loops += 1 if ifLoop else 0
        return loops
        


    def selectsort(self):
        loops = 0
        for i in range(len(self.array) - 1):
            record = i
            for j in range(i + 1, len(self.array)):
                if self.array[record] > self.array[j]:
                    record = j
                loops += 1
            self.array[record], self.array[i] = self.array[i], self.array[record]
        return loops