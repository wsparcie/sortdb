import os
from glob import iglob

from preferences import*
from sets import Set
from ranks import Rank
from sorts import Sort

from datetime import datetime

class Database:
    dirType = (
        '__ranks__.txt',
    )
    
    def __init__(self):
        self.R = React()
        self.sets = Set()
        self.ranks = Rank(self.sets)
        self.sort = Sort(self.sets, self.ranks)

        self.menuType = {
            'sr': 'sort',
            'rk': 'ranks',
            'st': 'sets',
            'sv': 'save',
            'ex': 'exit',
            'clear': 'clear',
        }

        self.menuNonUsable = (
            'sr',
            'sv',
            'ex',
            'clear',
        )

        ifIntegral = self.__checkFiles()
        if ifIntegral in (0, 1):
            text = f'reading database'
            print(f"{self.R.warnSplitL} {text} {self.R.warnSplitR}")
            self.ranks.read()
            self.sets.read()
        else:
            text = f'generating database'
            print(f"{self.R.warnSplitL} {text} {self.R.warnSplitR}")
            self.sets.generate()
            self.sets.save()

    def __checkFiles(self):
        try:
            print(f"{self.R.warnSplitL} {'checking files'} {self.R.warnSplitR}")
            directory = [file for file in iglob("*.txt")]
            files = set([*self.dirType, *directory])
            if len(files) == len(directory):
                isComplete = 0
            elif len(files) < len(directory):
                isComplete = 1
            else:
                isComplete = -1
            if len(directory) != 0 and isComplete == -1:
                self.R.printIncorrectItem('missing files')
            return isComplete
        except Exception as e:
            self.R.printException('checking files', e)
            return 0

    def __saveData(self, selection):
        try:
            if selection == 'all':
                for key, value in self.menuType.items():
                    if key not in self.menuNonUsable:
                        getattr(self, value).save()
        except Exception as e:
            self.R.printException('saving database', e)
        return -1

    def __exSelect(self):
        text = 'SAVE data? [y/n]: '
        text = f'{bcolors.WARNING}{text}{bcolors.ENDC}'
        ifSave = input(text).strip().lower()
        if ifSave == 'y':
            self.__saveData('all')

    def info(self):
        print(f"{self.R.header}")
        text = 'Welcome back'
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tabs = ' '*(len(self.R.header)//10)
        data = f'{text}{tabs}{time}'
        welcome = f'{bcolors.OKGREEN}{data}{bcolors.ENDC}'
        print(welcome, end = '\n\n')
        text = 'STATS:'
        print(f'{bcolors.BOLD}{text}{bcolors.ENDC}', end = '\t')
        status = ' | '.join(f'{self.__dataVolume(key)} {value}'
                            for key, value in self.menuType.items() 
                            if key not in self.menuNonUsable)
        print(status, end = '\n\n')

    def __home(self):
        print(f'{self.R.splitL} PLEASE SELECT {self.R.splitR}')
        [print(f'{key}. {value}', end = ' | ') 
         for key, value in self.menuType.items()]
        text = 'YOUR SELECTION >>> '
        selection = input(f'{bcolors.HEADER}{text}{bcolors.ENDC}')
        selection = selection.strip().lower()
        if selection == 'sv':
            self.__saveData('all')
            return 0
        elif selection == 'ex':
            self.__exSelect()
            return self.R.exited(0)
        elif selection == 'clear':
            os.system('cls||clear')
            self.info()
            return 0
        elif selection in self.menuType:
            attr = self.menuType[selection]
            self.homeSel = getattr(self, attr)
        else:
            return self.R.failed(0)
        return selection

    def menu(self):
        try:
            self.info()
            while True:
                status = self.__home()
                if status == 1:
                    break
                elif status != 0:
                    while True:
                        attr = self.menuType[status]
                        s = getattr(self, attr).subMenu()
                        if s == 1:
                            break
        except Exception as e:
            self.R.printException('main menu', e)
        return -1

    def __dataVolume(self, name):
        if name not in self.menuNonUsable:
            attr = self.menuType[name]
            return getattr(self, attr).volume()