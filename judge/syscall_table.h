#ifndef _SYSCALL_TABLE_H_

int	syscall_used[512];

# ifdef __i386__
void init_syscall_table() {
	memset(syscall_used, 0, sizeof(syscall_used));
	syscall_used[  1] = 1;// exit
	syscall_used[  3] = 1;// read
	syscall_used[  4] = 1;// write
	syscall_used[  5] = 1;// open
	syscall_used[  6] = 1;// close
	//syscall_used[ 33] = 1;// access
	//syscall_used[ 125] = 1;// mprotect
	syscall_used[ 45] = 1;// brk
	syscall_used[ 54] = 1;// ioctl
	//syscall_used[ 67] = 1;// sigaction
	syscall_used[85] = 1;//readlink
	syscall_used[ 90] = 1;// mmap
	syscall_used[ 91] = 1;// munmap
	syscall_used[122] = 1;// uname
	//syscall_used[186] = 1;// sigaltsatck
	syscall_used[192] = 1;// mmap2
	syscall_used[197] = 1;// fstat64
	syscall_used[199] = 1;// getuid32    Get user identity
	syscall_used[200] = 1;// getegid32   Get group identity
	syscall_used[201] = 1;// geteuid32   Get user identity
	syscall_used[202] = 1;// getgid32    Get group identity
	syscall_used[221] = 1;// getdents64  Get directory entrys
	syscall_used[252] = 1;// exit group
	syscall_used[140] = 1;// llseek
	syscall_used[145] = 1;// readv
	syscall_used[146] = 1;// writev
	syscall_used[174] = 1;//sys_rt_sigaction
	syscall_used[191] = 1;//getrlimit

	//syscall_used[243] = 1;//set_thread_area

/* I think set_thread_area is not necessary to be allowed */

}

# else

void init_syscall_table() {
	syscall_used[ 60] = 1;	// sys_exit
	syscall_used[  0] = 1;	// sys_read
	syscall_used[  1] = 1;	// sys_write
	syscall_used[  2] = 1;	// sys_open
	syscall_used[  3] = 1;	// sys_close
	syscall_used[  5] = 1;	// sys_fstat
	syscall_used[  8] = 1;	// sys_lseek
	syscall_used[  9] = 1;	// sys_mmap
	syscall_used[ 12] = 1;	// sys_brk
	syscall_used[ 13] = 1;	// sys_rt_sigaction
	syscall_used[ 16] = 1;	// sys_ioctl
	syscall_used[ 19] = 1;	// sys_readv
	syscall_used[ 20] = 1;	// sys_writev
	syscall_used[ 11] = 1;	// sys_munmap
	syscall_used[ 63] = 1;	// sys_uname
	syscall_used[ 89] = 1;	// sys_readlink
	syscall_used[ 97] = 1;	// sys_getrlimit
	//mmap2 is not found in x86_64 system call
	syscall_used[102] = 1;	// sys_getuid
	syscall_used[104] = 1;	// sys_getgid
	syscall_used[107] = 1;	// sys_geteuid
	syscall_used[108] = 1;	// sys_getegid
	syscall_used[158] = 1;	// sys_arch_prctl
	syscall_used[217] = 1;	// sys_getdents64
	syscall_used[231] = 1;	// sys_exitgroup
}
#endif

#endif
