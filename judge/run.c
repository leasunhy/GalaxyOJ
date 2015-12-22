#include <stdio.h>
#include "execute.h"
#include "run.h"

static
void parse_arguments(int argc, char* argv[]) {
    int opt;
    extern char *optarg;

    while ((opt = getopt(argc, argv, "c:t:m:d:S:s")) != -1) {
        switch (opt) {
            case 'c': strncpy(codepath, optarg, 120);   break;
            case 'S': strncpy(spejpath, optarg, 120);   break;
            case 't': time_limit   = atoi(optarg);      break;
            case 'm': memory_limit = atoi(optarg);      break;
            case 's': spj          = true;              break;
            case 'd': strcpy(run_dir, optarg);          break;
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
    int ret = execute("in", "out", "a", 1000, 1000, 1000, &mem, &time);
    fprintf(stdout, "%d,%d,%d\n", ret, (int)(time * 1000), mem);
}

