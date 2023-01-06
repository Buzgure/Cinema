from Domain.entity import Entity
from Domain.undo_redo_operations import UndoRedoOperations
from Repository.repository import Repository


class UpdateOperation(UndoRedoOperations):

    def __init__(self,
                 repository: Repository,
                 update_entity: Entity,
                 prev_entity: Entity):
        self.repository = repository
        self.update_entity = update_entity
        self.prev_entity = prev_entity

    def undo(self):
        self.repository.update(self.prev_entity)

    def redo(self):
        self.repository.update(self.update_entity)
