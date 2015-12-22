#ifndef RUN_H

char codepath[121];
char specpath[121];
char rundir[121] = "/tmp";

char in_file[121];
char out_file[121];

int time_limit;
int memory_limit;
int spj;

const char* result[] = {
    "OK",
    "Runtime Error",
    "Time Limit Exceed",
    "Memory Limit Exceed",
    "Output Limit Exceed",
    "Restrict Function"
};

#endif
