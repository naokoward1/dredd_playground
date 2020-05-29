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

@hooks.before("upload > /v1/upload/{dataset_name} > Delete a dataset > 404")
def deleteDS(transaction):
    invalidDS = '/v1/upload/another_ds_name.csv'
    transaction['request']['uri'] = invalidDS
    transaction['fullPath'] = invalidDS
    print('Delete a dataset > 404')

@hooks.after("auth > AUTH > Login as a user > 201")
def clearBearerToken(transaction):
    print('after')
    del stash['token']

# UPLOADFILE ####
@hooks.before("upload > UPLOADFILE > Upload a dataset > 201")
# check to ensure file does not exist on server
# if exists, delete the file
def uploadFile(transaction):
    print("before upload file")
    print(transaction['request'])
    datasetFile = 'samples/cancer_train.csv'
    testFileName = 'dredd_upload.csv'
    dredd_utils.delete_file(stash['token'], testFileName)
    text = None
    with open(datasetFile, 'r', encoding='utf8') as f:
        text = f.read()

    body = "--BOUNDARY\r\n"
    body += 'content-Disposition: form-data; name="dataset"; filename="' + testFileName + '"\r\n'
    body += 'Content-Type: text/csv\r\n'
    body += text
    body += '\r\n'
    body += '--BOUNDARY\r\n'
    body += 'Content-Disposition: form-data; name="dataset_name"\r\n'
    body += '\r\n' + testFileName + '\r\n'
    body += '--BOUNDARY\r\n'
    body += 'Content-Disposition: form-data; name="has_header"\r\n'
    body += '\r\n'
    body += 'true'
    body += '\r\n'
    body += '--BOUNDARY--'

    transaction['request']['body'] = body

@hooks.before_each_validation
def my_before_each_validation_hook(transaction):
    print('before each validation')


@hooks.before_validation
def my_before_validation_hook(transaction):
    print('before validations')


@hooks.after
def my_after_hook(transaction):
    print('after')


@hooks.after_each
def my_after_each(transaction):
    print('after_each')


@hooks.after_all
def my_after_all_hook(transactions):
    print('after_all')
