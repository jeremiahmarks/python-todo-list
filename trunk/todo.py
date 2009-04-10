#!/usr/bin/python
import time
import datetime
import cPickle
import os
from sys import exit

class BadUserError(Exception):
    pass

def get_integer(retrieve,question,attempts=3):
    while attempts > 0:
        num = retrieve(question)
        try: # check if the user input is an integer
            return int(num)
        except ValueError:
            print "Opps, You must enter a number!"
        attempts -= 1
    raise BadUserError("Too many incorrect attempts!")

def get_info():
    print '\nYour current Todo list is: \n'
    for k, v in todo.iteritems():
        print k, v[0], v[1]
    load_todo(todo)

def add_todo():
    try:
        key = raw_input('Enter Todo Title: ')
        print '\n', key, 'has been added.'
        print 'Next, enter date for Todo: '
        curr_date = time.strftime('%Y %m %d', time.gmtime())
        print 'Format as ', curr_date
        yr = get_integer(raw_input,'\nEnter Year: ')
        mt = get_integer(raw_input,'Enter Month: ')
        dy = get_integer(raw_input, 'Enter Day: ')
        hr = get_integer(raw_input,'Enter Hour (24h): ')
        mn = get_integer(raw_input,'Enter Minute (01-59): ')
        sec = 0
        datevalue = datetime.date(yr, mt, dy)
        hourvalue = datetime.time(hr, mn, sec)
        todo[key] = datevalue, hourvalue
        load_todo(todo)
        print '\nYour current Todo list is: \n'
        for k, v in todo.iteritems():
            print k, datevalue, hourvalue
        response = raw_input('\nDo you want to add another Todo? (y/n) ')
        if response == 'y':
            add_todo()
        else:
            print 'Goodbye'
    except KeyError, e:
        print '\nError! Please enter the Todo you want to add.\n'

def load_todo(todo):
    fname = open('todo_data.dat', 'w')
    object = cPickle.Pickler(fname)
    object.dump(todo)
    fname.close()

def del_todo():
    try:
        print '\nYour current Todo list is: \n'
        for k, v in todo.iteritems():
            print k
        answer = raw_input('\nWhich Todo do you want to remove? ')
        del todo[answer]
        print '\nDeleted Todo', answer
        print '\nYour current Todo list is: \n' 
        for k, v in todo.iteritems():
            print k, v[0],v[1]
        load_todo(todo)
    except KeyError, e:
        print '\nError! Please enter the Todo to be removed.\n'
        print 'Case and spaces are important.'

def edit_todo():
    try:
        get_info()
        answer = raw_input('\nWhich Todo do you want to edit? \nEnter >> ')
        for k, v in todo.iteritems():
            key = todo[answer]
            current_date = key[0]
            print 'Current Date and Time for', answer,'\n'
            print 'Date: =', current_date
            current_time = key[1]
            print 'Time: =', current_time
            print """

    Enter D: Edit Date
    Enter T: Edit Time
            """
            new_value = raw_input('\nWhich value do you want to edit? ')
            new_value = new_value.lower()
            if new_value == 'd':
                print 'Next, enter date for Todo: '
                curr_date = time.strftime('%Y %m %d', time.gmtime())
                print 'Format as ', curr_date
                yr = get_integer(raw_input,'\nEnter Year: ')
                mt = get_integer(raw_input,'Enter Month: ')
                dy = get_integer(raw_input,'Enter Day: ')
                datevalue = datetime.date(yr, mt, dy)
                todo[answer] = datevalue, current_time
                load_todo(todo)
                print '\nYour Current Todo list is: \n'
                for k, v in todo.iteritems():
                    print k, v[0],v[1]
                response = raw_input('Do you want to edit another Todo? (y/n) ')
                response = response.lower()
                if response == 'y':
                    edit_todo()
                else:
                        menu()
            elif new_value == 't':
                hr = get_integer(raw_input,'\nEnter Hour (24h): ')
                mn = get_integer(raw_input,'Enter Minute (01-59): ')
                sec = 0
                hourvalue = datetime.time(hr, mn, sec)
                todo[answer] = current_date, hourvalue
                load_todo(todo)
                print '\nYour Current Todo list is: \n'
                for k, v in todo.iteritems():
                    print k, v[0],v[1]
                response = raw_input('Do you want to edit another Todo? (y/n) ')
                response = response.lower()
                if response == 'y':
                    edit_todo()
                else:
                    menu()
            else:
                print 'big time error'
    except KeyError, e:
        print '\nError! Please enter the Todo to be appended.\n'
        print 'Case and spaces are important.'

def menu():
    print '''
    Todo List
    
    Press I: Get Info
    Press A: Add Todo
    Press D: Remove Todo
    Press E: Edit Todo
    Press X: Exit
    '''
    answer = raw_input('\nEnter > ')
    answer = answer.lower()
    if answer == 'a':
        add_todo()
        menu()
    elif answer == 'i':
        get_info()
        menu()
    elif answer == 'd':
        del_todo()
        menu()
    elif answer == 'e':
        edit_todo()
        menu()
    elif answer == 'x':
        print 'Goodbye'
        exit()
    else:
        print 'Goodbye'

#   print k, 'Date:',vals[1],vals[2],vals[0],'Time:',vals[3],':',vals[4]
if __name__ == '__main__':
    if os.path.exists('todo_data.dat'):
        try:
            fname = open('todo_data.dat', 'rb')
            data = cPickle.Unpickler(fname)
            todo = data.load()
            load_todo(todo)
        finally:    
            fname.close()
    else:
        todo = {}
    
    menu()
