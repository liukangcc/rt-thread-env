# -*- coding:utf-8 -*-
#
# File      : archive.py
# This file is part of RT-Thread RTOS
# COPYRIGHT (C) 2006 - 2018, RT-Thread Development Team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Change Logs:
# Date           Author          Notes
# 2018-5-28      SummerGift      Add copyright information
#

import tarfile
import zipfile
import os
import pkgsdb
import platform
import shutil


def unpack(archive_fn, path, pkg, pkgs_name_in_json):
    pkg_ver = pkg['ver']
    flag = True

    iswindows = False

    if platform.system() == "Windows":
        iswindows = True

    if ".tar.bz2" in archive_fn:
        arch = tarfile.open(archive_fn, "r:bz2")
        for tarinfo in arch:
            arch.extract(tarinfo, path)
            a = tarinfo.name
            if not os.path.isdir(os.path.join(path, a)):
                if iswindows:
                    right_path = a.replace('/', '\\')
                else:
                    right_path = a
                a = os.path.join(os.path.split(right_path)[0], os.path.split(right_path)[1])
                pkgsdb.savetodb(a, archive_fn)
        arch.close()

    if ".tar.gz" in archive_fn:
        arch = tarfile.open(archive_fn, "r:gz")
        for tarinfo in arch:
            arch.extract(tarinfo, path)
            a = tarinfo.name
            if not os.path.isdir(os.path.join(path, a)):
                if iswindows:
                    right_path = a.replace('/', '\\')
                else:
                    right_path = a
                a = os.path.join(os.path.split(right_path)[0], os.path.split(right_path)[1])
                pkgsdb.savetodb(a, archive_fn)
        arch.close()

    if ".zip" in archive_fn:
        arch = zipfile.ZipFile(archive_fn, "r")
        for item in arch.namelist():
            arch.extract(item, path)
            if not os.path.isdir(os.path.join(path, item)):
                if iswindows:
                    right_path = item.replace('/', '\\')
                else:
                    right_path = item

                # Gets the folder name and change_dirname only once
                if flag:
                    dir_name = os.path.split(right_path)[0]
                    change_dirname = pkgs_name_in_json + '-' + pkg_ver
                    flag = False
    
                right_name_to_db = right_path.replace(dir_name, change_dirname, 1)
                pkgsdb.savetodb(right_name_to_db, archive_fn, right_path)
        arch.close()
        
    # Change the folder name
    change_dirname = pkgs_name_in_json + '-' + pkg_ver

    if os.path.isdir(os.path.join(path, change_dirname)):
        if iswindows:
            cmd = 'rd /s /q ' + os.path.join(path, change_dirname)
            os.system(cmd)
        else:
            shutil.rmtree(os.path.join(path, change_dirname))
    
    os.rename(os.path.join(path, dir_name),os.path.join(path, change_dirname)) 


def packtest(path):
    ret = True

    if path.find(".zip") != -1:
        try:
            if zipfile.is_zipfile(path):
                # Test zip again to make sure it's a right zip file.
                arch = zipfile.ZipFile(path, "r")
                if arch.testzip():
                    ret = False
                arch.close()
            else:
                ret = False
                print('package check error. \n')
        except Exception as e:
            print('packtest error message:%s\t' % e)
            print("The archive package is broken. \n")
            arch.close()
            ret = False

    # if ".tar.bz2" in path:.
    if path.find(".tar.bz2") != -1:
        try:
            if not tarfile.is_tarfile(path):
                ret = False
        except Exception as e:
            ret = False

    # if ".tar.gz" in path:
    if path.find(".tar.gz") != -1:
        try:
            if not tarfile.is_tarfile(path):
                ret = False
        except Exception as e:
            ret = False

    return ret
