


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


    def __repr__(self):
        return str(self.data)




class LinkedList:
    def __init__(self, *args):
        print(args)
        self.head = None
        if len(args) == 1 and isinstance(args[0], list):
            nodes = args[0]
        else:
            nodes = list(args)
        if nodes:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    # def __repr__(self):
    #     node = self.head
    #     nodes = []
    #     while node is not None:
    #         nodes.append(str(node.data))
    #         node = node.next
    #     nodes.append("None")
    #     return " -> ".join(nodes)

    def __repr__(self):
        node = self.head
        result = ""
        while node is not None:
            result += str(node.data) + " -> "
            node = node.next
        result += "None"
        return result

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def add_at_the_beginning(self, node):
        node.next = self.head
        self.head = node

    def _add_at_the_end(self, node):
        if not isinstance(node, Node):
            raise TypeError(f"Argument should be type Node, but it is type {type(node)}")
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node

    def append(self, data):
        node = Node(data)
        self._add_at_the_end(node)

    def add_between_two_nodes(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return

        raise Exception("Node with data '%s' not found" % target_node_data)

    def add_before_nodes(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            return self.add_at_the_beginning(new_node)

        prev_node = self.head
        for node in self:
            if node.data == target_node_data:
                prev_node.next = new_node
                new_node.next = node
                return
            prev_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)

    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.data == target_node_data:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)

    def get_index(self, index):
        length = self.len()
        if index < 0:
            index = length + index

        if index < 0 or index >= length:
            raise IndexError("List index out of range")

        for i, node in enumerate(self):
            if i == index:
                return node

    def len(self):
        count = 0
        a = self.head
        while a:
            count += 1
            a = a.next
        return count

    def slice(self, start, stop):
        length = self.len()
        if start < 0:
            start += length
        if stop < 0:
            stop += length
        start = max(start, 0)
        stop = min(stop, length)
        if start > stop:
            return LinkedList()
        slice_ll = LinkedList()
        index = 0
        for x in self:
            if start <= index < stop:
                slice_ll._add_at_the_end(Node(x.data))
            elif index >= stop:
                break
            index += 1
        return slice_ll











