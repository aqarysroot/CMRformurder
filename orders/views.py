
from rest_framework import viewsets, mixins
from rest_framework_xml.parsers import XMLParser
from rest_framework.response import Response
from datetime import datetime, timedelta

from .serilalizers import OrderSerializer, PaymentSerializer
from .models import Order, Target, Payment
from users.models import User


# # Create your views here.

class TempOrder: # Custom data stucture 
    def __init__(self, username, age, priority, difficulty):
        self.username = username
        self.age = age
        self.priority = priority
        self.difficulty = difficulty
        self.children = []
    
    def get_time(self):
        if self.children:
            increment = 1
            for child in self.children:
                if child.age < 40:
                    increment *= 1.5  
                else:
                    increment *= 2
            return self.difficulty*increment
        else:
            return self.difficulty
    
    def __lt__(self, other): # to support sorting 
        if isinstance(other, type(self)):
            return self.priority < other.priority
        return TypeError()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.priority == other.priority
        return TypeError()

    def __iter__(self): # to suppport iteration
        return self

    def __hash__(self): # to support hashing which allows to store in set and dict
        return hash(self.username)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    parser_classes = (XMLParser,)

    def parseFromXmltoList(self, usernames_list, xml_data): # parses data in one iteration
        link_dict = {} # Stores usernames' link to find where it belongs
        for item in xml_data: 
            if not User.objects.filter(username=item['username']):
                to = TempOrder(item['username'], item['age'], item['priority'], item['difficulty'])
                link_dict[item['username']] = to
                if item['link']:
                    link_dict[item['link']].children.append(to)
                usernames_list.append(to)

    def dfs(self, node, final_order, alreadyDeadUsers_set, ancestors_set): # depth-first search alorithm works with N-ry Tree(where tree can have more than 2 branches)
        for child in sorted(node.children):
            if child not in alreadyDeadUsers_set and child not in ancestors_set: # acestors_set is needed to avoid infinite recursion
                temp_ancestors_set = ancestors_set.copy() # set's Shallow copy to not send the same sets
                temp_ancestors_set.add(child)  
                self.dfs(child, final_order, alreadyDeadUsers_set, temp_ancestors_set)
                final_order.append(child)
                alreadyDeadUsers_set.add(child)
    
    def sortOrderList(self, final_order, usernames_list): 
        alreadyDeadUsers_set = set()
        for username in sorted(usernames_list): # starts proccess with the most prioritest usernames
            if username not in alreadyDeadUsers_set:
                self.dfs(username, final_order, alreadyDeadUsers_set, {username})
                final_order.append(username)
                alreadyDeadUsers_set.add(username)  

    def create(self, request):
        usernames_list = []
        self.parseFromXmltoList(usernames_list, request.data)
        final_order = []
        self.sortOrderList(final_order, usernames_list)

        order = Order.objects.create(user=request.user)
        count_hours = 0
        for target in final_order:
            count_hours += target.get_time()
            Target.objects.create(username=target.username, order=order, age=target.age, time_to_death=datetime.now() + timedelta(hours=count_hours))
        order.finish_time = datetime.now() + timedelta(hours=count_hours)
        order.save()
        return_data = {
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(hours=count_hours),
            'hours': count_hours,
            'order': [target.username for target in final_order]
        }
        payment = Payment.objects.create(user=request.user, order=order,cost=count_hours*len(final_order)*10)
        payment.save()
        return Response({'received data': return_data})
        
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request):
        return Response({'user': str(request.user), 'amount': request.data['amount']})            