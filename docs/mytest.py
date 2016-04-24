#coding=UTF-8


class TestClass:
    def sub(self,a,b):
        return a-b
    def add(self,a,b):
        return a+b
    def echo(self):
        print "test"

def main():
    class_name = "TestClass" #类名
    module_name = "mytest"   #模块名
    method = "echo"          #方法名

    module = __import__(module_name) # import module
    print "#module:",module
    c = getattr(module,class_name)  
    print "#c:",c
    obj = c() # new class
    print "#obj:",obj
    obj.echo()
    mtd = getattr(obj,method)
    print "#mtd:",mtd
    mtd() # call def
    
    mtd_add = getattr(obj,"add")
    t=mtd_add(1,2)
    print "#t:",t

    #mtd_sub = getattr(obj,"sub")
    #print mtd_sub(2,1)
    

if __name__ == '__main__':
   main()

