
#ifndef ERROR_H
#define ERROR_H

/*
 * error.c header file.  Originally from trt_err.h version 1.5 from the
 * TRT daq.
 */

/*
 * Error recording facility defines.
 *
 *    If you you add a new facility, you must add code in 
 *    error.c:SNO_printerr and error.c:SNO_printf to handle it.
 *
 *    At the moment, there are a maximum of 10 facilities.  It is easy to
 *    change though.
 */

enum ERR_FACS { DAQ_FAC=0,
		VME_FAC,
		INIT_FAC,
		DB_FAC,
		UTIL_FAC,
                SYS_FAC,
                MTC_FAC,
                EB_FAC,
                CAL_FAC,
                RC_FAC,
                HV_FAC};

#define DFAC_STR  "DAQ"               /* DAQ_FAC     */
#define VFAC_STR  "VME"               /* VME_FAC     */
#define IFAC_STR  "INIT"              /* INIT_FAC    */
#define DBFAC_STR "DB"                /* DB_FAC      */
#define UFAC_STR  "UTIL"              /* UTIL_FAC    */
#define SFAC_STR  "SYS"               /* SYS_FAC     */
#define MFAC_STR  "MTC"               /* MTC_FAC     */
#define EFAC_STR  "EB"                /* EB_FAC      */
#define CFAC_STR  "CAL"               /* CAL_FAC     */
#define RFAC_STR  "RC"                /* RC_FAC      */
#define HFAC_STR  "HV"                /* HV_FAC      */

/*
 * These are the output destinations for the error recrding facility.
 * 0 is no output.  The value is a bitmask, so the defines must be
 * powers of 2.
 */

#define T_NONE   0
#define T_STDERR 1
#define T_FILE   2

/*
 *  This is to be used for dumping error strings for the the error recording
 *  facility.  Storage is allocated in error.c
 */
extern char err_str[1024];



int
   SNO_seterr_level( int level, enum ERR_FACS facility ),
   SNO_seterr_output( int output, enum ERR_FACS facility ),
   SNO_geterr_level( enum ERR_FACS facility );

void
   SNO_printerr( int level, enum ERR_FACS facility, char *string ),
   SNO_output_fname( char *string ),
   SNO_output_file_puts( char *string ),
   SNO_output_file_open( char *mode ),   
   SNO_output_file_close( void ),
   SNO_printf( int level, enum ERR_FACS facility, char *format, ... ),
   SNO_printf_errl( int level, enum ERR_FACS facility, char *format, ... );


#endif /* not SNOERR_H */
