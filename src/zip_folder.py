#!/usr/bin/env python
import sys, os, datetime
import getpass
import zipfile
import pickle
import json

from getmac import get_mac_address as gma


# Support for Python2
try:
    input = raw_input
except NameError:
    pass


def write_data_in_file(bits_id, zipf):
    info = {
        'author': getpass.getuser(),
        'mac_address': gma(),
        'bits_id': bits_id,
        'created_at': datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S')
    }
    file_name = 'tmp.pkl'
    with open(file_name, 'wb') as handle:
        pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)
    zipf.write(file_name)
    os.remove(file_name)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                       os.path.join(path, '..')))

def select_file():
    files = os.listdir('.')
    file_number = 0
    for file_name in files:
        file_number += 1
        print(str(file_number)+') '+file_name)
    file_name = files[int(input('Please enter the key corresponding to your submission file (or folder) name: '))-1]
    return file_name


def zip_folder():
    print('\nIt is assumed you are in the parent directory of the submission file (or folder) to be zipped\n')
    folder_name = select_file()
    if not os.path.exists(folder_name):
        print('No file with this name exists')
        exit()
    bits_id = input('Enter your BITS ID: ')
    task_number = input('Enter the integer task number: ')
    zip_file_name = bits_id+'_task'+task_number+'.zip'
    zipf = zipfile.ZipFile(zip_file_name, 'a', zipfile.ZIP_DEFLATED)
    zipdir(folder_name, zipf)
    write_data_in_file(bits_id, zipf)
    zipf.close()
    print('Please submit the zip file '+zip_file_name)

def unzip_file():
    vr_password = '123d1qwdxb*#@&GEuibBX&DQWG&D#VBW(dqbd8&QBAXD(*BW@#'
    password = input('Enter the admin password: ')
    if password == vr_password:
        # To get back the metadata
        file_name = select_file()
        if not os.path.exists(file_name):
            print('No file with this name exists')
            exit()
        folder_name = file_name.split('.')[0]
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(folder_name)
        try:
            with open(folder_name+'/tmp.pkl', 'rb') as handle:
                user_details = pickle.load(handle)
                info_file = open(folder_name+'/user_submission_details.txt', 'wt')
                info_file.write(str(user_details))
                info_file.close()
                print('Below are the user details for the submission:-')
                print(json.dumps(user_details, indent=4))
        except Exception as e:
            print("The zipfile wasn't created using this package.\n"+str(e))
        print('\nThe zip file has been extracted to current directory and original zip file has been deleted.\n')
        os.remove(file_name)
        os.remove(folder_name+'/tmp.pkl')
        exit()
    else:
        print('Imposter spotted!')
        exit()


def main():
    # unzip the files
    if len(sys.argv)>1:
        if sys.argv[1] ==  'RoboconEasterEgg':
            unzip_file()
    zip_folder()
