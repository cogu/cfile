import os

indentChar=' ' #globally set to space or tab
#preprocessor
class comment:
   def __init__(self,text,line=False):
      self.text=text
      if line==True:
         self.lineComment=True
      else:
         self.lineComment=False
   def __str__(self):
      if self.lineComment == True:
         return '//%s'%self.text
      else:
         return '/*%s*/'%self.text

def linecomment(text):
   return comment(text,True)

class include:
   def __init__(self,filename,sys=False):
      self.filename=filename
      self.sys=True if sys==True else False
   def __str__(self):
      if self.sys == True:
         return '#include <%s>'%self.filename
      else:
         return '#include "%s"'%self.filename

class define:
   def __init__(self,left,right=None):
      self.left=left
      self.right=right
   def __str__(self):
      if self.right is not None:
         return "#define %s %s"%(self.left,self.right)
      else:
         return "#define %s"%(self.left)

class ifndef:
   def __init__(self,text):
      self.text=text
   def __str__(self):
      return "#ifndef %s"%(self.text)

class endif:
   def __str__(self):
      return "#endif"


#helper function
def sysinclude(filename):
   return include(filename,sys=True)

#C Language

class statement:
   def __init__(self,val,indent=0):
      self.val=val
      self.indent=indent
   def __str__(self):
      if not self.indent:
         return str(self.val)+';'
      else:
         return indentChar*self.indent+str(self.val)+';'

class line:
   def __init__(self,val,indent=0):
      self.val=val
      self.indent=indent
   def __str__(self):
      if not self.indent:
         return str(self.val)
      else:
         return indentChar*self.indent+str(self.val)

class blank:
   def __init__(self,lines=1):
      self.lines=lines
   def __str__(self):
      return '\n'*self.lines

class sequence():
   def __init__(self):
      self.elements=[]
   def __str__(self):
      result = []
      for elem in self.elements:
         if elem is None:
            result.append('')
         elif isinstance(elem,str):
            result.append(elem)
         else:
            result.append(str(elem))
         if not isinstance(elem,blank):            
            result.append('\n')
      return ''.join(result)
   def append(self,elem):
      self.elements.append(elem)
   def extend(self,seq):
      self.elements.extend(seq.elements)

class block():
   def __init__(self,indent=0):
      self.code=sequence()
      self.indent=indent
   def insert(self,index,elem):
      self.code.insert(index,elem)
   def append(self,elem):
      self.code.append(elem)
   def extend(self,sequence):
      self.code.extend(sequence)
   def __str__(self):
      if self.indent==0:
         text='{\n'
         text+=str(self.code)
         text+='}'
      else:
         text='{\n'
         text+='\n'.join([indentChar*self.indent+line if len(line)>0 else line for line in str(self.code).split('\n')])
         text+='}'
      return text
   

class variable():
   def __init__(self,name,typename='int',static=0,const=0, pointer=0,alias=0,extern=0, array=None):
      self.name=name
      self.typename=typename      
      self.array=array
      if isinstance(pointer,int):
         self.pointer=pointer
      elif isinstance(pointer,bool):
         self.pointer=1 if pointer==True else 0
      else:
         raise ValueError(pointer)
      if isinstance(alias,int):
         self.alias=alias
      elif isinstance(alias,bool):
         self.alias=1 if alias==True else 0
      else:
         raise ValueError(alias)
      if isinstance(const,int):
         self.const=const
      elif isinstance(const,bool):
         self.const=1 if const==True else 0
      else:
         raise ValueError(const)
      if isinstance(static,int):
         self.static=static
      elif isinstance(static,bool):
         self.static=1 if static==True else 0
      else:
         raise ValueError(static)
      if isinstance(extern,int):
         self.extern=extern
      elif isinstance(extern,bool):
         self.extern=1 if extern==True else 0
      else:
         raise ValueError(static)
   def __str__(self):
      result=[]
      #static
      if self.static>0:
         result.append('static')
      #exteren
      if self.extern>0:
         result.append('extern')
      #const
      if self.const & 1: #first bit of self.const activates first (lefmost) const declaration
         result.append('const')
      result.append(self.typename)
      if self.const & 2: #second bit of self.const activates second const declaration
         result.append(self.pointer*'*')
         result.append('const')
         result.append(self.name)         
      else: #special case: if second const is not declared, merge '*' and variable name together
         if self.alias>0:
            result.append(self.alias*'&'+self.name)
         else:
            result.append(self.pointer*'*'+self.name)
      #array
      text=' '.join(result)
      if self.array is not None:
         text+='[%s]'%str(self.array)
      return text


class function:
   """
   Creates a function
   """
   def __init__(self,name,typename='int',const=0,pointer=0,classname=""):
      self.name=name
      self.typename=typename
      self.classname=classname
      self.arguments=[]
      if isinstance(pointer,int):
         self.pointer=pointer
      elif isinstance(pointer,bool):
         self.pointer=1 if pointer==True else 0
      else:
         raise ValueError()    
      if isinstance(const,int):
         self.const=const
      elif isinstance(const,bool):
         self.const=1 if const==True else 0
      else:
         raise ValueError()
   def add_arg(self,arg):
      if not isinstance(arg,variable):
         raise ValueError('expected variable object')
      self.arguments.append(arg)
      return self
   def __str__(self):
      const1='const ' if self.const & 1 else ''
      pointer1='*'*self.pointer+' ' if self.pointer>0 else ''
      classname='%s::'%self.classname if len(self.classname)>0 else ""
      if len (self.arguments)>0:
         s='%s%s %s%s%s(%s)'%(const1,self.typename,pointer1,classname,self.name,', '.join([str(x) for x in self.arguments]))
      else:
         s='%s%s %s%s%s(%s)'%(const1,self.typename,pointer1,classname,self.name,'void')
      return s
   def set_class(self, classname):
      self.classname=classname

class fcall(object):
   """
   Creates a function call
   """
   def __init__(self,name):
      self.name=name
      self.parameters=[]
   def add_param(self,arg):
      if not isinstance(arg,str):
         raise ValueError('expected string object')
      self.parameters.append(arg)
      return self
   def __str__(self):
      s='%s(%s)'%(self.name,', '.join([str(x) for x in self.parameters]))
      return s

class _file(object):
   def __init__(self,path):
      self.path=path
      self.code=sequence()
   
class cfile(_file):
   def __init__(self,path):
      super().__init__(path)
   def __str__(self):
      text=''
      for elem in self.code.elements:
         text+=str(elem)
         if isinstance(elem,blank):            
            newLine=False
         else:
            newLine=True
         if newLine == True:
            text+='\n'      
      return text
      
            
class hfile(_file):
   def __init__(self,path,guard=None):
      super().__init__(path)
      if guard is None:
         basename=os.path.basename(path)
         self.guard=os.path.splitext(basename)[0].upper()+'_H'
      else:
         self.guard=guard
   def __str__(self):
      text=str(ifndef(self.guard))+'\n'
      text+=str(define(self.guard))+'\n'
      for elem in self.code.elements:
         text+=str(elem)
         if isinstance(elem,blank):            
            newLine=False
         else:
            newLine=True
         if newLine == True:
            text+='\n'      
      text+="\n%s %s\n"%(str(endif()),str(linecomment(self.guard)))
      return text

class initializer:
   def __init__(self,typeref,expression):
      self.typeref=typeref
      self.expression=expression
   def __str__(self):
      if isinstance(self.expression,list):
         return '{'+', '.join([str(x) for x in self.expression]) +'}'
      else:
         return str(self.expression)

if __name__ == '__main__':
   test = cfile('test.c')
   