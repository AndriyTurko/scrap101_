import unittest
from unittest import mock
from linked_list import LinkedList, Node


class TestLinkedList(unittest.TestCase):
    def test_init_with_list(self):
        ll = LinkedList([99, 5, 11])
        self.assertEqual(ll.head.data, 99)
        self.assertEqual(ll.head.next.data, 5)
        self.assertEqual(ll.head.next.next.data, 11)

    def test_init_with_args(self):
        ll = LinkedList(99, 5, 11)
        self.assertEqual(ll.head.data, 99)
        self.assertEqual(ll.head.next.data, 5)
        self.assertEqual(ll.head.next.next.data, 11)

    def test_repr_full(self):
        ll = LinkedList(99, 5, 11, 3, 8, 456)
        self.assertEqual(str(ll), '99 -> 5 -> 11 -> 3 -> 8 -> 456 -> None')

    def test_repr_empty(self):
        self.assertEqual(str(LinkedList()), 'None')

    def test_add_at_the_beginning(self):
        ll = LinkedList(5, 11)
        ll.add_at_the_beginning(Node(99))
        self.assertEqual(ll.head.data, 99)
        self.assertEqual(ll.head.next.data, 5)

    def test_add_at_the_end_normal(self):
        ll = LinkedList(99, 5)
        ll._add_at_the_end(Node(11))
        self.assertEqual(str(ll), '99 -> 5 -> 11 -> None')

    def test_add_at_the_end(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        self.assertEqual(llist.head.data, 99)
        llist._add_at_the_end(Node(7))
        a = llist.head
        while a.next is not None:
            a = a.next
        self.assertEqual(a.data, 7)

    def test_add_at_the_end_incorrect_data(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        self.assertEqual(llist.head.data, 99)
        llist._add_at_the_end(Node(7))
        a = llist.head
        while a.next is not None:
            a = a.next
        self.assertEqual(a.data, 7)

    def test_add_at_the_end_empty_list(self):
        llist = LinkedList()
        self.assertEqual(llist.head, None)
        llist._add_at_the_end(Node(7))
        self.assertEqual(llist.head.data, 7)

    def test_add_between_two_nodes(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        llist.add_between_two_nodes(11, Node(10))
        self.assertEqual(llist.head.next.next.next.data, 10)
        self.assertEqual(llist.head.next.next.data, 11)
        self.assertEqual(llist.head.next.next.next.next.data, 3)

    def test_add_between_two_nodes_empty_list(self):
        llist = LinkedList()
        with self.assertRaises(Exception) as context:
            llist.add_between_two_nodes(11, Node(10))
        self.assertEqual(str(context.exception), "List is empty")

    def test_add_between_two_nodes_element_not_found(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        with self.assertRaises(Exception) as context:
            llist.add_between_two_nodes(71, Node(10))
        self.assertEqual(str(context.exception), "Node with data '71' not found")

    def test_add_before_nodes(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        llist.add_before_nodes(11, Node(7))
        self.assertEqual(llist.head.next.next.data, 7)
        self.assertEqual(llist.head.next.next.next.data, 11)

    def test_add_before_nodes_not_found(self):
        ll = LinkedList(99, 5, 11)
        with self.assertRaises(Exception) as context:
            ll.add_before_nodes(42, Node(7))
        self.assertEqual(str(context.exception), "Node with data '42' not found")

    def test_add_before_head(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        llist.add_before_nodes(99, Node(7))
        self.assertEqual(llist.head.data, 7)
        self.assertEqual(llist.head.next.data, 99)

    def test_remove_node_head(self):
        ll = LinkedList(99, 5, 11)
        ll.remove_node(99)
        self.assertEqual(ll.head.data, 5)

    def test_remove_node(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        llist.remove_node(3)
        self.assertEqual(llist.head.next.next.next.data, 8)
        self.assertEqual(llist.head.next.next.next.next.data, 456)

    def test_remove_node_not_found(self):
        ll = LinkedList(99, 5, 11)
        with self.assertRaises(Exception) as context:
            ll.remove_node(42)
        self.assertEqual(str(context.exception), "Node with data '42' not found")

    def test_remove_node_empty(self):
        ll = LinkedList()
        with self.assertRaises(Exception) as context:
            ll.remove_node(11)
        self.assertEqual(str(context.exception), "List is empty")

    def test_get_index(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        self.assertEqual(llist.get_index(0).data, 99)
        self.assertEqual(llist.get_index(2).data, 11)
        self.assertEqual(llist.get_index(-1).data, 456)
        self.assertEqual(llist.get_index(-3).data, 3)

    @mock.patch('linked_list.LinkedList.len')
    def test_get_index_patched(self, patched_len):
        patched_len.return_value = 6
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        self.assertEqual(llist.get_index(0).data, 99)
        self.assertEqual(llist.get_index(4).data, 8)
        self.assertEqual(llist.get_index(-1).data, 456)
        self.assertEqual(llist.get_index(-3).data, 3)

    def test_len(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        self.assertEqual(llist.len(), 6)
        llist2 = LinkedList()
        self.assertEqual(llist2.len(), 0)

    def test_slice(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        sliced = llist.slice(1, 4)
        self.assertEqual(sliced.head.data, 5)
        self.assertEqual(sliced.head.next.data, 11)
        self.assertEqual(sliced.head.next.next.data, 3)
        self.assertIsNone(sliced.head.next.next.next)

    @mock.patch('linked_list.LinkedList.len')
    def test_slice_patched(self, patched_len):
        patched_len.return_value = 6
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        sliced = llist.slice(1, 4)
        self.assertEqual(sliced.head.data, 5)
        self.assertEqual(sliced.head.next.data, 11)
        self.assertEqual(sliced.head.next.next.data, 3)
        self.assertIsNone(sliced.head.next.next.next)


    def test_slice_negative_indexes(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        sliced = llist.slice(-4, -1)
        self.assertEqual(sliced.head.data, 11)
        self.assertEqual(sliced.head.next.data, 3)
        self.assertEqual(sliced.head.next.next.data, 8)
        self.assertIsNone(sliced.head.next.next.next)

    def test_slice_empty_result(self):
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        sliced = llist.slice(4, 2)  
        self.assertIsNone(sliced.head)

    @mock.patch('linked_list.LinkedList._add_at_the_end')
    @mock.patch('linked_list.LinkedList.len')
    def test_failed_slice_patched(self, patched_len, patched_add):
        patched_len.return_value = 6
        patched_add.side_effect = KeyError('Test key error')
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        with self.assertRaises(KeyError) as context:
            llist.slice(1, 4)
        self.assertEqual(str(context.exception), "'Test key error'")
        patched_add.assert_called_once()

    @mock.patch('linked_list.LinkedList._add_at_the_end')
    @mock.patch('linked_list.LinkedList.len')
    def test_failed_slice_patched(self, patched_len, patched_add):
        patched_len.return_value = 6
        patched_add.side_effect = [1, KeyError('Test key error')]
        llist = LinkedList(99, 5, 11, 3, 8, 456)
        with self.assertRaises(KeyError) as context:
            llist.slice(1, 4)
        self.assertEqual(str(context.exception), "'Test key error'")
        self.assertEqual(2, patched_add.call_count)





