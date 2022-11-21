"""
Case Hotel 
======================
Developers:
Pichuev D.  - 85%
Dyakovich A. - 35%
Trushkin N. - 20%
"""
from datetime import date,timedelta
from random import randint
global TotalRevenue
global TotalLoses
global firstdate
def variation_people_count(variation):
	roomn=int(str(variation)[:-1])
	for room in Room.rooms:
		if room.room_number == roomn:
			return int(room.count_guests)
def de_variation(variation):
	variation=str(variation)
	return int(variation[:-1]),int(variation[-1])
class Hotel:
	'''The main control class'''
	def __init__(self):
		pass

	@staticmethod
	def choice(people_count,arrival_date, day_count, money_count):
		Room.refresh_var_dict()
		cost_list=[]
		arrival_date,day_count,people_count=date2days(arrival_date),int(day_count),int(people_count)
		cost_dict={}
				
		for variation_set in Room.var_dict.values():
				
				for variation  in variation_set:
					room_number,food_var = de_variation(variation) #распаковка строки
					if food_var==0:
					
						foodk=0
					elif food_var==1:
						
						foodk=280
					elif food_var==2:
						foodk=1000
					for room in Room.rooms:
						if room.room_number == room_number:
							cost_list.append(int(room.room_cost+foodk))
							try:
								cost_dict[int(room.room_cost+foodk)].add(variation) #ключ - цена, значение - множество вариаций по этой цене
							except KeyError:
								cost_dict[int(room.room_cost+foodk)]={variation}
						
					cost_list=list(set(cost_list))
					sorted_cost=sorted(cost_list,key=None,reverse =True)	
					#сортированный список цен вариаций
					
				#print(sorted_cost)
				
						#SORTING COST
		avaibility_set=Room.var_dict[arrival_date]
		
		
		#print(avaibility_set)
		#все вариации по этой дате
		for day1 in range(day_count):
			#print(days2date(int(arrival_date)+day),variation)

			avaibility_set&=Room.var_dict[int(arrival_date)+day1]#print(avaibility_set)
#			print("",sorted(list(avaibility_set)),"\n",sorted(list(Room.var_dict[int(arrival_date)+day1])),"\n",days2date(arrival_date))
		#print(Room.var_dict.items())
		for var_cost in sorted_cost:
				#print(var_cost)
				#print(cost_dict,var_cost)
				for variation in cost_dict[var_cost]: 
						#print(var_cost,cost_dict[var_cost])
						#каждая вариация в множестве по этой цене
						if int(var_cost*people_count) > int(money_count):
							continue
						if variation not in avaibility_set:
							# если свободен все дни
							continue
						if int(variation_people_count(variation))==int(people_count):
							#нашли номер, проверить согласие
							if randint(0,4)!=0:
									#клиент согласен			
								return variation,int(var_cost*(int(people_count)))
							else:
								return "клиент отказался",int(var_cost*(int(people_count)))
#бежим по people_count+1 со скидкой по цене
		for var_cost in sorted_cost:
			for variation in cost_dict[var_cost]: #каждая вариация в множестве по этой цене
				if int(var_cost*(int(people_count)+1)*0.7) > int(money_count):
					continue
				if variation not in avaibility_set:
					# если свободен все дни
					continue
				if int(variation_people_count(variation))==int(people_count)+1:
						
							#нашли номер, проверить согласие
					if randint(0,4)!=0:
								#клиент согласен
						return variation,int(var_cost*(int(people_count)+1)*0.7)
					else:
						return "клиент отказался",int(var_cost*(int(people_count)+1)*0.7)
		return "нет комнат",int(money_count)
					
							
						
								
						
			
	@staticmethod
	def exit(massage, book_line, room_number, room_type, count_guests, 	comfort_degree,  people_count, foodvar, revenue):
		food_list = ['без питания', 'завтрак', 'полупансион']
		food_var = food_list[int(foodvar)]
		print('--------------------------------------------------------------------------------------\nПоступила заявка на бронирование:\n')
		print(book_line + '\nНайден:\n')
		if not "нет" in massage:
			print('номер', room_number, room_type, comfort_degree, 'рассчитан на', count_guests, 'чел. фактически', people_count, 'чел.', food_var, 'стоимость', str(revenue) + '.00', 'руб./сутки\n', sep=' ')
		if "клиент" in massage:
		#count as lose @stat
		#клиент отказался от брони
			print('Клиент отказался от варианта.')
		elif "нет" in massage:
			print('Предложений по данному запросу нет. В бронировании отказано.')
		else:
			print('Клиент согласен. Номер забронирован.')
			print('\n---------------------------------------------------------------------------------------------')

	@staticmethod
	def day_exit(revenue,losses,date1):
		stats_rooms_occ={}
		summ=0
		#period=date2days(last_date)-date2days(firstdate)
	
		roomstats_t={}
		print("\n Статистика за день:",date1)
		stats_rooms_occ={"двухместный":0,"одноместный":0,"полулюкс":0,"люкс":0}
		for room in Room.rooms:
			
			if date2days(date1) in Room.room_free_date_dict[room.room_number]:
				try:
					stats_rooms_occ[room.room_type]+=1
				except KeyError:
					stats_rooms_occ[room.room_type]=1
			try:
				roomstats_t[room.room_type]+=1
			except KeyError:
				roomstats_t[room.room_type]=1
		for s in ["одноместный","двухместный","полулюкс","люкс"]:
			print("".join(("Тип номера : ",s, " из всего ",str(roomstats_t[s])," свободно ",str( stats_rooms_occ[s]))))
			summ+=stats_rooms_occ[s]
			print("Процент загруженности номеров типа: ",s," ",round((roomstats_t[s]-stats_rooms_occ[s])/roomstats_t[s]*100),"%",sep="")
		print("Выручка за день: ",revenue,"рублей")
		print("Потери за день: ",losses,"рублей")
		print("Число свободных номеров: ", summ)
		a=sum(roomstats_t.values())
		print("Из общего:",a)
		
		
		
def date2days(date1):
	'''date to days conversion'''
	d,m,y=date1.split(".")
	d,m,y=int(d),int(m),int(y)
	b=date(y,m,d)
	a=date(1,1,1)
	c=b-a
	return c.days-33
	
def days2date(days1):
	'''days to date conversion'''
	y,m,d=str(date(1,2,3)+timedelta(days=days1)).split("-")
	return "".join([d,".",m,".",y])



	'''sub class'''
class Room:
	rooms = []
	room_free_date_dict = {}
	var_dict = {}
	def __init__(self,room_number,room_type,count_guests,comfort_degree):
		self.room_number,self.room_type,self.count_guests,self.comfort_degree=room_number,room_type,count_guests,comfort_degree
		if self.room_type == 'одноместный':
			self.room_cost = 2900
		elif self.room_type == 'двухместный':
			self.room_cost = 2300
		elif self.room_type == 'полулюкс':
			self.room_cost = 3200
		else:
			self.room_cost = 4100
		if self.comfort_degree == 'стандарт_улучшенный':
			self.room_cost *= 1.2
		elif self.comfort_degree == 'апартамент':
			self.room_cost *= 1.5

	@staticmethod
	def refresh_var_dict():
		#refresh variations 
		# variation dict [date] - set of avaible rooms for the date|||| key-date, value - set of variations
		var_dict={}
		#print(date2days("01.03.2020"))
		for i in range(date2days("01.03.2020"),date2days("01.03.2020")+30):
				var_dict[i]=set()
				#print(123)
		for room,dates in Room.room_free_date_dict.items():
			#print(room,sorted(list(dates)[:5]))
			for day in dates:
				
				roomset = {int(str(room)+"0"),int(str(room)+"1"),int(str(room)+"2")}
				try:
					var_dict[day].update(roomset)
				except KeyError:
					var_dict[day] = roomset
		Room.var_dict=var_dict
		#print(5,Room.var_dict[date2days("01.03.2020")] & var_dict[date2days("01.03.2020")])
	
		return
#Main Code
#init_rooms
TotalRevenue=0
fundf=open("fund.txt","r")
for line in fundf.readlines():
	room_number,room_type,count_guests,comfort_degree=line.split()
	room_number,room_type,count_guests,comfort_degree=int(room_number),room_type,int(count_guests),comfort_degree
	Room.rooms.append(Room(room_number,room_type,count_guests,comfort_degree))
	
fundf.close()
dates=[]
#dates
f1=open("booking.txt","r")

firstdate=f1.readline().split()[0]
f1.close()
for day in range(date2days(firstdate),date2days(firstdate)+30):
	dates.append(day)
for i in range(1, len(Room.rooms) + 1):
	for day in dates:
		#fill free dates
		try:
		  Room.room_free_date_dict[i].add(day)
		except KeyError:
			Room.room_free_date_dict[i]={day}
#read booking
bookingf=open("booking.txt","r")
global last_date
last_date=bookingf.readlines()[-1].split()[0]
bookingf.close()
bookingf=open("booking.txt","r")
for line in bookingf.readlines():
	date_req,n1,n2,n3,people_count,arrival_date, day_count, money_count=line.split()
	day_count=int(day_count)
	try:
		if req_date!=date_req:
			#подвести статистику
			Hotel.day_exit(day_revenue,day_losses,req_date)
			day_losses=0
			day_revenue=0
			req_date=date_req
			
	except NameError:
		req_date=date_req
		day_revenue=0
		day_losses=0
	variation,revenue=Hotel.choice(people_count,arrival_date, day_count, money_count)
	
	
	arrival_date=date2days(arrival_date)
	
	if "клиент" in str(variation):
		#клиент отказался от брони
		day_losses+=revenue*day_count
		pass
	elif "нет" in str(variation):
		#no rooms
		day_losses+=revenue*day_count
		pass
	else:
			day_revenue+=revenue*day_count
			
			room_num,food_type=de_variation(variation)
			for day in range(int(day_count)):
					Room.room_free_date_dict[room_num]-={arrival_date+day}
			TotalRevenue+=revenue*int(day_count)
	try:
		
		room_num=int(room_num)-1
	except NameError:
		continue
		
	Hotel.exit(str(variation), line, Room.rooms[room_num].room_number, Room.rooms[room_num].room_type, Room.rooms[room_num].count_guests, Room.rooms[room_num].comfort_degree, people_count, food_type, revenue)

Hotel.day_exit(day_revenue,day_losses,req_date)
bookingf.close()
