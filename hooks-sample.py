import sys
import dredd_hooks as hooks
import dredd_utils.utils as dredd_utils


stash = {}


# we want to set pre-conditions for all tests
# delete existing files that will be used for uploading
# upload files that will be used for deletion
# analyze and clean files for model training and model run


@hooks.before_all
def my_before_all_hook(transactions):
    print('before all')


@hooks.before_each
def before_each(transaction):
    transaction['skip'] = False

    if 'token' in stash:
        print('adding a token')
    else:
        print('Obtaining token')
        print('calling util method')
        stash['token'] = dredd_utils.obtain_token(stash)

    try:
        print('Adding bearer token to', transaction['name'] )
        transaction['request']['headers']['Authorization'] = stash['token']
    except:
        print('Ignore error')

# AUTH ####
## argument inside @hooks.before is the route
## set the request body inside the function

@hooks.before("auth > AUTH > Login as a user > 201")
def setUserNameGood(transaction):
    transaction['request']['body'] = "username=nward&pass1=nw4rd!"
    print('before login 201')

@hooks.before("auth > AUTH > Login as a user > 400")
def setUserNameNone(transaction):
    transaction['request']['body'] = 'pass1=dr3dd!'
    print('before login 400')

@hooks.before("auth > AUTH > Login as a user > 401")
def setBadPassword(transaction):
    transaction['request']['body'] = 'username=cluu&pass1=bad'
    print('before login 401')

@hooks.after_each
def my_after_each(transaction):
    print('after_each')


@hooks.after_all
def my_after_all_hook(transactions):
    print('after_all')
