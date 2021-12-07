import copy
from functools import total_ordering

class Monom:
    def __init__(self, power, coef=1):
        self.power = int(power)
        self.coef = coef
        self.next = None
        if self.coef - int(self.coef) != 0:
            self.coef = round(self.coef, 2) if round(self.coef, 2) != 0.0 else 0
            if self.coef == 0:
                self.power = 0
        elif type(self.coef) == float:
            self.coef = int(self.coef)

    def __repr__(self): #aX^n
        """
        Sorry I tried to write it neatly but it make a weird error so you got this mess instead.
        :return: repr for monom class
        """
        if self.coef < 0:
            temp = self.coef * - 1
            if self.coef == -1:
                if self.power == 0:
                    return "(-1)"
                if self.power == 1:
                    return "(-1X)"
                return "(-1X^" + str(self.power) + ")"
            if self.power == 1:
                return "(-" + str(temp) + "X)"
            if self.power == 0:
                return "(-" + str(temp) + ")"
            return "(-" + str(temp) + "X^" + str(self.power) + ")"
        if self.coef == 0 and self.power != 0:
            return "0"
        if self.coef == 1:
            if self.power == 0:
                return "1"
            if self.power == 1:
                return "X"
            return "X^" + str(self.power)
        if self.power == 1:
            return str(self.coef) + "X"
        if self.power == 0:
            return str(self.coef)
        return str(self.coef) + "X^" + str(self.power)

    def __mul__(self, other):
        """
        Multiply function to monom
        :param other: monom or number (int or float)
        :return: new monom after multiply
        """
        if isinstance(other, Monom): #check if multiply monom by monom
            c = self.coef * other.coef
            p = self.power + other.power
            return Monom(p, c)
        c = self.coef * other #if not multiply by number
        return Monom(self.power, c)

    def __rmul__(self, other):
        """
        Multiply from right, Call __mul__ function.
        """
        return self.__mul__(other)

    def derivative(self):
        """
        Function to get Monom derivative
        :return: the Monom derivative
        """
        c = self.coef * self.power
        if self.power - 1 < 0:
            p = 0
        else:
            p = self.power - 1
        return Monom(p, c)

    def integral(self):
        """
        Function to get Monom integral
        :return: the Monom integral
        """
        p = self.power + 1
        c = self.coef / p
        return Monom(p, c)

def init_helper(l):
    """
    Helper Function to polynominal init, sort the polynominal and summ simillar monoms
    :param l: list
    :return: sorted list that ready to be polynominal
    """
    l = sorted(l, reverse=True) #sort the list to make my life easier
    p = l[0][0] #first power
    summ = 0 #summ for coefs
    new_l = [] #temp list
    temp = 0
    for i in range(len(l)):
        if p == l[i][0]:
            summ += l[i][1]
            temp += 1
        elif p != l[i][0] and summ == 0:
            if temp > 0:
                new_l.append((p, summ))
                p = l[i][0]
                temp = 0
                summ += l[i][1]
            else:
                new_l.append((p, l[i - 1][1]))
                p = l[i][0]
        else:
            new_l.append((p, summ))
            p = l[i][0]
            summ = l[i][1]
            temp = 0
    new_l.append((p, summ))
    final_l = []
    for j in new_l:
        if j[1] != 0:
            final_l.append(j)
    return final_l

@total_ordering
class Polynomial:
    def __init__(self, l):
        self.head = None
        x = None
        if not isinstance(l, list):
            raise ValueError('Invalid polynomial initialization.')
        else:
            if l == []:
                self.head = Monom(0,0)
            for t in l:
                if not isinstance(t, tuple):
                    raise ValueError('Invalid polynomial initialization.')
                if len(t) != 2:
                    raise ValueError('Invalid polynomial initialization.')
                for c in t:
                    if not isinstance(c, int) and not isinstance(c, float):
                        raise ValueError('Invalid polynomial initialization.')
        if self.head == None:
            l = init_helper(l)
            if l == []: #turn empty list to monom 0
                l.append((0,0))
            for item in range(len(l)): #take the list and make them monoms and add them to the polynominal
                if self.head == None:
                    x = Monom(l[item][0], l[item][1])
                    self.head = x
                else:
                    x.next = Monom(l[item][0], l[item][1])
                    x = x.next

    def __repr__(self):
        if not self.head:
            return "P(X)=0"
        loc = self.head
        txt = ""
        while loc != None:
            txt += loc.__repr__() #access the monom repr and add it to string
            if loc.next != None and loc.next.coef != 0:
                loc = loc.next
                txt += "+"
            else:
                loc = None
        if len(txt) > 0:
            txt = "P(X)=" + txt
        return txt

    def rank(self):
        return self.head.power if self.head != None else 0 #return the rank of the polynominal

    def calculate_value(self, x):
        """
        Function that calculate the value of polynominal with given x (number)
        :param x: number (int or float)
        :return: the valute of the polynominal with the given x
        """
        loc = self.head
        summ = 0
        while loc != None:
            summ += loc.coef * (x ** loc.power)
            loc = loc.next
        return summ

    def __neg__(self):
        """
        function that turn polynominal to negative
        :return: negative Polynominal
        """
        loc = self.head
        final_l = []
        while loc != None:
            final_l.append((loc.power, loc.coef * -1))
            loc = loc.next
        return Polynomial(final_l)

    def __sub__(self, other):
        """
        Function that subtract polynominals
        :param other: other polynominal
        :return: the result from the subtract (Polynominal)
        """
        loc1 = self.head
        loc2 = other.head
        final_l = []
        while loc2 != None:
            final_l.append((loc2.power, loc2.coef * -1))
            loc2 = loc2.next
        while loc1 != None:
            final_l.append((loc1.power, loc1.coef))
            loc1 = loc1.next
        return Polynomial(final_l)

    def __add__(self, other):
        """
        Function that summ polynominals
        :param other: other polynominal
        :return: the result from the summ (Polynominal)
        """
        loc1 = self.head
        loc2 = other.head
        final_l = []
        while loc1 != None:
            final_l.append((loc1.power, loc1.coef))
            loc1 = loc1.next
        while loc2 != None:
            final_l.append((loc2.power, loc2.coef))
            loc2 = loc2.next
        return Polynomial(final_l)

    def __mul__(self, other):
        """
        Function that multiply polynominals
        :param other: other polynominal or scalar
        :return: the result from the multiply (Polynominal)
        """
        if not isinstance(other, Polynomial): #check if not polynominal than multiply by scalar
            final_l = []
            loc = self.head
            while loc != None:
                final_l.append((loc.power, loc.coef * other))
                loc = loc.next
            return Polynomial(final_l)
        else:
            self_l = []
            other_l = []
            final_l = []
            self_loc = self.head
            other_loc = other.head
            while self_loc != None:
                self_l.append((self_loc.power, self_loc.coef))
                self_loc = self_loc.next
            while other_loc != None:
                other_l.append((other_loc.power, other_loc.coef))
                other_loc = other_loc.next
            for i in self_l:
                for j in other_l:
                    final_l.append((i[0]+j[0], i[1]*j[1])) #summ powers and multiply coefs
            return Polynomial(final_l)

    def __rmul__(self, other):
        return self.__mul__(other)

    def derivative(self):
        """
        Function to get Polynominal derivative
        :return: the Polynominal derivative
        """
        final_l = []
        loc = self.head
        while loc != None:
            final_l.append((loc.power - 1, loc.coef * loc.power))
            loc = loc.next
        return Polynomial(final_l)

    def integral(self, other=0):
        """
        Function to get Polynominal integral
        :param other: the C that lost from the derivative
        :return: the new Polynominal integral
        """
        final_l = []
        loc = self.head
        while loc != None:
            final_l.append((loc.power + 1, loc.coef / (loc.power + 1)))
            loc = loc.next
        final_l.append((0, other))
        return Polynomial(final_l)

    def __lt__(self, other):
        """
        Less than Function
        :param other: the other polyniminal to compare
        :return: True if its less than or False if not
        """
        self_loc = self.head
        other_loc = other.head
        while self_loc != None and other_loc != None:
            if self_loc.power > other_loc.power:
                return False
            elif self_loc.power == other_loc.power:
                if self_loc.coef < other_loc.coef:
                    return True
                elif self_loc.coef == other_loc.coef:
                    self_loc = self_loc.next
                    other_loc = other_loc.next
                else:
                    return False
            else:
                return True
        if other_loc != None:
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Greater than Function
        :param other: the other polyniminal to compare
        :return: True if its greater than or False if not
        """
        self_loc = self.head
        other_loc = other.head
        while self_loc != None and other_loc != None:
            if self_loc.power > other_loc.power:
                return True
            elif self_loc.power == other_loc.power:
                if self_loc.coef > other_loc.coef:
                    return True
                elif self_loc.coef == other_loc.coef:
                    self_loc = self_loc.next
                    other_loc = other_loc.next
                else:
                    return False
            else:
                return False
        if self_loc != None:
            return True
        return False

    def __eq__(self, other):
        """
        Equal Function
        :param other: the other polyniminal to compare
        :return: True if its Equal or False if not
        """
        self_loc = self.head
        other_loc = other.head
        while self_loc != None and other_loc != None:
            if self_loc.power == other_loc.power:
                if self_loc.coef == other_loc.coef:
                    self_loc = self_loc.next
                    other_loc = other_loc.next
                else:
                    return False
            else:
                return False
        if self_loc == None and other_loc == None:
            return True
        else:
            return False

class BinTreeNode:
    def __init__(self, val):
        self.value = val
        self.left = self.right = None

class PolynomialBST:
    def __init__(self):
        self.head = None

    def insert(self, val):
        """
        Function to insert polynominal to tree data structure
        :param val: the polynominal to insert
        """
        if self.head == None:
            self.head = BinTreeNode(val)
        else:
            self.insert_rec(val, self.head)

    def insert_rec(self, val, node):
        if val > node.value:
            if node.right == None:
                node.right = BinTreeNode(val)
            else:
                self.insert_rec(val, node.right)
        if val <= node.value:
            if node.left == None:
                node.left = BinTreeNode(val)
            else:
                self.insert_rec(val, node.left)

    def inorder_rec(self, node, lst):
        """
        Helper recursive function to the in order function
        :param node: head
        :param lst: list of polynominals
        :return:
        """
        if node != None:
            self.inorder_rec(node.left, lst)
            lst.append(node.value)
            self.inorder_rec(node.right, lst)
        return lst

    def in_order(self):
        if self.head == None:
            return []
        else:
            return self.inorder_rec(self.head, lst=[])

    def __add__(self, other):
        """
        Add function to trees, summ polynominals
        :param other: other tree
        :return: new tree with the final polynominals
        """
        result = PolynomialBST()
        result.insert(self.head.value)
        self_l = self.in_order()
        if self.head.value in self_l:
            self_l.remove(self.head.value)
        other_l = other.in_order()
        final_l = self_l + other_l
        for i in final_l:
            result.insert(i)
        return result