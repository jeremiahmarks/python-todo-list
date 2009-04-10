#!/usr/bin/python
import time
import datetime
import cPickle
import os
from sys import exit

class BadUserError(Exception):
    pass

def get_integer(retrieve,question,attempts=3):
    """Test for integer input, three attempts allowed"""
    while attempts > 0:
        num = retrieve(question)
        try: 
            return int(num)
        except ValueError:
            print "Opps, You must enter a number!"
        attempts -= 1
    raise BadUserError("Too many incorrect attempts!")

def main():
    """Starts the program, loads data from disk, prints current todo's"""
    print '\nYour current Todo list is: \n'
    if os.path.exists('todo.dat'):
        try:
            fname = open('todo.dat', 'rb')
            data = cPickle.Unpickler(fname)
            todo = data.load()
            save_todo(todo)
            for k, v in todo.iteritems():
                print k, v[0], v[1]
        finally:    
            fname.close()
            menu()
    else:
        todo = {}
        menu()

def add_todo():
    """Add a todo to the todo list"""
    if os.path.exists('todo.dat'):
        try:
            fname = open('todo.dat', 'rb')
            data = cPickle.Unpickler(fname)
            todo = data.load()
            save_todo(todo)
        finally:    
            fname.close()
    else:
        todo = {}
    
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
        save_todo(todo)
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

def save_todo(todo):
    """Save todo list to disk"""
    fname = open('todo.dat', 'w')
    object = cPickle.Pickler(fname)
    object.dump(todo)
    fname.close()

def del_todo():
    """Delete a todo"""
    if os.path.exists('todo.dat'):
        try:
            fname = open('todo.dat', 'rb')
            data = cPickle.Unpickler(fname)
            todo = data.load()
            save_todo(todo)
        finally:    
            fname.close()
    else:
        todo = {}

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
        save_todo(todo)
    except KeyError, e:
        print '\nError! Please enter the Todo to be removed.\n'
        print 'Case and spaces are important.'

def edit_todo():
    """Edit the date and time for a todo"""
    if os.path.exists('todo.dat'):
        try:
            fname = open('todo.dat', 'rb')
            data = cPickle.Unpickler(fname)
            todo = data.load()
            save_todo(todo)
        finally:    
            fname.close()
    else:
        todo = {}
    
    try:
        for k, v in todo.iteritems():
            print k, v[0], v[1]
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
                save_todo(todo)
                print '\nYour Current Todo list is: \n'
                for k, v in todo.iteritems():
                    print k, v[0],v[1]
                response = raw_input('\nDo you want to edit another Todo? (y/n) ')
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
                save_todo(todo)
                print '\nYour Current Todo list is: \n'
                for k, v in todo.iteritems():
                    print k, v[0],v[1]
                response = raw_input('\nDo you want to edit another Todo? (y/n) ')
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
        main()
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

if __name__ == '__main__':
    main()
