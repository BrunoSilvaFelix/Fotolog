import json
import statistics
from photo_avl import PhotoAVL  
from photo import Photo

class Catalog:
    def __init__(self):
        self._index = PhotoAVL()
        self.sec_index = dict() 
        self._next_id = 1

    def _gerar_novo_id(self):
        id_gerado = self._next_id
        self._next_id += 1 
        return id_gerado

    def add(self, photo: Photo):
        if photo._id == 0 or photo._id is None:
            photo._id = self._gerar_novo_id()
            
        if photo._id >= self._next_id:
            self._next_id = photo._id + 1

        if photo._id in self.sec_index:
            raise ValueError(f"Erro: ID {photo._id} duplicado! Tente usar o ID {self._next_id}.")
        
        self._index.insert(photo)
        self.sec_index[photo._id] = photo

    def remove(self, id: int):
        p = self.sec_index.get(id)
        if not p:
            raise ValueError(f"Erro: Foto com id {id} não encontrada.")
        
        self._index.delete(p)
        self.sec_index.pop(id)

    def get_by_id(self, id):
        result = self.sec_index.get(id)
        if not result:
            raise ValueError(f"Photo with id {id} not found")
        return result

    def __get_by_id_in_tree(self, id):
        p: Photo = self.get_by_id(id)
        return self._index.get_node(p)

    def next_of(self, id):
        node = self.__get_by_id_in_tree(id)
        if node:
            res = self._index.successor(node)
            return res.data() if res else None
        return None

    def prev_of(self, id):
        node = self.__get_by_id_in_tree(id)
        if node:
            res = self._index.predecessor(node)
            return res.data() if res else None
        return None

    def range(self, ts1, ts2):
        t1 = Photo(0, ts1, "")._timestamp
        t2 = Photo(0, ts2, "")._timestamp
        return self._index.range_search(t1, t2)

    def nearest(self, ts):
        t = Photo(0, ts, "")._timestamp
        return self._index.nearest(t)

    def remove_range(self, ts1, ts2):
        fotos_no_intervalo = self.range(ts1, ts2)
        for f in fotos_no_intervalo:
            self.remove(f._id)
        return len(fotos_no_intervalo)

    def tag(self, id: int, t: str):
        foto = self.get_by_id(id)
        if t not in foto._tags:
            foto._tags.append(t)

    def rate(self, id: int, r: int):
        if not (0 <= r <= 5):
            raise ValueError("O rating deve estar entre 0 e 5.")
        foto = self.get_by_id(id)
        foto._rating = r

    def find_by_tag(self, tag):
        todos_os_nos = self._index.in_order()
        return [n.data() for n in todos_os_nos if tag in n.data()._tags]

    def stats(self):
        if not self.sec_index:
            return "Catálogo vazio."
        
        timestamps = [p._timestamp for p in self.sec_index.values()]
        ratings = [p._rating for p in self.sec_index.values() if p._rating is not None]
        
        return {
            "total": len(self.sec_index),
            "mais_antiga": min(timestamps),
            "mais_recente": max(timestamps),
            "rating_medio": statistics.mean(ratings) if ratings else 0,
            "rating_mediano": statistics.median(ratings) if ratings else 0
        }

    def save(self, path):
        data = []
        for p in self.sec_index.values():
            data.append({
                "id": p._id,
                "ts": p._timestamp,
                "path": p._path,
                "tags": p._tags,
                "rating": p._rating
            })
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self._index = PhotoAVL()
            self.sec_index = dict()
            for d in data:
                self.add(Photo(d['id'], d['ts'], d['path'], d.get('tags', []), d.get('rating')))

    def __str__(self):
        return self._index.in_order().__str__()