import pandas as pd

class Database:
    def __init__(self, path: str = '') -> None:
        self._path: str = path
        self._db: pd.DataFrame = pd.DataFrame()
        try:
            self._db = pd.read_csv(self._path)
        except:
            raise FileNotFoundError
    

    def __str__(self) -> str:
        return self._db.to_string(index = False)


    def __getitem__(self, index: int) -> pd.Series:
        if index < 0 or index > len(self._db) - 1:
            raise IndexError
        return self._db.iloc[index]


    def __len__(self):
        return len(self._db)


    def get_column(self, column: str) -> list:
        try:
            return list(self._db[column])
        except:
            return []


    def load_csv(self, path: str) -> None:
        self.__init__(path)


    def save_csv(self, path: str = '') -> None:
        if len(path) == 0:
            path = self._path
        self._db.to_csv(path, index = False)
    

    def find(self, column: str, prompt) -> int:
        item: pd.DataFrame = self._db[self._db[column] == prompt]
        if len(item):
            return int(item.iloc[0].name)
        return -1


    def change(self, index: int, row: list) -> None:
        if index < 0 or index > len(self._db) - 1:
            raise IndexError
        self._db.loc[index] = row


    def add(self, row: list, back: bool = True) -> None:
        index: int = -1
        if back:
            index = len(self._db)        
        self._db.loc[index] = row
        self._db = self._db.sort_index().reset_index(drop = True)
    

    def remove(self, index: int) -> None:
        if index < 0 or index > len(self._db) - 1:
            raise IndexError
        self._db = self._db.drop(index)