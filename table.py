from typing import List

MARKDOWN_COL_MAX_LENGTH = 20

class TableGenerator:
    def __init__(self, num_col=None):
        self._num_col = num_col
        self._header = []
        self._contents = []
        self._col_max_length = {}
        
    @property
    def num_col(self):
        return self._num_col

    @num_col.setter
    def num_col(self, num_col: int):
        self._num_col = num_col
    
    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header: List):
        assert isinstance(self._num_col, int)
        if not isinstance(header, list):
            raise AssertionError(f"`header` should be list!")
        if len(header) != self._num_col:
            raise AssertionError(f"`header` {header} has different length from `num_col` ({self._num_col})!")
        self._header = header
    
    def _length_check(self, elem: List):
        length = len(elem)
        _elem = [_ for _ in elem]  # deepcopy
        if length < self._num_col:
            _elem.extend(['' for _ in range(self._num_col - length)])
        return _elem
    
    def append(self, elem: List):
        if not isinstance(elem, list):
            raise AssertionError(f"`elem` should be list!")
        _elem = self._length_check(elem)
        
        self._contents.append(_elem)
    
    def extend(self, elems: List):
        for elem in elems:
            if not isinstance(elem, list):
                raise AssertionError(f"`elem` should be list!")
            _elem = self._length_check(elem)
            
            self._contents.append(_elem) 
    
    def csv_generate(self):
        csv_string = ""
        csv_string += (','.join(map(str, self._header)) + '\n')
        
        for elem in self._contents:
            csv_string += (','.join(map(str, elem)) + '\n')
        
        return csv_string
            
    
    def tsv_generate(self):
        tsv_string = ""
        tsv_string += ('\t'.join(map(str, self._header)) + '\n')
        
        for elem in self._contents:
            tsv_string += ('\t'.join(map(str, elem)) + '\n')
        
        return tsv_string
    
    def markdown_generate(self):
        markdown_string = ""
        markdown_string += ('| ' + ' | '.join(map(str, self._header)) + ' |\n')
        
        markdown_string += ('| ' + ' | '.join(["-----" for _ in range(len(self._header))]) + ' |\n')
        
        for elem in self._contents:
            markdown_string +=  ('| ' + ' | '.join(map(str, elem)) + ' |\n')

        return markdown_string
    
    def generate(self, format='.csv'):
        _format = format.lower()
        
        self._col_max_length = {i: 0 for i in range(self._num_col)}
        
        if 'csv' in _format:
            output = self.csv_generate()
        elif 'tsv' in _format:
            output = self.tsv_generate()
        elif 'markdown' in _format or 'md' in _format:
            output = self.markdown_generate()

        return output