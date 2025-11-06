'''
set.py

Declaration of the Set class and underlying data structure for
storing term-definition pairs with corresponding data. 
Contains definition of Entry class to provide schema for data

History: 
21 Oct 2025 - Created, v1.0
'''

import os, csv, re

class Set: 
    '''
    Set class
    
    Contains all data for a single study set.
    
    Attributes: 
    - data: list
        List containing all set entries (dictionary type), according to 
        below schema (should be updated as features are added).

    The from_file() method automatically detects CSV format, to a limit. 
    Tab-delimited files seem to work best.
    '''
    # Constants
    ACCEPT_FILETYPES = [".csv"]
    ILLEGAL_CHARS_RE = re.compile('[/\\<>:"|?*]')

    # Entry schema
    class _Entry: 
        '''
        Entry class
        
        Data schema for storing term-definition pairs and related data
        N.B. this is a *private class* - should be used only within the Set class
        Both the '__slots__' attribute and the constructor  must be updated to add
        new fields to the class.
        
        Attributes: 
        - data: list
            List containing all set entries (dictionary type), according to 
            below schema (should be updated as features are added).
        '''
        # Data schema
        __slots__ = [
            "term", 
            "definition"
        ]

        def __init__(self, data: dict):
            '''
            Entry class constructor
            '''
            self.term = data["term"]
            self.definition = data["definition"]
        
        def __repr__(self):
            return str({k: getattr(self, k) for k in self.__slots__})

    def __init__(self, save_file_path, init_data: list = None):
        '''
        Set class constructor
        '''
        if init_data:
            if not (isinstance(init_data, list) or isinstance(init_data, tuple)):
                print(type(init_data))
                raise ValueError("init_data must be iterable type!")
            # Schema validation handled in _Entry class
            self.data = [self._Entry(ent) for ent in init_data]
        else: 
            self.data = []

        self.path = save_file_path

    @classmethod
    def from_file(cls, path: str):
        '''
        Alternate constructor for Set class
        ------
        Parameters: 
        - path: str
            Path to set data file
            Expects .csv format (more to be added later)
        -------
        Returns: Set object
        '''
        _, ext = os.path.splitext(path)
        if ext not in cls.ACCEPT_FILETYPES: 
            raise ValueError("Filetype must be in " + str(cls.ACCEPT_FILETYPES))
        
        if ext == ".csv":
            with open(path, 'r', encoding='utf-8') as f:
                # Detect CSV format
                csvDialect = csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
                columnNames = cls._Entry.__slots__
                csvData = csv.DictReader(f, columnNames, dialect=csvDialect)
                return cls([row for row in csvData])
        else: 
            raise NotImplementedError(f"Handler for filetype {ext} not yet implemented.")

    def save(self): 
        '''
        Save current state of Set to specified filepath
        '''
        os.makedirs(os.path.dirname(self.path), exist_ok=True)  # Make set directory if not exists
        with open(self.path, 'w') as file: 
            writer = csv.DictWriter(file, fieldnames = self._Entry.__slots__, dialect='unix')
            writer.writeheader()
            writer.writerows(self.data)

    @classmethod
    def to_set_path(cls, set_name): 
        '''
        Transform the provided string into the path to
        a csv file for a set with that name.
        Paths are relative to project root
        '''
        if re.match(cls.ILLEGAL_CHARS_RE, set_name): 
            raise ValueError("Set name contains illegal characters")
        return f"./sets/{set_name}.csv"
