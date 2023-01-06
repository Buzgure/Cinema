from typing import List

from Domain.undo_redo_operations import UndoRedoOperations


class UndoRedoService:
    def __init__(self):
        self.undo_list: List[UndoRedoOperations] = []
        self.redo_list: List[UndoRedoOperations] = []

    def do_undo(self):
        while self.undo_list:
            top_operation = self.undo_list.pop()
            top_operation.undo()
            self.redo_list.append(top_operation)

    def do_redo(self):
        while self.redo_list:
            top_operation = self.redo_list.pop()
            top_operation.redo()
            self.undo_list.append(top_operation)

    def clear_redo(self):
        self.redo_list.clear()

    def add_to_undo(self, operation: UndoRedoOperations):
        self.undo_list.append(operation)
