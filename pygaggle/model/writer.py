from pathlib import Path
from typing import List, Optional
import abc

from pygaggle.data.relevance import RelevanceExample

__all__ = ['Writer', 'MsMarcoWriter', 'TrecWriter']


class Writer:
    def __init__(self, path: Optional[Path] = None, overwrite: bool = True, tag: Optional[str] = None):
        self.to_output = str(path) not in [".", None]
        print(f'Writing run: {self.to_output}')
        if self.to_output:
            self.f = open(path, "w" if overwrite else "w+")
        self.tag = tag

    def write_line(self, text: str):
        if self.to_output:
            self.f.write(f"{text}\n")

    @abc.abstractmethod
    def write(self, example: RelevanceExample):
        pass


class MsMarcoWriter(Writer):
    def write(self, example: RelevanceExample):
        for ct, doc in enumerate(example.documents):
            self.write_line(f"{example.query.id}\t{doc.metadata['docid']}\t{ct+1}")


class TrecWriter(Writer):
    def write(self, example: RelevanceExample):
        for ct, doc in enumerate(example.documents):
            self.write_line(f"{example.query.id}\tQ0\t{doc.metadata['docid']}\t{ct+1}\t{doc.score}\t{self.tag}")
