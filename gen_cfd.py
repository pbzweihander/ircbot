# Name : gen_cfd.py
# Author : pbzweihander
# Email : sd852456@naver.com
#
# Copyright (C) 2016-2017 pbzweihander
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

print("Loading Modules...")

from sentence_generator import calc_cfd
import pickle
import sys

doc = ""
cfd = []

fn = ""
on = ""

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage : python3 gen_cfd.py <text file> [<output file> (Default=cfd.pkl)]")
    sys.exit(0)
elif len(sys.argv) == 2:
    fn = sys.argv[1]
    on = "cfd.pkl"
else:
    fn = sys.argv[1]
    on = sys.argv[2]

print("Reading Text File...")
with open(fn, 'r') as f:
    while True:
        line = f.readline()
        if not line: break
        doc += line

print("Calculating Conditional Frequency Distribution...")
cfd = calc_cfd(doc)

print("Writing Pickle Dump...")
with open(on, 'wb') as f:
    pickle.dump(cfd, f, -1)

print("Done!")

