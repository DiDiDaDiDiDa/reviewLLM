class ListNode:
    def __init__(self, value=0, next=None):
        self.val = value
        self.next = next


def reverse_listNode(head):
    if head is None:
        return None
    pre = None
    cur = head
    while cur:
        temp = cur.next
        cur.next = pre
        pre = cur
        cur = temp
    return pre


def add_node(listNode1, listNode2):
    i, sum = 0, 0
    while listNode1 is not None or listNode2 is not None:
        m, n = 0, 0
        if listNode1 is not None:
            m = listNode1.val
            listNode1 = listNode1.next
        if listNode2 is not None:
            n = listNode2.val
            listNode2 = listNode2.next
        sum += (m + n) * 10 ** i
        i += 1
    return sum


def test_reverse_listNode():
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head = reverse_listNode(head)
    assert head.val == 3
    assert head.next.val == 2
    assert head.next.next.val == 1


def test_add_node():
    listNode1 = ListNode(2)
    listNode1.next = ListNode(4)
    listNode1.next.next = ListNode(3)
    listNode2 = ListNode(5)
    listNode2.next = ListNode(6)
    reversed_listNode1 = reverse_listNode(listNode1)
    reversed_listNode2 = reverse_listNode(listNode2)

    result = add_node(reversed_listNode1, reversed_listNode2)
    assert result == 299
