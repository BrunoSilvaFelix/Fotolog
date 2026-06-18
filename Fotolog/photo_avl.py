from binary_tree import AVLTree
from photo import Photo

class PhotoAVL(AVLTree):
    def range_search(self, ts1, ts2):
        result = []
        self._range_search_helper(self._root, ts1, ts2, result)
        return result

    def _range_search_helper(self, root, ts1, ts2, result):
        if not root:
            return
        
        photo = root.data()
        
        # Poda à esquerda
        if photo._timestamp >= ts1:
            self._range_search_helper(root.left_node(), ts1, ts2, result)
            
        # Adiciona se estiver no intervalo
        if ts1 <= photo._timestamp <= ts2:
            result.append(photo)
            
        # Poda à direita
        if photo._timestamp <= ts2:
            self._range_search_helper(root.right_node(), ts1, ts2, result)

    def nearest(self, ts):
        if self.empty():
            return None
        return self._nearest_helper(self._root, ts, self._root.data())

    def _nearest_helper(self, root, ts, best_photo):
        if not root:
            return best_photo
        
        curr = root.data()
        curr_diff = abs(curr._timestamp - ts)
        best_diff = abs(best_photo._timestamp - ts)

        # Atualiza a melhor foto se encontrou uma mais próxima ou para desempate
        if curr_diff < best_diff or (curr_diff == best_diff and curr._id < best_photo._id):
            best_photo = curr

        if ts < curr._timestamp:
            return self._nearest_helper(root.left_node(), ts, best_photo)
        elif ts > curr._timestamp:
            return self._nearest_helper(root.right_node(), ts, best_photo)
        else:
            return curr

    def get_node(self, photo):
        # Utiliza o search herdado da BinaryTree/AVLTree
        belongs, node = self.search(photo)
        return node if belongs else None