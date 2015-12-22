import os
import subprocess
import glob

from . import worker

from judge.config import COMPILER_LIST
from judge.config import COMPILER_OPTION_LIST
from judge.config import COMPILE_TIME_LIMIT

def compile(source_path, compiler_id, exec_path):
    #print("[log] compile:")
    #print(COMPILER_LIST[compiler_id])
    #print(source_path)
    #print(COMPILER_OPTION_LIST[compiler_id])
    proc = subprocess.Popen([COMPILER_LIST[compiler_id],
        source_path,
        *COMPILER_OPTION_LIST[compiler_id]], 
        cwd = exec_path,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    try:
        outs, err = proc.communicate(timeout = COMPILE_TIME_LIMIT)
    except:
        proc.kill()
        out, err = proc.communicate()
    return ("a.out", err)

def execute(program, input_file, output_file, time_limit, memory_limit):
    proc = subprocess.Popen(
        ["execute", "-c", program, "-i", input_file, "-o", output_file, "-t", str(time_limit), "-m", str(memory_limit)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    
    out = out.split(',')
    return (out, err)

def check(file_out, std_out):
    proc = subprocess.Popen(["diff", "%s %s"%(file_in, file_out)], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    return {out is None, err}

def judge(source_path, testcase_folder, compiler_id, time_limit, memory_limit):
    from tempfile import TemporaryDirectory
    tmp_folder = TemporaryDirectory()
    (prog, err) = compile(source_path, compiler_id, tmp_folder.name)
    if err is not None:
        return {"verdict":"Compile Error", "time_used": 0, "memory_used": 0, "log": err}
    sum_time = 0
    max_mem = 0
    for filename in glob.glob(testcase_folder + "/*.in"):
        file_in = filename
        file_out = filename[:-2] + ".tmp"
        std_out = filename[:-2] + ".out"
        (out, err) = execute(prog, file_in, file_out, time_limit, memory_limit)
        if out[0] != "OK":
            return {"verdict": out[0], "time_used": out[1], "memory_used": out[2], "log": err}
        (verdict, err) = check(file_out, std_out)
        if verdict == False:
            return {"verdict": "Wrong Answer", "time_used": sum_time, "memory_used": max_mem, "log": err}
        sum_time += int(out[1])
        max_mem = max(max_mem, out[2])
    return {"verdict": "Accepted", "time_used": sum_time, "memory_used": max_mem, "log": None}

