import json
import uuid
from datetime import date
import dicttoxml
import requests

from sess import Sess


class InvOut(object):
    def exec(self, f, d, l, inv):
        if f == 1:
            dt = date.today().strftime('%d/%m/%y')
            usr = Sess.current()
            i = uuid.uuid1()
            it = []

            for x in inv.itms:
                it.append({'prodcode': x.id, 'quantity': x.quant, 'unitprice': x.price, 'subtotal': x.quant * x.price})

            o = {'date': dt,
                 'author': usr,
                 'id': i.hex,
                 'items': it
                 }

            j = json.dumps(o)

            if d == 'f':
                f = open(l, 'x')
                f.write(j)
                f.close()

            if d == 'c':
                r = requests.post(l, j, {'Content-type': 'application/json', 'Accept': 'text/plain'})

        if f == 2:
            dt = date.today().strftime('%d/%m/%y')
            usr = Sess.current()
            i = uuid.uuid1()
            it = []

            for x in inv.itms:
                it.append({'prodcode': x.id, 'quantity': x.quant, 'unitprice': x.price, 'subtotal': x.quant * x.price})

            o = {'date': dt,
                 'author': usr,
                 'id': i.hex,
                 'items': it
                 }

            xml = str(dicttoxml.dicttoxml(o))

            if d == 'f':
                f = open(l, 'x')
                f.write(xml)
                f.close()

            if d == 'c':
                r = requests.post(l, xml, {'Content-type': 'application/xml', 'Accept': 'text/plain'})

        if f == 3:
            dt = date.today().strftime('%d/%m/%y')
            usr = Sess.current()
            i = uuid.uuid1()
            it = []

            for x in inv.itms:
                it.append({'prodcode': x.id, 'quantity': x.quant, 'unitprice': x.price, 'subtotal': x.quant * x.price})

            o = {'date': dt,
                 'author': usr,
                 'id': i,
                 'items': it
                 }

            c = 'date,author,id,prodcode,quantity,unitprice,subtotal\n'

            for y in o['items']:
                c += '{0},{1},{2},{3},{4},{5}\n ' \
                    .format(o['date'], o['author'], o['id'], y['prodcode'], y['quantity'],
                            y['unitprice'],y['subtotal'])

            if d == 'f':
                f = open(l, 'x')
                f.write(c)
                f.close()

            if d == 'c':
                r = requests.post(l, c, {'Content-type': 'application/csv', 'Accept': 'text/plain'})


class Inv(object):
    def __init__(self, itms):
        self.itms = itms


class Itm(object):
    def __init__(self, id, quant, price):
        self.id = id
        self.quant = quant
        self.price = price


if __name__ == '__main__':
    itms = [Itm('widget', 5, 10.0)]
    inv = Inv(itms)
    InvOut().exec(f=3, d='f', l='invout/testfile.xml', inv=inv)
