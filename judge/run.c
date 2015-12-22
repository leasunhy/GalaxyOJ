#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "execute.h"
#include "run.h"

static
void parse_arguments(int argc, char* argv[]) {
    int opt;
    extern char *optarg;

    while ((opt = getopt(argc, argv, "c:t:m:d:s:i:o:")) != -1) {
        switch (opt) {
            case 'c': strncpy(codepath, optarg, 120);   break;
            case 's': spj = 1;
                      strncpy(specpath, optarg, 120);   break;
            case 'i': strncpy(in_file, optarg, 120);    break;
            case 'o': strncpy(out_file, optarg, 120);   break;
            case 't': time_limit   = atoi(optarg);      break;
            case 'm': memory_limit = atoi(optarg);      break;
            case 'd': strncpy(rundir, optarg, 120);     break;
            default:
                fprintf(stderr, "Unknown option -%c\n", opt);
                exit(-1);
        }
    }
}

int main(int argc,char *argv[]) {
    parse_arguments(argc, argv);
    int mem;
    double time;
    int ret = execute(in_file, out_file, codepath, time_limit, memory_limit, 30000, &mem, &time);
    fprintf(stdout, "%s,%d,%d\n", result[-ret], (int)(time * 1000), mem);
    return 0;
}

