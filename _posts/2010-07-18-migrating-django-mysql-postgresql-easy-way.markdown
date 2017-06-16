---
layout: post
title: Migrating Django from MySQL to PostgreSQL the Easy Way
date: '2010-07-18T16:43:20+00:00'

---
I recently moved NewsBlur from MySQL to PostgreSQL for a variety of reasons, but most of all I want to use connection pooling and database replication using Slony, and Postgres has a great track record and community. But all of my data was stored in MySQL and there is no super easy way to move from one database backend to another.

Luckily, since I was using the Django ORM, and with Django 1.2's multi-db support, I can use Django's serializers to move the data from MySQL's format into JSON and then back into Postgres. 

Unfortunately, If I were to use the command line, every single row of my models has to be loaded into memory. Issuing commands like this:

    #!python
    python manage.py dumpdata --natural --indent=4 feeds > feeds.json

would take a long, long time, and it wouldn't even work since I don't have even close to  enough memory to make that work. 

Luckily, the dumpdata and loaddata management commands are actually just wrappers on the internal serializers in Django. I decided to iterate through my models and grab 500 rows at a time, serialize them and then immediately de-serialize them (so Django could move from database to database without complaining).

    #!python
    import sys
    from django.core import serializers
    
    def migrate(model, size=500, start=0):
        count = model.objects.using('mysql').count()
        print "%s objects in model %s" % (count, model)
        for i in range(start, count, size):
            print i,
            sys.stdout.flush()
            original_data =  model.objects.using('mysql').all()[i:i+size]
            original_data_json = serializers.serialize("json", original_data)
            new_data = serializers.deserialize("json", original_data_json, 
                                               using='default')
            for n in new_data:
                n.save(using='default')
    
    migrate(Feed)

This assume that you have both databases setup in your `settings.py` like so:

    #!python
    DATABASES = {
        'mysql': {
            'NAME': 'newsblur',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'newsblur',
            'PASSWORD': '',
        },
        'default': {
            'NAME': 'newsblur',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'newsblur',
            'PASSWORD': '',
        }
    }

*Note that I changed my default database to the Postgres database, because otherwise some management commands would still try to run on the default MySQL database. This is probably resolved and I didn't do something right, but when I migrated, I changed Postgres to be the default database.*

I just run the short script in the Django console and wait however long it takes. This script prints out which set it's working on, so you can at least track the progress, which might take a long, long time, but is much less prone to crashing like dumpdata and loaddata.

A word of warning to those with large datasets. Instead of iterating straight through the table, see if you have a handier index already built on the table. I have a table with a million rows, but there are a few indices which can quickly find stories throughout the table, rather than having to order and offset the entire table by primary key. Adapt the following code to suit your needs, but notice that I use an index on the Feed column in the Story table. 

    #!python
    import sys
    from django.core import serializers

    def migrate_with_model(primary_model, secondary_model, offset=0):
        secondary_model_data = secondary_model.objects.using('mysql').all()
        for i, feed in enumerate(secondary_model_data[offset:].iterator()):
            stories = primary_model.objects.using('mysql').filter(story_feed=feed)
            print "[%s] %s: %s stories" % (i, feed, stories.count())
            sys.stdout.flush()
            original_data = serializers.serialize("json", stories)
            new_data = serializers.deserialize("json", original_data, 
                                               using='default')
            for n in new_data:
                n.save(using='default')

    migrate_with_model(primary_model=Story, secondary_model=Feed)

This makes it much faster, since I only have to sort a few hundreds records rather than the entire Story table and its million rows.

Also of note is that while all of the data made it into the Postgres tables, the sequences (counts) were all off. Many were at 0. To remedy this easily, just use the count of the table itself and store it in the sequence table, like so:

    #!sql
    select setval('rss_feeds_tag_id_seq', max(id)) from rss_feeds_tag;
    select setval('analyzer_classifierauthor_id_seq', max(id)) from analyzer_classifierauthor;            
    select setval('analyzer_classifierfeed_id_seq', max(id)) from analyzer_classifierfeed;              
    select setval('analyzer_classifiertag_id_seq', max(id)) from analyzer_classifiertag;               
    select setval('analyzer_classifiertitle_id_seq', max(id)) from analyzer_classifiertitle;             
    select setval('analyzer_featurecategory_id_seq', max(id)) from analyzer_featurecategory;

I just made a quick text macro on the table names. This quickly set all of the sequences to their correct amounts.

<i>This post has been translated to <a href="http://www.webhostinghub.com/support/es/misc/migracion-de-django-de-mysql">Spanish</a> by  <a href="http://www.webhostinghub.com/support/edu">Maria Ramos</a>.</i>
