from abc import ABC, abstractmethod


class UndoRedoOperations(ABC):

    @abstractmethod
    def undo(self):
        ...

    @abstractmethod
    def redo(self):
        ...
