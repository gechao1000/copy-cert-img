# coding=utf-8
import os
import shutil
import pandas as pd
import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename='24.log',
                filemode='a')


IMG_SRC = 'E:/bmcp/bmcpImageServer/bmcpImageServer/userimgs/temp/{0}'
IMG_DB = 'LGB_ZZ/{0}/{1}/{2}/{3}'
IMG_DEST = 'E:/bmcp/bmcpImageServer/bmcpImageServer/userimgs/{0}'
SQL_TEMPLATE = 'update S_CERTIFICATE_IMG_000024 set CERT_PICNAME=\'{0}\' where JLBH={1} and INX={2};\n'


def cp(src, dest, sql):
    if not os.path.isfile(src):
        log.warning('%s not exist!' % (src))
    else:
        fpath, fname = os.path.split(dest)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(src, dest)
        log.info('copy %s->%s' % (src, dest))
        with open('24.sql', 'a+') as f:
            f.write(sql)


df = pd.read_csv('data/24.csv')

cert = df[df.LEN == 30]

for index, row in cert.iterrows():
    file_name = row.IMG.split('\\')[1]
    src = IMG_SRC.format(file_name)
    path = IMG_DB.format(row.SHOP, row.JTCODE[-1], row.JTCODE[-6:], file_name)
    dest = IMG_DEST.format(path)
    sql = SQL_TEMPLATE.format(path, row.JLBH, row.INX)
    cp(src, dest, sql)
    print(file_name)

print('OK')
