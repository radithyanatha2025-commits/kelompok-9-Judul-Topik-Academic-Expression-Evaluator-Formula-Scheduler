class VarBSTNode:
    def __init__(self, key: str, val: float):
        self.key = key
        self.val = val
        self.left: Optional['VarBSTNode'] = None
        self.right: Optional['VarBSTNode'] = None
 
 
class VarBST:
    """
    Binary Search Tree untuk menyimpan variabel (symbol table).
    Key = nama variabel (string), value = float.
    Mensimulasikan symbol table pada compiler.
    Big-O operasi: O(log n) rata-rata, O(n) worst case.
    Untuk 26 variabel (a-z): O(log 26) ≈ O(1) praktis.
    """
    def __init__(self):
        self.root: Optional[VarBSTNode] = None
 
    def set(self, key: str, val: float) -> None:
        """
        Insert atau update variabel. Big-O: O(log n).
        Jika key sudah ada, update nilainya.
        """
        self.root = self._set(self.root, key, val)
 
    def _set(self, node: Optional[VarBSTNode], key: str, val: float) -> VarBSTNode:
        if node is None:
            return VarBSTNode(key, val)
        if key < node.key:
            node.left = self._set(node.left, key, val)
        elif key > node.key:
            node.right = self._set(node.right, key, val)
        else:
            node.val = val  # update nilai jika key sama
        return node
 
    def get(self, key: str) -> Optional[float]:
        """Cari variabel berdasarkan key. Big-O: O(log n)."""
        node = self._get(self.root, key)
        return node.val if node else None
 
    def _get(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None:
            return None
        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        return node
 
    def delete(self, key: str) -> None:
        """Hapus variabel berdasarkan key. Big-O: O(log n)."""
        self.root = self._delete(self.root, key)
 
    def _delete(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node ditemukan, hapus dengan 3 kasus:
            if node.left is None:
                return node.right  # kasus 1 & 2: 0 atau 1 anak
            if node.right is None:
                return node.left
            # Kasus 3: 2 anak → ganti dengan inorder successor (minimum kanan)
            successor = self._min_node(node.right)
            node.key = successor.key
            node.val = successor.val
            node.right = self._delete(node.right, successor.key)
        return node
 
    def _min_node(self, node: VarBSTNode) -> VarBSTNode:
        while node.left:
            node = node.left
        return node
 
    def list_all(self) -> List[Tuple[str, float]]:
        """
        Inorder traversal → variabel terurut secara alfabetis.
        Big-O: O(n).
        """
        result = []
        self._inorder(self.root, result)
        return result
 
    def _inorder(self, node: Optional[VarBSTNode], result: list) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append((node.key, node.val))
        self._inorder(node.right, result)
 
    def clear(self) -> None:
        """Hapus semua variabel. Big-O: O(1)."""
        self.root = None
 
