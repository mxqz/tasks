import pandas as pd

class Database:
    """
    A simple class for working with a CSV-based database using pandas.
    Allows loading, saving, searching, and modifying data efficiently.
    """
    
    def __init__(self, path: str = '') -> None:
        """
        Initializes the database by loading data from a CSV file.
        If the file is not found, an exception is raised.
        
        Args:
            path (str): Path to the CSV file.
        """
        self._path: str = path
        self._db: pd.DataFrame = pd.DataFrame()
        try:
            self._db = pd.read_csv(self._path)
        except:
            raise FileNotFoundError
    
    def __str__(self) -> str:
        """
        Returns a string representation of the database (CSV content as a table).
        """
        return self._db.to_string(index = False)

    def __getitem__(self, index: int) -> pd.Series:
        """
        Returns a specific row from the database by index.
        
        Args:
            index (int): Row index.
        
        Returns:
            pd.Series: The selected row.
        
        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index > len(self._db) - 1:
            raise IndexError
        return self._db.iloc[index]

    def __len__(self) -> int:
        """
        Returns the number of rows in the database.
        """
        return len(self._db)

    def get_column(self, column: str) -> list:
        """
        Retrieves all values from a specific column as a list.
        
        Args:
            column (str): The name of the column.
        
        Returns:
            list: List of values from the column, or an empty list if the column is not found.
        """
        try:
            return list(self._db[column])
        except:
            return []

    def load_csv(self, path: str) -> None:
        """
        Loads a new CSV file into the database, replacing the existing data.
        
        Args:
            path (str): Path to the new CSV file.
        """
        self.__init__(path)

    def save_csv(self, path: str = '') -> None:
        """
        Saves the current database to a CSV file. If no path is given, it overwrites the original file.
        
        Args:
            path (str, optional): Path to save the CSV file. Defaults to the original file path.
        """
        if len(path) == 0:
            path = self._path
        self._db.to_csv(path, index=False)
    
    def find(self, column: str, prompt) -> int:
        """
        Searches for a value in a specific column and returns the index of the first match.
        
        Args:
            column (str): Column to search in.
            prompt: The value to search for.
        
        Returns:
            int: The index of the first matching row, or -1 if not found.
        """
        item: pd.DataFrame = self._db[self._db[column] == prompt]
        if len(item):
            return int(item.iloc[0].name)
        return -1

    def change(self, index: int, row: list) -> None:
        """
        Modifies an existing row in the database.
        
        Args:
            index (int): The row index to modify.
            row (list): The new row values.
        
        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index > len(self._db) - 1:
            raise IndexError
        self._db.loc[index] = row

    def add(self, row: list, back: bool = True) -> None:
        """
        Adds a new row to the database.
        
        Args:
            row (list): The new row to add.
            back (bool, optional): If True, adds the row at the end. Defaults to True.
        """
        index: int = -1
        if back:
            index = len(self._db)        
        self._db.loc[index] = row
        self._db = self._db.sort_index().reset_index(drop = True)
    
    def remove(self, index: int) -> None:
        """
        Removes a row from the database by index.
        
        Args:
            index (int): The row index to remove.
        
        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index > len(self._db) - 1:
            raise IndexError
        self._db = self._db.drop(index)
