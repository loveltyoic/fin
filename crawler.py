from dataapiclient import Client
import json
import pdb

import os
def craw_by_date(date):
    try:
        client = Client()
        client.init('0a10b42bf3c6488a9d2e97a8e5ba839633c0791dc130569b64de680209fe60ae')
        slice_cnt = 200
        ids = [i.strip() for i in open("/data/zhli7/news/id_{}.txt".format(date), 'r').readlines()]
        c = 0
        with open("news_{}.csv".format(date), 'w') as f:
            while c < len(ids) / slice_cnt:
                id_str = ','.join(ids[slice_cnt*c:slice_cnt*(c+1)])
                url2='/api/subject/getNewsBody.json?field=&newsID='+id_str
                code, result = client.getData(url2)
                if(code==200):
                    json_result = json.loads(result, encoding='utf8')
                    for value in json_result['data']:
                        f.write('$*$'.join([str(value['newsID']), value['newsBody'], value['newsURL']])+"\n")
                    f.write(json.dumps(json_result))
                    #f.write(result+"\n")
                    break
                else:
                    print(code)
                    print(result)
                c += 1
    except Exception as e:
        #traceback.print_exc()
        raise e
        
def craw_by_code(code):
    target_file = "/data/zhli7/company_news/news_{}.csv".format(code)
    if os.path.isfile(target_file):
        print(target_file, ' exsits, skip it')
        return 0
    try:
        client = Client()
        #client.init('13acded54e0e47e4e440cb3fe42fdbff1113e6dcb6a27d601ee128f28ad91192')
        client.init('97b197e1451722213caa5ff4a16d51dd868188e1d0d363bf673de596e7201297')
        slice_cnt = 300
        ids = [i.strip() for i in open("/data/zhli7/code/code_{}.txt".format(code), 'r').readlines()]
        c = 0
        with open(target_file, 'w') as f:
            while c < len(ids) / slice_cnt:
                id_str = ','.join(ids[slice_cnt*c:slice_cnt*(c+1)])
                url2='/api/subject/getNewsBody.json?field=&newsID='+id_str
                status, result = client.getData(url2)
                if(status==200):
                    json_result = json.loads(result, encoding='utf8')
                    for value in json_result['data']:
                        f.write('$*$'.join([str(value['newsID']), value['newsBody'].replace("\n", " "), value['newsURL']])+"\n")
                    f.write(json.dumps(json_result))
                    #f.write(result+"\n")
                else:
                    print(status)
                    print(result)
                c += 1
    except Exception as e:
        #traceback.print_exc()
        raise e