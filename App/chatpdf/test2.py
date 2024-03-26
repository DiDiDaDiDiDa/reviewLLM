# 定义链表节点类
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 定义函数用于反转链表
def reverseList(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


# 构造示例链表
x = ListNode(1)
x.next = ListNode(2)
x.next.next = ListNode(3)
x.next.next.next = ListNode(4)

y = ListNode(1)
y.next = ListNode(2)

x_reverseList = reverseList(x)
y_reverseList = reverseList(y)

i = 0
sum = 0
while x_reverseList is not None or y_reverseList is not None:
    m, n = 0, 0
    if x_reverseList is not None:
        m = x_reverseList.val
        x_reverseList = x_reverseList.next
    if y_reverseList is not None:
        n = y_reverseList.val
        y_reverseList = y_reverseList.next

    sum += (m + n) * 10 ** i
    i+=1

print('----------',sum,'----------')
