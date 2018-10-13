import re


class Command:
  # exec += print
  is_test = False

  def __init__(self, cmd):
    '''
    初始化命令
    :param cmd: 例如 echo 等命令
    '''
    self.__cmd = cmd
    self.__param_list = []
    self.out = None
    self.returncode = None

  def make(self):
    '''
    构建命令
    :return: 构建好的命令
    '''
    cmd = self.__cmd
    for param in self.__param_list:
      param = " ".join(param)
      cmd += " " + param
    return cmd

  def print(self):
    '''
    打印命令
    :return: None
    '''
    print(self.make())

  def add_param(self, *param_list):
    '''
    添加参数，例如

    `echo.add_param("-e",'abcd\nabcd')`
    `echo.add_param("abcd")`
    `echo.add_param("111").add_param("222").exec()`

    :param param_list:
    :return: Command
    '''
    if len(param_list) == 0: return
    self.__param_list.append(tuple(param_list))
    return self

  def exec(self):
    '''
    执行命令
    :return: 执行结果，stdout/stderr 会打印出来
    '''
    if Command.is_test:
      self.print()
    import os
    return os.system(self.make())

  def exec_quiet(self):
    if Command.is_test:
      self.print()
    import subprocess
    subp = subprocess.run(self.make(), shell=True, stdout=subprocess.PIPE)
    self.out = subp.stdout.decode("utf-8")
    self.returncode = subp.returncode
    return self.returncode

  def get_param(self, n):
    '''
    返回对应位置 n 的参数(从完整命令里)，例如

    `echo -a -l -h`
    echo.get_param(1) # "-a"
    echo.get_param(0) # "echo"
    echo.get_param(100) # ""

    :param n: 第几个参数
    :return: 参数值
    '''
    try:
      return re.split("\s", self.make())[n]
    except:
      return ""

  def rm_param(self, param_by_first):
    '''
    删除匹配**第一个值**的参数，例如

    ls.add_param("-l","-a")
    ls.add_param("-h")

    ls.rm_param("-l") # 可以删除
    ls.rm_param("-a") # 则不能删除

    :param param_by_first: 第一个参数
    :return: None
    '''

    def check(t, p):
      '''
      测试类似于 ("-f","abcd.txt") 等是否**全匹配**

      :param t: tuple
      :param p: param，用来匹配等参数
      :return:
      '''
      for x in t:
        if x == p: return False
      return True

    self.__param_list = list(filter(lambda t: check(t, param_by_first), self.__param_list))

  def clean(self):
    self.__param_list = []
    self.out = None
    self.returncode = None
