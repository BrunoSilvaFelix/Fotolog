from binary_tree import AVLNode
from photo import Photo

class Catalog:

    def __init__(self, photo: Photo):
        self._index = AVLNode(photo)  
        self.sec_index = dict()

    def add(self, photo: Photo):
        self._index.insert(photo)
        self.sec_index[photo._id] = photo

    def remove(self, id: int):
        p = self.sec_index.get(id)
        self._index.delete(p)

    def get_by_id(self, id):
        result = self.sec_index.get(id)
        if not result:
            raise ValueError(f"Photo with id {id} not found")
        return result

    def next_of(self, id):
        return self._index.successor(self.get_by_id(id))

    def prev_of(self, id):
        return self._index.predecessor(self.get_by_id(id))

    def nearest(self, ts):
        ...

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._index.in_order().__str__()
