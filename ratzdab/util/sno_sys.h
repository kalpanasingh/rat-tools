/*
** File:        sno_sys.h
*/

#ifndef SNO_SYS_H
#define SNO_SYS_H

#ifdef __POWERPC__

typedef unsigned char   byte;
typedef short           int16;
typedef unsigned short  u_int16;
typedef int            int32;
typedef unsigned int   u_int32;

#ifdef __MWERKS__
typedef unsigned long   u_long;
#endif

#else /* not __POWERPC__ */

typedef unsigned char  byte;
typedef short   int16;
typedef unsigned short u_int16;
typedef int    int32;
typedef unsigned int  u_int32;

#endif /* not __POWERPC__ */

#ifdef VAX
typedef unsigned long u_long;
#endif

#endif /* not SNO_SYS_H */
