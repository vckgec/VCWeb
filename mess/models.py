import datetime
from django.db import models
from django.db import connection
from account.models import Boarder
from django.db.models import Max,Sum

class Presence(models.Model):
    STATUS_CHOICES = (('on', 'ON'), ('off', 'OFF'))
    HALF_CHOICES = (('1MO', 'Morning'), ('2EV', 'Evening'))
    boarder = models.ForeignKey(Boarder, on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    half = models.CharField(choices=HALF_CHOICES, max_length=12)

    def get_status(self):
        if self.status=="on":
            return 'checked'
        else:
            return 'unchecked'

    def get_half(self):
        if self.half == '1MO':
            return 'Morning'
        else:
            return 'Evening'

    def __str__(self):
        return '%s\'s status %s for %s at %s'%(self.boarder,self.status,self.date,self.half)


class MealDish(models.Model):
    HALF_CHOICES = (('1MO', 'Morning'),
                    ('2EV', 'Evening'),)
    dish = models.CharField(blank=True, max_length=100)
    date = models.DateField(blank=True)
    half = models.CharField(choices=HALF_CHOICES, unique_for_date='date', max_length=12, blank=True)
    has_fish = models.BooleanField(default=False)
    has_chicken = models.BooleanField(default=False)
    has_mutton = models.BooleanField(default=False)
    has_egg = models.BooleanField(default=False)

    def get_half(self):
        if self.half == '1MO':
            return 'Morning'
        else:
            return 'Evening'

    def __str__(self):
        return str(self.dish)+'---'+str(self.half)+'---'+str(self.date)


class GuestMeal(models.Model):
    HALF_CHOICES = (('1MO', 'Morning'),
                    ('2EV', 'Evening'),)
    boarder = models.ForeignKey(Boarder,limit_choices_to={'Current_Boarder':True},on_delete=models.CASCADE)
    date = models.DateField()
    half = models.CharField(choices=HALF_CHOICES, max_length=12)
    number = models.IntegerField(default=0)

    def __str__(self):
        return '%s\'s %s guest is added at %s for %s'%(self.boarder,self.number,self.half,self.date)


class MessManager(models.Model):
    start = models.DateField()
    name=models.ManyToManyField(Boarder,blank=True,limit_choices_to={'Current_Boarder':True},unique_for_month='start',unique_for_year='start')
    def __str__(self):
        return 'Mess manager for %s for the year %s' % (self.start.month, self.start.year)


class StoreKeeper(models.Model):
    HALF_CHOICES = (('1MO', 'Morning'),
                    ('2EV', 'Evening'),)
    name = models.ForeignKey(Boarder, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'Year_Of_Passing': Boarder.objects.aggregate(
        Year_Of_Passing=Max('Year_Of_Passing'))['Year_Of_Passing'], 'Current_Boarder': True} if 'mess_storekeeper' in connection.introspection.table_names() else {'Current_Boarder': True}, unique_for_date='date')
    date = models.DateField()
    half = models.CharField(choices=HALF_CHOICES, unique_for_date='date', max_length=12)

    def get_half(self):
        if self.half == '1MO':
            return 'Morning'
        else:
            return 'Evening'
    def __str__(self):
        return str(self.date)+' ('+self.half+')'


class Store(models.Model):
    HALF_CHOICES = (('1MO', 'Morning'), ('2EV', 'Evening'),)
    presence = models.ManyToManyField(Presence, limit_choices_to={'boarder__Current_Boarder': True,'date':datetime.date.today(),'status':'on'},blank=True)
    date = models.DateField(auto_now=True)
    half = models.CharField(choices=HALF_CHOICES,unique_for_date='date', max_length=12)
    meal_dish = models.OneToOneField(MealDish, on_delete=models.CASCADE, blank=True, null=True)
    extra_meals = models.DecimalField(default=4, decimal_places=0, max_digits=2)
    adjust_count = models.IntegerField(default=0)
    guest_meal = models.ManyToManyField(GuestMeal,blank=True,limit_choices_to={'date':datetime.date.today()})
    mess_manager = models.ForeignKey(MessManager, blank=True,on_delete=models.CASCADE, limit_choices_to={'start__month': datetime.date.today().month, 'start__year': datetime.date.today().year})
    store_keeper=models.OneToOneField(StoreKeeper,on_delete=models.CASCADE,blank=True, null=True)

    def get_current_half(self):
        if self.half == '1MO':
            return 1 if datetime.datetime.now().hour < 13 else 2
        else:
            return 1 if datetime.datetime.now().hour > 12 else 2

    def get_total_guest_meal(self):
        total=self.guest_meal.aggregate(Sum('number'))['number__sum']
        return total if total else 0
        

    def get_total_meals(self):
        return self.extra_meals-self.adjust_count+self.presence.count()+self.get_total_guest_meal()

    def get_half(self):
        if self.half == '1MO':
            return 'Morning'
        else:
            return 'Evening'

    def __str__(self):
        return '%s (%s)'%(self.date,self.half)

    def get_absolute_string(self):
        def generate_length_wise_string(string, string_list, length):
            for i in range(length):
                for j in range(len(string)):
                    for k in range(i+j, len(string)-(length-i-1)):
                        if string[j:i+j]+string[k:k+length-i] not in string_list:
                            string_list.append(string[j:i+j]+string[k:k+length-i])
            return string_list

        kwargs = [{'boarder__Eats_Mutton': not self.meal_dish.has_mutton}, {'boarder__Eats_Chicken': not self.meal_dish.has_chicken}, {
                          'boarder__Eats_Fish': not self.meal_dish.has_fish}, {'boarder__Eats_Egg': not self.meal_dish.has_egg}]

        required_kwargs = lambda mutton=None, chicken=None, fish=None, egg=None: {
            **(mutton if mutton else {}), **(chicken if chicken else {}), **(fish if fish else {}), **(egg if egg else {})}

        string = ('1' if self.meal_dish.has_mutton else '')+('2' if self.meal_dish.has_chicken else '')+('3' if self.meal_dish.has_fish else '')+('4' if self.meal_dish.has_egg else '')

        count_string = []
        iteration = []
        string_list = []

        for l in range(1, len(string)+1):
            string_list = generate_length_wise_string(string, string_list, l)

        for generate_string in string_list:
            minusAllNonFromEachNon = self.presence.filter(**required_kwargs(*map(kwargs.__getitem__,map(lambda x:int(x)-1, generate_string)))).count(
            )-self.presence.filter(**required_kwargs(*map(kwargs.__getitem__,map(lambda x:int(x)-1,string)))).count()  # -1 bcz indexing starting from 0

            if minusAllNonFromEachNon:
                iteration.append([minusAllNonFromEachNon, generate_string])

        max_length_string_count = 1
        while True:
            try:
                if len(iteration[len(iteration)-max_length_string_count][1]) > 1:
                    remove_count = 0
                    for i in range(len(iteration)-max_length_string_count):
                        find_count = 0
                        for j in iteration[i-remove_count][1]:
                            if iteration[len(iteration)-max_length_string_count][1].find(j) != -1:
                                find_count += 1
                            else:
                                break
                        if find_count == len(iteration[i-remove_count][1]):
                            if iteration[i-remove_count][0]-iteration[len(iteration)-max_length_string_count][0] > 0:
                                iteration[i-remove_count][0] = iteration[i][0]-iteration[len(iteration)-max_length_string_count][0]
                            else:
                                iteration.remove(iteration[i-remove_count])
                                remove_count += 1
                    max_length_string_count += 1
                else:
                    break
            except:
                break
                
        main_string = ['Mutton', 'Chicken', 'Fish', 'Egg']
        required_string= lambda string: 'Non %s: '%' and '.join(map(main_string.__getitem__,map(lambda x:int(x)-1,string)))

        uncount_veg=0
        for i in iteration:
            count_string.append(required_string(i[1])+str(i[0]))
            uncount_veg+=i[0]
            
        try:
            veg = self.presence.filter(**required_kwargs(*map(kwargs.__getitem__,map(lambda x:int(x)-1,string)))).count()
            if veg:
                count_string.append('Veg: '+str(veg))
            if self.get_total_meals()-veg -uncount_veg:
                count_string.append('Non Veg: '+str(self.get_total_meals()-veg-uncount_veg))
        except:
            pass
        if self.adjust_count:
            count_string.append('Adjustment: '+str(self.adjust_count))

        if self.guest_meal:
            count_string.append('Guest Meal: '+str(self.get_total_guest_meal()))
        return count_string
