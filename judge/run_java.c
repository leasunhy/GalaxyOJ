#include <stdlib.h>
#include <stdio.h>
int main() {
	fprintf(stderr, "Ready to execute Java Program\n");
	int code = system("java -cp /tmp Main");
	fprintf(stderr, "Execute Java Program, exit code = %d\n", code);
	if (code == 38912) return 1;
	if (code) return -1;
	return 0;
}