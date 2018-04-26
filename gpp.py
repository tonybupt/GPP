# coding: UTF-8

import requests
import re

startUrl = "http://mirrors.aliyun.com/pypi/simple/"
downloadBaseUrl = "http://mirrors.aliyun.com/pypi/"
localPath = "D:\\NUSIC\\"
proxies = {
    "http": "http://localhost:8899",
}


def download(file, url):
    r = requests.get(url, proxies=proxies)
    with open(localPath+file, "wb") as f:
        f.write(r.content)
    f.close()


def compareVersion(version1, version2):
    version1s = version1.split('.')
    version2s = version2.split('.')

    len1 = len(version1s)
    len2 = len(version2s)

    if len1 < len2:
        print version1
        print version2
        return False
        # raise Exception("Version Format Incompatible!")

    for i in xrange(len1):
        if version1s > version2s:
            return True
        elif version1s < version2s:
            return False
        else:
            continue
    return True

def getSingle(singleUrl):
    r1 = requests.get(singleUrl, proxies=proxies)
    downloadItems = re.findall(r"<a href=.*</a>", r1.text)

    fileUrls = {
        "py27Win32whl": [],
        "py27Win64whl": [],
        "py36Win32whl": [],
        "py36Win64whl": [],
        "py27Linux32whl": [],
        "py27Linux64whl": [],
        "py36Linux32whl": [],
        "py36Linux64whl": [],
        "gz": [],
    }

    for downloadItem in downloadItems:
        _key = ""

        _items = downloadItem.replace(r'</a>', '').split(r"../../")[1]

        url = downloadBaseUrl + _items.split('\">')[0]
        fileName = _items.split('\">')[1]

        # print url
        # print fileName

        # tar.gz与平台无关
        fileType = fileName.split('.')[-1]

        if fileType == "gz":
            fileVersion = fileName.split('-')[1]
            if not fileUrls['gz']:
                fileUrls['gz'] = [fileName, url]
            elif compareVersion(fileVersion, fileUrls['gz'][0].split('-')[1]):
                fileUrls['gz'] = [fileName, url]
            continue

        if fileType != "whl":
            continue

        fileNames = fileName.split('-')

        pyVersion = fileNames[2]
        if pyVersion == "cp27" or pyVersion == "py2":
            _key = _key + "py27"
        elif pyVersion == "cp36" or pyVersion == "py3" or pyVersion == r'py2.py3':
            _key = _key + "py36"
        else:
            continue

        osVersion = fileNames[4].split(".")[0]
        if "win" in osVersion:
            if "64" in osVersion:
                _key = _key + "Win64"
            else:
                _key = _key + "Win32"
        elif "linux" in osVersion:
            if "64" in osVersion:
                _key = _key + "Linux64"
            else:
                _key = _key + "Linux32"
        elif "any" in osVersion:
            _key = _key + "Linux64"
        else:
            continue

        _key = _key + fileType

        fileVersion = fileNames[1]
        if not fileUrls[_key]:
            fileUrls[_key] = [fileName, url]
        elif compareVersion(fileVersion, fileUrls[_key][0].split('-')[1]):
            fileUrls[_key] = [fileName, url]

    for fileUrl in fileUrls.values():
        if not fileUrl:
            continue
        print fileUrl[0]
        print fileUrl[1]
        download(fileUrl[0],fileUrl[1])


def getAll():
    r = requests.get(startUrl, proxies=proxies)
    secUrls = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", r.text)
    for secUrl in secUrls:
        r1 = requests.get(startUrl + secUrl, proxies=proxies)
        getSingle(startUrl+secUrl)


if __name__=="__main__":
    getSingle("http://mirrors.aliyun.com/pypi/simple/djangorestframework/")
    # download("cffi-1.2.0-cp27-none-win_amd64.whl", "http://mirrors.aliyun.com/pypi/packages/2c/9f/ee334eafc2f1200e8c6978dd77ec3d32feebf287f1102d941feb1841d69c/cffi-1.2.0-cp27-none-win_amd64.whl#md5=9853d7581dc836c474d07712c19c6d1a")
    # download("http://mirrors.aliyun.com/pypi/packages/90/30/ad1148098ff0c375df2a30cc4494ed953cf7551fc1ecec30fc951c712d20/djangorestframework")