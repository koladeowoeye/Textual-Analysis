# -*- coding: utf-8 -*-
import subprocess
import shlex
import logging

class Runposit:
    @staticmethod
    def shell_commands(cmds):
        # split the commands
        cmds = cmds.split("|")
        # cmds = list(map(shlex.split,cmds))
        logging.info('%s' % (cmds,))
        # run the commands
        stdout_old = None
        stderr_old = None
        p = []
        # for cmd in cmds:
        # logging.info('%s' % (cmd,))
        print(cmds)
        p.append(subprocess.Popen(cmds, shell=True, stdin=stdout_old, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        stdout_old = p[-1].stdout
        stderr_old = p[-1].stderr
        return p[-1]

    @staticmethod
    def run_posit(indir):
        runallshell ="~/posit/run_all.sh"   #command to execute - change the path accordingly
        # indir = "~/Desktop/ICCRC/Desktop/Negative"   #parameter to the command - the directory to dataset (upload in your case )
        cmd = runallshell +" "+indir  # combine command i.e run_all.sh  ~/Desktop/ICCRC/Desktop/Negative
        Runposit.shell_commands("chmod a+x "+ runallshell)  #grant priviledges to the .sh file
        p = Runposit.shell_commands(cmd)
        out = p.communicate()
        logging.error("Testing Error Logs")
        logging.error(out)
        print(out)
        #subprocess.Popen(args=[runallshell,indir], shell=True, stdout=subprocess.PIPE)

