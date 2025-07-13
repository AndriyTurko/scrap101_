def dva(a):
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
    return a


def three(a):
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
        print(1111, a)
    if a[1] > a[2]:
        a[1], a[2] = a[2], a[1]
        print(2222, a)
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
        print(3333, a)
    return a


def five_without_cycle(a):
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
    if a[1] > a[2]:
        a[1], a[2] = a[2], a[1]
    if a[2] > a[3]:
        a[2], a[3] = a[3], a[2]
    if a[3] > a[4]:
        a[3], a[4] = a[4], a[3]
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
    if a[1] > a[2]:
        a[1], a[2] = a[2], a[1]
    if a[2] > a[3]:
        a[2], a[3] = a[3], a[2]
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
    if a[1] > a[2]:
        a[1], a[2] = a[2], a[1]
    if a[0] > a[1]:
        a[0], a[1] = a[1], a[0]
    return a


def sort_five(a):
    j = 0
    while j < len(a)-1:
        print('start', j)
        if a[j] > a[j+1]:
            print('list before', a)
            a[j], a[j + 1] = a[j + 1], a[j]
            print('list after', a)
            print('j before', j)
            j = -1
            print('j after', j)
        j += 1
        print('end', j)
    return a


def povtor(a):
    j = 0
    while j < len(a)-1:
        if a[j] > a[j+1]:
            a[j], a[j + 1] = a[j + 1], a[j]
            j = -1
        if a[j] == a[j + 1]:
            a.remove(a[j])
            j = -1
        j += 1
    return a


def povtor_two(a):
    return list(set(a))


def sort_anyone(a):
    for i in range(len(a)):
        print(1111, i)
        for j in range(len(a)-i-1):
            print(222, j)
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                print(a)
    return a



def sort_anyone_two(a):
    i = 0
    for x in range(len(a)):
        b = len(a) - x
        for c in range(b-1):
            i += 1
            if a[c] > a[c+1]:
                a[c], a[c+1] = a[c+1], a[c]
    print(i)
    return a


def ins_sort(k):
    y = 0
    for i in range(1, len(k)):
        j = i
        temp = k[j]
        while j > 0 and temp < k[j-1]:
            y += 1
            k[j] = k[j-1]
            j=j-1
        k[j] = temp
    print(y)
    return k

def factorial(a):
    if a == 0:
        return 1
    else:
        return a * factorial(a-1)


def povtor_improved(a):
    b = []
    for x in a:
        if x not in b:
            b.append(x)
    return b


def enter(a):
    d = {}
    for x in a:
        if x not in d:
            d[x] = 1
        else:
            d[x] += 1
    return d


def enter_and_povtor(a):
    d = {}
    b = []
    for x in a:
        print(x)
        if x not in b:
            b.append(x)
            d[x] = 1
        else:
            d[x] += 1
            print(d)
    return b, d



def ins_sort_with_explanation(k):
    for i in range(1,len(k)):    #since we want to swap an item with previous one, we start from 1
        j = i                    #create i's copy (or not)
        temp = k[j]              #temp will be used for comparison with previous items, and sent to the place it belongs
        while j > 0 and temp < k[j-1]: #j>0 bcoz no point going till k[0] since there is no seat available on its left, for temp
            k[j] = k[j-1] #Move the bigger item 1 step right to make room for temp
            j=j-1 #take k[j] all the way left to the place where it has a smaller/no value to its left.
        k[j] = temp
    return k


def ins_sort_two(k):
    for i in range(1,len(k)):
        j = i
        temp = k[j]
        while j > 0 and temp < k[j-1]:
            k[j] = k[j-1]
            j=j-1
        k[j] = temp
    return k


def povtor_nested(a, n):
    b = 0
    for x in a:
        if x == n:
            b += 1
        elif isinstance(x, list):
            b += povtor_nested(x, n)
    return b



def merch_dict(d, d2):
    for q in d2:
        if q in d:
            d[q] += d2[q]
        else:
            d[q] = d2[q]
    return d

def povtor_nested_two(a):
    d = {}
    for x in a:
        if isinstance(x, list):
            d2 = povtor_nested_two(x)
            d = merch_dict(d, d2)
        elif x not in d:
            d[x] = 1
        elif x in d:
            d[x] += 1
    return d


def find_index(a, n):
    l = []
    y = 0
    for x in a:
        if x == n:
            l.append(y)
        y += 1
    return l


def find_index_four(a, n):
    l = []
    for y, x in enumerate(a):
        print(y, x)
        if x == n:
            l.append(y)
    return l


def find_index_nested(a, n):
    l = []
    for i, v in enumerate(a):
        if isinstance(v, list):
            l2 = find_index_nested(v, n)
            if l2:
                b = [i] + l2
                l.append(b)
        if v == n:
            l.append([i])
    return l


def the_biggest_sum_pidspusky(a, k):
    l = 0
    j = []
    while l < len(a)-k+1:
        s = 1
        r = a[l]
        while s <= k-1:
            r += a[l+s]
            s += 1
        j.append(r)
        l += 1
    return max(j)


def the_biggest_sum_pidspusky_two(a, k):
    l = 0
    m = 0
    while l < len(a)-k+1:
        s = 1
        r = a[l]
        while s <= k-1:
            r += a[l+s]
            s += 1
        if r > m:
            m = r
        l += 1
    return m


def the_biggest_sum_pidspusky_three(a, k):
    l = 0
    m = 0
    while l < len(a)-k+1:
        r = sum(a[l:l+k])
        if r > m:
            m = r
        l += 1
    return m


def dnum(a):
    if a >= 10:
        return dnum(a/10) + 1
    else:
        return 1


def count_smaller_elements_right(a):
    result = []
    for i in range(len(a)):
        print(i, 1111111)
        count = 0
        for j in range(i+1, len(a)):
            print(j, 2222222)
            print(a[j], a[i], 3333333)
            if a[j] < a[i]:
                count += 1
            print(count, 4444444)
        result.append(count)
    return result


