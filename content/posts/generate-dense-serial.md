date: 2013-09-29
slug: generate-dense-id
title: Generate deterministic ID in a django 1.5 Model
tags: django, postgresql, db

OK, let's talk about a thing that *seems* trivial & obvious, but unfortunately it is not.

Assume that we wfdfdfdffant that when we insert objects, those objects has to have an
unique, progressigggggve and dense integer as ID.

A thing like that:

    # models.py
    from django.db import models

	class Customer(models.Model):
	    [..]

    c1 = Customer.objects.create()
    c2 = Customer.objects.create()
    c3 = Customer.objects.create()

    c1.serial
    > 1
    c2.serial
    > 2
    c3.serial
    > 3

Well, someone (me too, though) would say that is there also a field that does this behaviour,
in django core: ```AutoField```, that is the type of the implicit ```id``` attribute,
default primary key of any Model.

*Wrong.*

Turns out that ```AutoField``` doesn't do anything django-side but instead asks (at the saving time)
at the DBMS for a generated ID or something as reported also [here][1].
The consequence is that what the DBMS may return isn't guaranteed **at all**
densely progressive.

That is a DBMS related thing that has to do with concurrence and perfomance
avoiding gapless sequence.

![](/static/images/race-condition.jpg "Race condition")

Clearly when an object is saved is generated a race-conditions between
the django "agents" (threads, different processes, different processes on different machines and so on) that possibly
could want to save another object at the same time. Of course, django and so the DBMS
has to manage that sort of thing and possibly in a perfomant manner.
So instead of locking anything the DBMS prefers to skip some number that have the risks (timely-related risks)
of a race-conditions

    c1 = Customer.objects.create() # t0 time
    c2 = Customer.objects.create() # t1 time
    c3 = Customer.objects.create() # t1` time

    c1.id
    > 1
    c2.id
    > 3
    c3.id
    > 4

Clearly also in that scenario it **maybe** could want to skip 2 as number and take 3 and 4.
Don't fraintend me, this is a great choice of work, the world needs perfomances.

> But what if do you need a deterministic progressive id?

So I've solved that issue using an auxiliary model 'Counter' which holds, locks and increments a row.

	# models.py
    from django.db import models, transaction

	class Counter(models.Model):
		name = models.CharField(max_length=40, unique=True, db_index=True)
		n = models.PositiveIntegerField(default=1)

	class Customer(models.Model):
		def save(self, *args, **kwargs):
			super(Customer, self).save(*args, **kwargs)

			if self.cod == '':
				with transaction.commit_on_success():
					try:
						counter = Counter.objects.select_for_update().get(name='Customer')
					except Counter.DoesNotExist:
						counter = Counter.objects.select_for_update().create(name='Customer')
					self.cod = "CUST%d" % counter.n
					counter.n += 1
					counter.save()
				super(Customer, self).save(*args, **kwargs)

note that `select_for_update()` is what locks the row (but pay attention on the DBMS used)
until the transaction doesn't terminate.

I think that the above is a good and simple way to achieve that sort of thing.

Hope this helps

[1]: http://grokbase.com/t/postgresql/pgsql-general/0877x998fr/creating-a-perfect-sequence-column