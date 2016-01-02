CC	= gcc
CFLAGS	= -Wall -Wunused -g -O2
CFILES	= run.c execute.c
COBJS	= run.o execute.o
LIBS	= -lm

.SUFFIXES: .c.o

.c.o:
	$(CC) $(CFLAGS) -c $<

run: $(COBJS)
	$(CC) $(CFLAGS) -o run $(COBJS) $(LIBS)
	#$(CC) $(CFLAGS) -o run_java run_java.c
	rm -f $(COBJS)	
	#cp run_java /usr/bin

clean:
	rm -f $(COBJS)
	rm -f run

exec: 
	killall run
	./run &
