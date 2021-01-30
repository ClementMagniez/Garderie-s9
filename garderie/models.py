from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from datetime import datetime, timedelta, date, time
from math import ceil, floor
import garderie.utils 

	
# Managers

class ScheduleManager(models.Manager):

	# Schedules incomplets, sans départ encore déterminé
	def incomplete_schedules(self):
		return super().get_queryset().filter(departure=None)

	# Schedules ayant commencé il y a moins de 30 jours		
	def recent_schedules(self):
		return super().get_queryset().filter(arrival__gte=datetime.today()-timedelta(days=30))



### Modèles

class Parent(models.Model):
	uid=models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	phone=models.CharField(max_length=20, null=True, verbose_name="Téléphone")


	def __str__(self):
		return self.uid.first_name+" "+self.uid.last_name
			
	def fullname(self):
		return str(self)			


	# Queryset fusionnant child_set et child_set2 TODO les fusionner automatiquement ?
	def all_children(self):
		return self.child_set.all() | self.child_set2.all()

class Child(models.Model):
	parent=models.ForeignKey(Parent, on_delete=models.DO_NOTHING, related_name='child_set')
	first_name=models.CharField(max_length=100, verbose_name="Prénom")
	last_name=models.CharField(max_length=100, verbose_name="Nom")
	second_parent=models.ForeignKey(Parent, on_delete=models.DO_NOTHING, related_name='child_set2', null=True)


	def __str__(self):
		return self.first_name+" "+self.last_name
		
	### Méthodes de manipulation du modèle

	def fullname(self):
		return str(self)	

	# Renvoie un schedule incomplet (departure==None) de l'enfant ou None
	def incomplete_schedule(self):
		for schedule in self.schedule_set.all():
			if schedule.departure==None:
				return schedule
		
	# Schedules ayant commencé il y a moins de 30 jours		
	def recent_schedules(self):
		return self.schedule_set.filter(arrival__gte=datetime.today()-timedelta(days=30))

	# Bill du mois courant, None s'il n'y en a pas
	def last_bill(self):
		today=timezone.now()
		bills=self.bill_set.filter(year=today.year, month=today.month)
			
		return bills[0] if bills else None


	# Renvoie un tuple (datetime, ExpectedPresence) décrivant l'ExpectedPresence la plus proche
	def next_presence(self):
		all_occurrences=[presence.next_occurrence() for presence in self.expectedpresence_set.all()]
		# compare des tuples : on sait cependant que le premier item du tuple (un datetime)
		# sera unique (puisque basé sur un ExpectedPresence unique), on ne sera donc pas amené à
		# comparer des ExpectedPresence 
		# la comparaison se fait donc strictement sur les datetimes 
		if all_occurrences:
			return min(all_occurrences)
		else:
			return None
	
	# Renvoie true si l'enfant sera présent dans le créneau matin/soir suivant
	def present_next_time(self):
		next=self.next_presence()
		today=timezone.now()
		if next:
			return next[0].day==today.day and next[1].hour_arrival<today.hour and next[1].hour_departure>today.hour
		else:
			return False
	# Renvoie true si l'enfant a été présent (puis est parti) dans le créneau courant	
		
	# Return un Schedule incomplet selon incomplete_schedule ; s'il n'y en a pas mais was_here est True,
	# return le dernier Schedule complet ; si was_here est False, return None
	def schedule_to_display(self):
		res=self.incomplete_schedule()
		if not res:
			if self.was_here():
				return self.schedule_set.latest('id')
			return None
		return res
		
	# Renvoie un tuple des deux parents de l'enfant
	def parents(self):
		second_parent_uid=self.second_parent.uid if self.second_parent else None
		return (self.parent.uid, second_parent_uid)
	

	# True si l'enfant est parti il y a moins de 3h
	def was_here(self):
		today=timezone.now()
		for schedule in self.schedule_set.all():
			if schedule.departure+timedelta(hours=3)>today:
				return True
		return False

	# True si l'enfnat a été présent au Date ou Datetime renseigné
	# Différent de was_here qui check précisément un créneau de la journée actuelle
	def was_here_this_day(day):
		for schedule in self.schedule_set.all():
			if schedule.was_this_day():
				return True
		return False


class HourlyRate(models.Model):
	value=models.FloatField(verbose_name="Taux à la demi-heure (en €)")
	date_start=models.DateTimeField("Date de départ")
	date_end=models.DateTimeField("Date de fin", null=True)
		
		
class Bill(models.Model):

	MONTH=[(m, ugettext(date(1900, m, 1).strftime('%B')).capitalize())  for m in range(1,13)]
	YEAR=[(y, date(y, 1,1).strftime('Y')) for y in range(2000,timezone.now().year+1)]


	child=models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name="Enfant associé")
	month=models.IntegerField(choices=MONTH, default=timezone.now().month, verbose_name="Mois")
	year=models.IntegerField(choices=YEAR, default=timezone.now().year, verbose_name="Année")
			
	### Méthodes de manipulation du modèle

	# Renvoie la somme des Schedules associés à self
	@property
	def amount(self):
		return sum([x.calc_amount() for x in self.schedule_set.all()])          
		
class Schedule(models.Model):
	child=models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name="Enfant")
	rate=models.ForeignKey(HourlyRate, on_delete=models.CASCADE, null=True)
	arrival=models.DateTimeField('Heure d\'arrivée')
	departure=models.DateTimeField('Heure de départ', null=True)
	bill=models.ForeignKey(Bill, null=True, on_delete=models.DO_NOTHING)

	objects=ScheduleManager()

	def __str__(self):
		return str(self.arrival)+" -- "+str(self.departure)
		
	# Automatise l'association du Schedule à un Bill à la création selon utils.get_or_create_bill
	def save(self, *args, **kwargs):
		old=Schedule.objects.filter(id=getattr(self,'id',None)).first()
		if not old:
			bill=garderie.utils.get_or_create_bill(self)
			self.bill=bill
		super().save()	

	### Méthodes de manipulation du modèle
	
	# Renvoie True si le schedule n'a pas encore de départ, False sinon
	def incomplete(self):
		return self.departure==None

	# Renvoie un int arrival arrondi à la demi-heure inférieure
	# par rapport à l'heure réelle
	def rounded_arrival(self):
		temp_arrival=self.arrival
		arrival_minute=floor(self.arrival.minute/30)*30
		temp_arrival=self.arrival.replace(minute=arrival_minute)
		return temp_arrival

	# Renvoie un int departure arrondi à la demi-heure supérieure
	# par rapport à l'heure réelle
	def rounded_departure(self):
		if not self.departure: # peut arriver si l'enfant est actuellement présent
			return None
		temp_departure=self.departure				
		# Logique en cas où on arrondit à 60 : Datetime.minute accepte [0..59] 		
		departure_minute=ceil(self.departure.minute/30)*30
		departure_hour=self.departure.hour
		if departure_minute==60:
			departure_minute=0
			departure_hour+=1

		if departure_hour==24:
			departure_hour-=1 

		# Théoriquement, hour peut alors passer à 24 (cas où le départ a lieu entre 23:30 et 0:00),
		# forçant à incrémenter le jour, pouvant amener à incrémenter le mois, 
		# pouvant amener à incrémenter l'année
		# On considère que ce scénario ne peut arriver en situation normale et on 
		# l'ignore complètement

		temp_departure=self.departure.replace(hour=departure_hour, minute=departure_minute)
		return temp_departure
		
	# Renvoie un tuple d'int (arrival, departure) ; voir Schedule#rounded_arrival
	# et Schedule#rounded_departure
	# Exemple : si le Schedule enregisre arrival=7:03 et departure=8:34, 
	# rounded_arrival_departure renverra (7:00, 8:30) 
	def rounded_arrival_departure(self):
		return (self.rounded_arrival(), self.rounded_departure())	
	
	# Return le coût d'un schedule 
	def calc_amount(self):
		if not self.departure:
			return 0
		arrival, departure=self.rounded_arrival_departure()
		duration=(departure-arrival).seconds/1800 # calcul à la demi-heure	
		return round(duration*self.rate.value)	# round pour éliminer les millisecondes inutiles et avoir un int
	
	# True si le Schedule a eu lieu au Date ou Datetime renseigné
	def was_this_day(date):		
		return this.arrival.day==date.day
	
	
class ExpectedPresence(models.Model):
	DAY=[(d, ugettext(date(1900, 1,d).strftime('%A')).capitalize()) for d in range(1,8)]
	PERIOD=[(m, ['Matin', 'Soir'][m]) for m in range(0,2)] 
	
	child=models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name="Enfant associé")
	day=models.IntegerField(choices=DAY, default=timezone.now().weekday(), verbose_name="Jour")
	period=models.IntegerField(choices=PERIOD, default='Matin', verbose_name='Heure de présence')

	# Deux propriétés pour permettre à ExpectedPresence d'émuler un Schedule : attribuent
	# une heure de départ et d'arrive selon self.period
	@property
	def hour_arrival(self):
		return 0 if self.period==0 else 12
	
	@property
	def hour_departure(self):
		return 12 if self.period==0 else 20

	# Renvoie un tuple (datetime, self)
	# Exemple d'utilisation : si self.day==0 (lundi) et self.period=='Soir',
	# appeler self.next_occurrence() le jeudi 21/01/21 renverra le lundi soir suivant, 
	# donc un datetime (2021, 01, 25, 18, 0,0) 
	def next_occurrence(self):
		today=timezone.now()
		today_occurrence=today.replace(hour=self.hour_departure, minute=0, second=0) # standardisation de la période
		
		# weekday() compte de 0 à 6, mais self.day de 1 à 7, donc +1
		true_selfday=self.day-1
		# si ce jour de la semaine est passée, on cherche la semaine suivante, sinon 
		# celle-ci, donc 7 ou 0
		week_determiner=7 if (today_occurrence.hour<=today.hour and today.weekday()==true_selfday) or today.weekday()>true_selfday else 0
		return (today_occurrence+timedelta(days=(-today_occurrence.weekday())+true_selfday+week_determiner), self)
		

	def __str__(self):
		return self.get_day_display() + ' ' + self.get_period_display().lower()

# Personne de confiance : pas responsable légal d'un enfant, mais susceptible 
# d'aller le chercher et devant donc être connu	du système
# N'interagit pas directement avec le système
class ReliablePerson(models.Model):
	child=models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name='Enfant concerné')
	first_name=models.CharField(max_length=100, verbose_name="Prénom")
	last_name=models.CharField(max_length=100, verbose_name="Nom")
	phone=models.CharField(max_length=20, null=True, verbose_name="Téléphone") 		


	def __str__(self):
		return self.first_name+" "+self.last_name

	def fullname(self):
		return str(self)	

	
