Simple logging module for lazy people like me who doesn't feel like reading
the documentation for python's official logging module.

Example usage:

helge@helge:~/annet/loglady$ ls
loglady.py  MIT-LICENCE.txt  README.txt
helge@helge:~/annet/loglady$ mkdir logs
helge@helge:~/annet/loglady$ python
Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39)
[GCC 4.4.5] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import loglady
>>> logger = loglady.LogLady('./logs', ('test', 'foo'))
>>> logger.test('this is a test message')
>>> logger.foo('oh no!')
>>> logger.foo('oh yes!')
>>> quit()
helge@helge:~/annet/loglady$ ls -l logs/
total 12
-rw-r--r-- 1 helge helge 128 2010-11-08 23:34 all.log
-rw-r--r-- 1 helge helge  75 2010-11-08 23:34 foo.log
-rw-r--r-- 1 helge helge  53 2010-11-08 23:33 test.log
helge@helge:~/annet/loglady$ cat logs/foo.log
[2010-11-08 23:34:01] [ foo]: oh no!
[2010-11-08 23:34:03] [ foo]: oh yes!
helge@helge:~/annet/loglady$ cat logs/test.log
[2010-11-08 23:33:56] [test]: this is a test message
helge@helge:~/annet/loglady$ cat logs/all.log
[2010-11-08 23:33:56] [test]: this is a test message
[2010-11-08 23:34:01] [ foo]: oh no!
[2010-11-08 23:34:03] [ foo]: oh yes!
