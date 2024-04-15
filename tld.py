import os
import sys
import json


def _path(file_name_:str)->str:
    return (
      'tld_db/'+file_name_
    )
    
class TldManager:
    def __init__(self):
        self._cache_IDN = {}
        self._cached_IDN = False
        self._cache_allTLD = []
        self._not_cached_allTLD = True
    def getFile(
      self,
      file_name_: str
    )->list:
        with open(_path(file_name_), "r") as f:
            data = json.load(f)
            return data
    def getIDNs(
      self
    ):
        out = {}
        listcc = self.getFile('cctld.json')
        if self._cached_IDN:
            return self._cache_IDN
        for i in listcc:
            file_name = ('IDN_'+i+'.json')
            if os.access(
               _path(file_name), os.R_OK
            ):
                self._cache_IDN[i] = self.getFile(file_name)
        return self._cache_IDN
    def getTLDs(
      self
    )->list[str]:
        if self._not_cached_allTLD:
            self._cache_allTLD = self.getFile(
              'alltld.json'
            )
            self._not_cached_allTLD = False
        return self._cache_allTLD

manager = TldManager()
def getIDNs():
     return manager.getIDNs()
def getTLDs():
     return manager.getTLDs()


def splitter(line_:str)->list[str]:
    not_double = True
    if line_[-2:] == '/\n':
        line_ = line_[:-2]
    if line_[-1:] == '/':
        line_ = line_[:-1]
    [protocol, addr] = line_.split('//')
    addrs = addr.split('.')
    if (
      (addrs[-1] in (getIDNs())) 
      and 
      (addrs[-2] in (getIDNs())[addrs[-1]])
    ): 
       top = (addrs[-2]+'.'+addrs[-1])
       second = addrs[-3]
       sub = addrs[:-3]
       not_double = False
    if not_double:
        top = addrs[-1]
        second = addrs[-2]
        sub = addrs[:-2]
    return ([protocol, sub, second, top])

def processor(lines_:str):
    out = []
    for i in lines_:
        out.append(splitter(i))
    return out
