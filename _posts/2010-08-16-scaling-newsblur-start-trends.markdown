---
layout: post
title: 'Scaling NewsBlur: Start with trends'
date: '2010-08-16T17:59:57+00:00'

---
    #!sql
    SELECT num_subscribers, COUNT(*) 
    FROM feeds 
    GROUP BY num_subscribers 
    ORDER BY num_subscribers ASC;
