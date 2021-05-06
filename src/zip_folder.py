#!/usr/bin/env python
import sys, os, datetime
import getpass
import zipfile

import yaml
from getmac import get_mac_address as gma


def write_data_in_file(file_name, bits_id):
    os.setxattr(file_name, 'user.author', bytes(getpass.getuser(), 'utf-8'))
    os.setxattr(file_name, 'user.mac_address', bytes(gma(), 'utf-8'))
    os.setxattr(file_name, 'user.bits_id', bytes(bits_id, 'utf-8'))
    os.setxattr(file_name, 'user.created_at', bytes(datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S'), 'utf-8'))


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                       os.path.join(path, '..')))

def select_file():
    files = os.listdir()
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
    zipf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(folder_name, zipf)
    zipf.close()
    write_data_in_file(zip_file_name, bits_id)
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
        try:
            user_details = {
                'author': os.getxattr(file_name,'user.author').decode('utf-8'),
                'mac_address': os.getxattr(file_name,'user.mac_address').decode('utf-8'),
                    'bits_id': os.getxattr(file_name,'user.bits_id').decode('utf-8'),
                'created_at': os.getxattr(file_name,'user.created_at').decode('utf-8')
            }
        except OSError:
            print("The zipfile wasn't created using this package.")
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(file_name.split('.')[0])
        print('\nThe zip file has been extracted to current directory and original zip file has been deleted.\n')
        print('Below our user details for the submission:-')
        print(yaml.dump(user_details, default_flow_style=False))
        os.remove(file_name)
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
