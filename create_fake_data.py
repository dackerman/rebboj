from models import Company
from models import Rating
from models import Review

# Create some companies
company1 = Company(name='Google',urlname='google')
company2 = Company(name='Jobber',urlname='jobber')
company1.put()
company2.put()

#Create some ratings
rating1 = Rating(overall=4,salary=3,benefits=4,growth=5,peers=4,environment=5,location=5)
rating2 = Rating(overall=5,salary=3,benefits=3,growth=4,peers=5,environment=5,location=4)
rating1.put()
rating2.put()

#Create some reviews
review1 = Review(company=company1,text='Google is amazing!',rating=rating1)
review2 = Review(company=company2,text='Jobber is a wonderful start-up to work for!',rating=rating2)
review1.put()
review2.put()
