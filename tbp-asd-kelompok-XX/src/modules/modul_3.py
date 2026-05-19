class VarBSTNode:
    """Node untuk BST variabel."""
    __slots__ = ('key', 'val', 'left', 'right')
    def __init__(self, key: str, val: float):
        self.key = key      # nama variabel (satu huruf, a-z)
        self.val = val      # nilai numerik
        self.left = None
        self.right = None


class VarBST:
    """
    Binary Search Tree untuk menyimpan variabel.
    Kunci: satu huruf (a-z). Operasi:
        - set(key, val)  : insert atau update
        - get(key)       : ambil nilai, return None jika tidak ada
        - delete(key)    : hapus node
        - list_all()     : kembalikan semua pasangan (key, val) dalam urutan inorder
    Kompleksitas: O(log m) dengan m <= 26, praktis O(1)
    """

    def __init__(self):
        self.root = None

    # --- SET (insert/update) ---
    def set(self, key: str, val: float) -> None:
        """Menyisipkan atau memperbarui variabel. Key harus satu huruf a-z."""
        if len(key) != 1 or not key.isalpha():
            raise ValueError("Nama variabel harus satu huruf a-z")
        self.root = self._set(self.root, key, val)

    def _set(self, node: Optional[VarBSTNode], key: str, val: float) -> VarBSTNode:
        """Rekursif untuk menyisipkan atau memperbarui node."""
        if node is None:
            return VarBSTNode(key, val)
        if key < node.key:
            node.left = self._set(node.left, key, val)
        elif key > node.key:
            node.right = self._set(node.right, key, val)
        else:
            node.val = val   # update nilai jika key sudah ada
        return node

    # --- GET (search) ---
    def get(self, key: str) -> Optional[float]:
        """Mengembalikan nilai variabel, atau None jika tidak ditemukan."""
        node = self._get(self.root, key)
        return node.val if node else None

    def _get(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        """Rekursif mencari node dengan key tertentu."""
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._get(node.left, key)
        else:
            return self._get(node.right, key)

    # --- DELETE ---
    def delete(self, key: str) -> None:
        """Menghapus variabel dari BST."""
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        """Rekursif menghapus node dengan key."""
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node ditemukan
            # Kasus 1: tidak punya anak atau satu anak
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Kasus 2: dua anak, cari successor inorder
            succ = self._min(node.right)
            node.key = succ.key
            node.val = succ.val
            node.right = self._delete(node.right, succ.key)
        return node

    def _min(self, node: VarBSTNode) -> VarBSTNode:
        """Mencari node dengan key terkecil dalam subtree."""
        while node.left:
            node = node.left
        return node

    # --- LIST (inorder traversal) ---
    def list_all(self) -> List[Tuple[str, float]]:
        """Mengembalikan daftar (key, val) terurut berdasarkan key."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[VarBSTNode], out: List[Tuple[str, float]]) -> None:
        """Rekursif inorder traversal."""
        if node:
            self._inorder(node.left, out)
            out.append((node.key, node.val))
            self._inorder(node.right, out)
