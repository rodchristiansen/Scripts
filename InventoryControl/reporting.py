#!/usr/bin/python

import csv
import subprocess
import plistlib
import sys
import urllib2

CSV_LOCATION = 'http://server.edu.ca/imaging/inventory/reporting.csv'
CSV = urllib2.urlopen(CSV_LOCATION)

def get_hardware_info():
    '''Uses system profiler to get hardware info for this machine'''
    cmd = ['/usr/sbin/system_profiler', 'SPHardwareDataType', '-xml']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # system_profiler xml is an array
        sp_dict = plist[0]
        items = sp_dict['_items']
        sp_hardware_dict = items[0]
        return sp_hardware_dict
    except Exception:
        return {}

def check_compname(serial_number):
    csv_data = csv.DictReader(CSV, delimiter=',')
    for row in csv_data:
        serial = row['serial']
        computername = row['name']
        cohort_tag = row['cohort']
        dept_tag = row['dept']
        room_tag = row['room']
        asset_tag = row['asset']
        if serial == serial_number:
            set_sharingname(computername)
            set_hostname(computername)
            set_localhostname(computername)
            set_cohort_tag(cohort_tag)
            set_dept_tag(dept_tag)
            set_room_tag(room_tag)
            set_asset_tag(asset_tag)

def get_serial_number():
    hardware_info = get_hardware_info()
    return hardware_info.get('serial_number', 'UNKNOWN') 

def set_sharingname(computername):
    cmd = ['sudo', '/usr/sbin/scutil', '--set', 'ComputerName', computername]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_hostname(computername):
    cmd = ['sudo', '/usr/sbin/scutil', '--set', 'HostName', computername]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_localhostname(computername):
    cmd = ['sudo', '/usr/sbin/scutil', '--set', 'LocalHostName', computername]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_cohort_tag(cohort_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text1', '-string', cohort_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_dept_tag(dept_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text2', '-string', dept_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_room_tag(room_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text3', '-string', room_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_asset_tag(asset_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text4', '-string', asset_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def main():
    serial_number = get_serial_number()
    check_compname(serial_number)

if __name__ == '__main__':
    main()
