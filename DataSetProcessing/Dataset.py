"""
Give information about Dataset
"""
import os
import sys
#from traceback import print_tb

class Dataset:
    """Main class"""
    def __init__(self,path):
        """Main constructor"""
        self.path = path
        
        self.file_stats = {} #for each file type we have key: {'min': --, 'max': --, 'tot_size': --,'count': --, avg: --}
        self.totalsize = 0 #total size of the path
        self.totdirs = 0 # tot sub dir
        self.totalfiles = 0 # tot files
        self.filetype_nil_count=0 #tot files with no extension
        path_iter = os.scandir(self.path) #Return an iterator of os.DirEntry objects for given path
        for entry in path_iter:
            self._process_entry(entry)
        for type in self.file_stats:
            val = self.file_stats[type]
            val['avg'] = val['tot_size'] // val['count']  
             
    def _process_entry(self, entry): # single underscore means dont show up in from self import *
        """Helper function. Dont call it"""
        #is file entry
        if not entry.name.startswith('.') and entry.is_file(follow_symlinks=False):
            name, *rest = entry.name.split('.')
            if len(rest) > 0:
                ext = rest[-1] # last element of rest list; we can have multiple extensions
            elif len(rest) == 0:
                ext = 'filetype_nil'
                self.filetype_nil_count += 1
            
            
            if ext != 'filetype_nil': 
                size = entry.stat(follow_symlinks=False).st_size # entry.stat() ret os.stat_result
                type = ext
                val = self.file_stats.setdefault(type,{'min': size, 'max': size, 'tot_size':0,'count':0})
                if val['min'] > size: val['min'] = size
                if val['max'] < size: val['max'] = size
                val['tot_size'] = val['tot_size'] + size
                val['count'] += 1
                self.totalsize += size
                self.totalfiles += 1               
                
            
        elif not entry.name.startswith('.') and entry.is_dir(follow_symlinks=False):
            self.totdirs += 1 #tot subdirs seen
            for entry in os.scandir(entry.path):
                self._process_entry(entry)
        elif not entry.name.startswith('.') and entry.is_symlink():
            ext = 'symbolic_link'  # for shortcuts
            val = self.filetype_count.setdefault(ext,0) + 1
            self.filetype_count[ext] = val
            #print(entry.path)
    
    def __str__(self):
        
        return """Dataset Path: {path} tot size(KB): {totsize}
            tot dirs: {totdirs} tot files: {totfiles}
            nil_file_type count: {nilcount}
            file stats: {stats}""".format(path = self.path, 
                                                    
                                                    totsize = (self.totalsize // (1024)),
                                                    totdirs = self.totdirs,
                                                    totfiles = self.totalfiles,
                                                    nilcount = self.filetype_nil_count,
                                                    stats = self.file_stats
        )
        

    def __repr__(self):
        self.__str__()



if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: python self.py path')

    path = sys.argv[1]
    obj = Dataset(path)
    print(obj)
    
    
    
    
    

    


    


            
    
    
