# -*- coding: utf-8 -*-
"""
/***************************************************************************
Script to convert csv file to sqlite.
                                 A QGIS plugin
 options
                             -------------------
        begin                : 2014-05-30
        copyright            : (C) 2014 by Options
        email                : tim@kartoza.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'ismail@kartoza.com'
__revision__ = '$Format:%H$'
__date__ = '06/06/2014'
__copyright__ = ''

import csv
import sqlite3
import os
import sys

if __name__ == '__main__':
    csv_path = ''
    if len(sys.argv) == 2:
        csv_path = sys.argv[1]
    elif len(sys.argv) == 1:
        csv_path = '../data/sg_regional_offices.csv'
    else:
        print 'Usage'
        print 'python csv_to_sqlite.py [csv file]'
        exit()

    if not os.path.exists(csv_path):
        print 'Your csv is not exist in %s' % csv_path
        exit()

    # sqlite3_path = csv_path[:-3] + 'sqlite'
    sqlite3_path = '../data/sg_diagrams.sqlite'

    # adapted from http://stackoverflow.com/a/2888042/1198772
    con = sqlite3.connect(sqlite3_path)
    cur = con.cursor()
    query = "DROP TABLE IF EXISTS regional_office; "

    print 'Executing %s' % query
    cur.execute(query)

    query = "CREATE TABLE regional_office "
    query += "('province', 'region_code', 'typology', 'office', 'office_no');"

    print 'Executing %s' % query
    cur.execute(query)

    with open(csv_path, 'rb') as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dict_reader = csv.DictReader(fin)  # comma is default delimiter

        # province,region_code,typology,office,office_no
        rows = [(i['province'], i['region_code'], i['typology'],
                  i['office'], i['office_no']) for i in dict_reader]

    query = "INSERT INTO regional_office "
    query += "('province', 'region_code', 'typology', 'office', 'office_no') "
    query += "VALUES (?, ?, ?, ?, ?)"

    print 'Executing %s' % query
    cur.executemany(query, rows)

    con.commit()
