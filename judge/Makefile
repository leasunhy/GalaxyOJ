CC	= gcc
CFLAGS	= -Wall -Wunused -g -O2 -m32
CFILES	= main.c execute.c
COBJS	= main.o execute.o
LIBS	= -lm

.SUFFIXES: .c.o

.c.o:
	$(CC) $(CFLAGS) -c $<

judge: $(COBJS)
	$(CC) $(CFLAGS) -o judge $(COBJS) $(LIBS)
	#$(CC) $(CFLAGS) -o run_java run_java.c
	rm -f $(COBJS)	
	#cp run_java /usr/bin

clean:
	rm -f $(COBJS)
	rm -f judge

exec: 
	killall judge
	./judge &
