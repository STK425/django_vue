import threading
import time
from .MyNLP import main

class MainSystem:

    def __init__(self):
        self.flag = 1
        self.is_work_time = 0
        threading.Thread(target = self.get_cmd_input).start()
        threading.Thread(target = self.get_work_time).start()
        threading.Thread(target = self.main_System).start()
        print('系统开始运行')

    def main_System(self):
        while True:
            while self.flag:
                if self.is_work_time:
                    print('系统核心开始运行')
                    self.flag = 10000

                    main.main()
                    
                    self.flag = 1
                    self.is_work_time = 0
                    print('系统核心结束运行')
            if self.flag == -1:
                exit(0)

    def get_cmd_input(self):

        while True:
            try:
                cmd_str = input()
                if cmd_str == 'start':
                    self.sys_start()
                elif cmd_str == 'end' or cmd_str == 'stop':
                    self.sys_end()
                elif cmd_str == 'help' or cmd_str == 'h':
                    print('本系统支持如下命令：')
                    print('\tstart\t\t启动系统')
                    print('\tend/stop\t\t停止系统')
                    print('\texit\t\t退出系统')
                    print('\thelp/h\t\t获取帮助')
                elif cmd_str == 'exit':
                    self.sys_exit()
                else:
                    print('输入有误，请重试！')
                    print('如需帮助，请输入”help“或“h”以查看使用说明')
            except EOFError:
                print('请手动关闭服务器')
                self.sys_exit()
                

    def get_work_time(self):
        while True:
            time.sleep(60 * 60)
            now = time.localtime(time.time())
            if not self.is_work_time and now.tm_hour == 4:
                self.is_work_time = 1
            if self.flag == -1:
                exit(0)

    def sys_start(self):
        if self.flag != 10000:
            self.flag = 1
        print('系统已启动')

    def sys_end(self):
        if self.flag == 10000:
            print('系统核心运行中，暂时无法停止，该状态将不会持续超过……')
        else:
            self.flag = 0
            print('系统已停止')

    def sys_exit(self):
        if self.flag == 10000:
            print('系统核心运行中，暂时无法退出系统，该状态将不会持续超过……')
        else:
            print('已退出系统')
            self.flag = -1
            exit(0)

    def is_running(self):
        return self.flag == 1

    def sys_main_is_running(self):
        return self.flag == 100000

    def sys_main_start(self):
        if is_running():
            return 0
        else:
            self.is_work_time = 1
            return 1
        return -1


