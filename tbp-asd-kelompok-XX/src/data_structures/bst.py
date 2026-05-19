MODUL 3: BST Tabel Variabel (SATU-SATUNYA BST DALAM PROGRAM)
Binary Search Tree untuk menyimpan variabel dengan kunci (a-z)
"""

from typing import Optional, List, Tuple


class VarBSTNode:
    """NODE UNTUK BST"""
    __slots__ = ('key', 'val', 'left', 'right')
    def __init__(self, key: str, val: float):
        self.key = key      # Kunci: huruf a-z (unique)
        self.val = val      # Nilai: float
        self.left = None    # Anak kiri (key lebih kecil)
        self.right = None   # Anak kanan (key lebih besar)


class VarBST:
    """
    BINARY SEARCH TREE (BST) untuk menyimpan variabel
    Property BST: left.key < node.key < right.key
    """
    def __init__(self):
        self.root = None    # Akar pohon

    # ========== INSERT / UPDATE ==========
    def set(self, key: str, val: float) -> None:
        """SET <var> <nilai> - O(log n)"""
        if not isinstance(key, str) or len(key) != 1 or not key.isalpha():
            raise ValueError("Nama variabel harus satu huruf a-z")
        self.root = self._set(self.root, key, val)

    def _set(self, node: Optional[VarBSTNode], key: str, val: float) -> VarBSTNode:
        if node is None:
            return VarBSTNode(key, val)     # Leaf baru
        
        if key < node.key:
            node.left = self._set(node.left, key, val)   # Ke kiri
        elif key > node.key:
            node.right = self._set(node.right, key, val) # Ke kanan
        else:
            node.val = val   # Update nilai jika key sudah ada
        
        return node

    # ========== SEARCH ==========
    def get(self, key: str) -> Optional[float]:
        """GET <var> - O(log n)"""
        node = self._get(self.root, key)
        return node.val if node else None

    def _get(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._get(node.left, key)    # Cari di kiri
        else:
            return self._get(node.right, key)   # Cari di kanan

    # ========== DELETE ==========
    def delete(self, key: str) -> None:
        """DELETE <var> - O(log n)"""
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Ketemu node yang akan dihapus!
            
            # Case 1: Tidak punya anak
            if node.left is None and node.right is None:
                return None
            
            # Case 2: Punya 1 anak
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Case 3: Punya 2 anak
            # Cari successor (node paling kiri dari subtree kanan)
            succ = self._min(node.right)
            node.key = succ.key
            node.val = succ.val
            node.right = self._delete(node.right, succ.key)
        
        return node

    def _min(self, node: VarBSTNode) -> VarBSTNode:
        """Cari node dengan key terkecil"""
        while node.left:
            node = node.left
        return node

    # ========== TRAVERSAL ==========
    def list_all(self) -> List[Tuple[str, float]]:
        """LIST - Inorder traversal = hasil TERURUT O(n)"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[VarBSTNode], out: List[Tuple[str, float]]) -> None:
        """Inorder: kiri → node → kanan (menghasilkan urutan ascending)"""
        if node:
            self._inorder(node.left, out)
            out.append((node.key, node.val))
            self._inorder(node.right, out)

MODUL 6: CLI - Menggunakan berbagai struktur data
"""
