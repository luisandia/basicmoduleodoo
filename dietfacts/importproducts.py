import xmlrpclib
import csv

server = "http://localhost:8069"
db = 'dietfacts2'
username = "admin"
pwd = "programar"

common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' % server)

print common.version()

uid = common.authenticate(db, username, pwd, {})
print uid


OdooApi = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' % server)

filter = [[('largemeal', '=', True)]]

product_count = OdooApi.execute_kw(
    db, uid, pwd, 'res.users.meal', 'search_count', filter)
print product_count

Filename = 'importdata.csv'
reader = csv.reader(open(Filename, 'rb'))

print reader
for row in reader:
    print row

    filter = [[('name', '=', row[0])]]
    product_id = OdooApi.execute_kw(
        db, uid, pwd, 'product.template', 'search', filter)

    if product_id:
        record = [{'calories':row[1]}]
        print 'Found the product id=',product_id
    else:
        record = [{'name': row[0], 'calories':row[1]}]
        product_count = OdooApi.execute_kw(
            db, uid, pwd, 'product.template', 'create', record)
