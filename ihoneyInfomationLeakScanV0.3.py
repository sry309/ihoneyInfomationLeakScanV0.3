# coding:utf-8
import hackhttp
import logging
import multiprocessing
from datetime import datetime
from argparse import ArgumentParser


logging.basicConfig(level=logging.WARNING, format="%(message)s")


def vlun(url, datefile):
    webinfokey = "</web-app>"
    gitkey = 'repositoryformatversion'
    svnkey = 'svn://'

    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}

    try:
        hh = hackhttp.hackhttp()
        code, _, body, _, _ = hh.http(url=url, headers=headers, location=False, throw_exception=False, method='GET')

        if code == 200:
            if webinfokey in body or gitkey in body or svnkey in body:
                logging.warning("[*] {}".format(url))
                with open(datefile, 'a') as f:
                    try:
                        f.write(str(url) + '\n')
                    except:
                        pass
            else:
                logging.warning("[ ] {}".format(url))
        else:
            logging.warning("[-] %s" % url)
    except Exception as e:
        print e


def ucheck(target=None):
    if target is not None:
        if target.startswith('http://') or target.startswith('https://'):
            if not target.endswith('/'):
                target = target + '/'
        else:
            target = 'http://' + target
            if not target.endswith('/'):
                target = target + '/'
        return target


def urlcheck(target=None, ulist=None):
    if target is not None and ulist is not None:
        if target.startswith('http://') or target.startswith('https://'):
            if target.endswith('/'):
                ulist.append(target)
            else:
                ulist.append(target + '/')
        else:
            line = 'http://' + target
            if line.endswith('/'):
                ulist.append(line)
            else:
                ulist.append(line + '/')
        return ulist


if __name__ == "__main__":
    usageexample = '\n       Example: python3.5 ihoneyInfomationLeakScan.py -t 100 -f gitsvn.txt\n'
    usageexample += '                '
    usageexample += 'python3.5 ihoneyInfomationLeakScan.py -u https://www.example.com/'

    parser = ArgumentParser(add_help=True, usage=usageexample, description='Information leak scanning tools..')
    parser.add_argument('-f', dest="url_file", help="Url file name")
    parser.add_argument('-t', dest="max_thread", nargs='?', type=int, default=1, help="Max threads")
    parser.add_argument('-u', '--url', dest='url', nargs='?', type=str, help="Example: http://www.example.com/")
    args = parser.parse_args()

    pool = multiprocessing.Pool(args.max_thread)

    info_dic = ['.git/config', '.svn/entries', 'WEB-INF/web.xml']
    url_file = args.url_file

    datefile = datetime.now().strftime('%Y%m%d_%H-%M-%S.txt')

    urllist = []
    with open(str(url_file)) as f:
        while True:
            line = str(f.readline()).strip()
            if line:
                urllist = urlcheck(line, urllist)
            else:
                break

    for u in urllist:
        for info in info_dic:
            pool.apply_async(vlun, args=(str(u) + '' + str(info), datefile))

    pool.close()
    pool.join()
