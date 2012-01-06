from django.db import models


class Locations(models.Model):
	trial_id = models.CharField(max_length=12)
	facility = models.CharField(max_length=200)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zip = models.CharField(max_length=11)
	country = models.CharField(max_length=100)

        def __unicode__(self):
                return self.facility

class Keyword(models.Model):
	trial_id = models.CharField(max_length=12)
	keyword = models.CharField(max_length=200)	
        
        def __unicode__(self):
                return self.keyword

class Conditions(models.Model):
    trial_id = models.CharField(max_length=12)
    keyword = models.CharField(max_length=200)	
        
    def __unicode__(self):
        return self.keyword

class Mesh_key(models.Model):
        trial_id = models.CharField(max_length=12)
        keyword = models.CharField(max_length=200)       
        
        def __unicode__(self):
                return self.keyword

class Criteria(models.Model):                
    trial_id =models.CharField(max_length=12)
    gender = models.CharField(max_length=50)
    minimum_age = models.PositiveIntegerField()
    maximum_age = models.PositiveIntegerField()
    healthy_volunteers = models.CharField(max_length=100)
    textblock = models.CharField(max_length=1000)    
    
    def __unicode__(self):
        return self.trial_id

class Contact(models.Model):
    trial_id = models.CharField(max_length=12)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    email = models.EmailField(max_length=70)
        
    def __unicode__(self):
        return self.last_name

class Trial(models.Model):
	trial_id = models.CharField(primary_key=True, max_length=12)
	brief_title = models.TextField(max_length=500)
	official_title = models.TextField(max_length=500)
	brief_summary = models.TextField(max_length=500)
	detailed_Description = models.TextField(max_length=1000)
	overall_Status = models.CharField(max_length=100)
	phase = models.CharField(max_length=100)
	enrollment = models.TextField(max_length=500)
	study_type = models.CharField(max_length=500)
	condition = models.ManyToManyField(Conditions)
	elligibility = models.TextField(max_length=500)
        criteria = models.ManyToManyField(Criteria)
        overall_contact = models.ForeignKey(Contact)
        location = models.ManyToManyField(Locations)
	lastchanged_date = models.DateField()
	firstreceived_date = models.DateField()
	keyword = models.ManyToManyField(Keyword)
	condition_mesh = models.ManyToManyField(Mesh_key)
        
        def get_absolute_url(self):
            return "/trial/%s" % self.trial_id

        def __unicode__(self):
                return self.brief_title
        

class Patient(models.Model):

	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
	)

	email =models.EmailField(max_length=75)
	age = models.PositiveIntegerField()
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	condition = models.CharField(max_length=50)
	can_contact = models.BooleanField()
        first_name = models.CharField(max_length=25)
        last_name = models.CharField(max_length=25)
        
        def __unicode__(self):
                return u'%s %s %s' % (self.condition, self.first_name, self.last_name)


class Email(models.Model):
    email = models.EmailField(max_length=75)

    def __unicode__(self):
        return self.email

class Notification(models.Model):
    condition = models.TextField(max_length=250)
    email = models.ManyToManyField(Email) 
