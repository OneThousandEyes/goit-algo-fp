class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data, end=" -> " if cur.next else "\n")
            cur = cur.next

    def reverse(self):
        """Реверс однозв'язного списку."""
        prev = None
        cur = self.head

        while cur:
            nxt = cur.next      # запам'ятали наступний
            cur.next = prev     # розвернули посилання
            prev = cur          # посунули prev
            cur = nxt           # посунули cur

        self.head = prev

    # Merge Sort для однозв'язного списку 
    def sort_merge(self):
        self.head = self._merge_sort(self.head)

    def _merge_sort(self, head: Node | None) -> Node | None:
        if head is None or head.next is None:
            return head

        mid = self._split_middle(head)          # розбили на 2 половини
        left_sorted = self._merge_sort(head)    # сортуємо ліву
        right_sorted = self._merge_sort(mid)    # сортуємо праву

        return self._merge_two_sorted(left_sorted, right_sorted)

    def _split_middle(self, head: Node) -> Node:
        """Знаходить середину списку та розбиває його на дві частини."""
        slow = head
        fast = head
        prev = None

        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        # prev - останній вузол лівої половини
        prev.next = None
        return slow

    def _merge_two_sorted(self, a: Node | None, b: Node | None) -> Node | None:
        dummy = Node(0)
        tail = dummy

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        tail.next = a if a else b
        return dummy.next

    def merge_sorted_lists(l1: LinkedList, l2: LinkedList) -> LinkedList:
        merged = LinkedList()
        dummy = Node(0)
        tail = dummy

        a = l1.head
        b = l2.head

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        tail.next = a if a else b
        merged.head = dummy.next
        return merged


if __name__ == "__main__":
    llist = LinkedList()
    for x in [10, 3, 7, 1, 9, 2]:
        llist.insert_at_end(x)

    print("Початковий список:")
    llist.print_list()

    print("\nРеверс:")
    llist.reverse()
    llist.print_list()

    print("\nСортування злиттям:")
    llist.sort_merge()
    llist.print_list()

    # Два відсортовані списки для merge
    a = LinkedList()
    for x in [1, 4, 6, 10]:
        a.insert_at_end(x)

    b = LinkedList()
    for x in [2, 3, 7, 8, 9]:
        b.insert_at_end(x)

    print("\nСписок A:")
    a.print_list()
    print("Список B:")
    b.print_list()

    merged = LinkedList.merge_sorted_lists(a, b)
    print("\nMerged(A, B):")
    merged.print_list()
