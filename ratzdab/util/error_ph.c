
static char *ID[] = {"$Id: error_ph.c,v 1.14 2000/01/10 20:05:55 phil Exp $"};

/*
 * This file provides error support routines:
 *         SNO_seterr_level     : set error output level for a facility [ptk]
 *         SNO_seterr_output    : set error output dest for a facility [ptk]
 *         SNO_printerr         : prints a message at level for facility [ptk]
 *         SNO_output_fname     : sets T_FILE output file filename [ptk]
 *         SNO_output_file_puts : prints text to output file [ph]
 *         SNO_output_file_open : opens output file [ph]
 *         SNO_output_file_close: closes T_FILE output file [ptk]
 * (See README.error for usage)
 * Originally from version 1.3 of the TRT daq error.c 
 *
 */

#include <malloc.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <time.h>

#include "sys_util/error.h"
#include "CUtils.h"

#define __MAXIMUM_LINES__

char err_str[1024];

static void
   SNO_output_stderr( char *string );


/*****************************************************************************
 * This is code provided a standardized error recording facility.  It is     *
 * based on error levels and facilities.  Each logical section of code can   *
 * have its own facility and determine independantly which messages should   *
 * be printed/recorded.                                                      *
 *****************************************************************************/

/*
 * You *MUST* change the init of SNO_err_levels and SNO_err_output if you
 * change this!
 */
#define MAX_FACILITY 20

/* PH 06/05/98 additions */
#ifdef __MAXIMUM_LINES__
  #define SNO_PRINTF_INTERVAL	10.0		// interval for maximum number of messages
  #define MAX_SNO_PRINTF_NUM	20		// maximum of messages per time period
  static double interval_time[MAX_FACILITY] = { 0 };
  static int messages_printed_in_this_interval[MAX_FACILITY] = { 0 };
#else // __MAXIMUM_LINES__
  #define SNO_PRINTF_INTERVAL	1.0		// interval for maximum number of messages
  #define MAX_SNO_PRINTF_NUM	20		// maximum of messages per time period
  #define MESSAGE_SAMPLE_NUM    4               // num messages to print as a sample when skipping
  static double printf_call_times[MAX_SNO_PRINTF_NUM] = { 0 };
  static int printf_call_pt = 0;
#endif // __MAXIMUM_LINES__
#define PERMANENT_LEVEL		1		// messages at or below this level always printed
static int skipped_printf[MAX_FACILITY] = { 0 };
static int sample_printf[MAX_FACILITY] = { 0 };
extern double double_time();
				
/*
 * We need to initialize SNO_err_levels and SNO_err_outuut, but there is
 * no good way to do it.
 * It *MUST* be changed when MAX_FACILITY is changed.
 */
static int SNO_err_levels[MAX_FACILITY] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
					   0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static int SNO_err_output[MAX_FACILITY] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
					   0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

static char * SNO_fac_string[MAX_FACILITY] = {
		DFAC_STR, VFAC_STR,  IFAC_STR,  DBFAC_STR,   UFAC_STR,
		SFAC_STR, MFAC_STR,  EFAC_STR,  CFAC_STR,    RFAC_STR,
		HFAC_STR, REFAC_STR, DIFAC_STR, ORCAFAC_STR, "u14",
		"u15",    "u16",     "u17",     "u18",       "u19" };

static int SNO_default_fac = REC_FAC;

/*
 * SNO_seterr_level( level, facility ) -
 * sets the current error level to level for facility.  This is used in 
 * deciding what error messages to print.  It returns the old error level.
 * If facility is not in range, it returns -1.  
 */
int
SNO_seterr_level( int level, enum ERR_FACS facility )
{
   int old;

   if ( facility >= 0 && facility < MAX_FACILITY ) {
      old = SNO_err_levels[ facility ];
      SNO_err_levels[ facility ] = level;
   } else {
      fprintf( stderr, "SNO_seterr_level: Invalid facility (%d)\n", facility );
      old = -1;
   }

   return old;
}

/*
 * SNO_geterr_level( void ) -
 * gets the current error level 
 */
int
SNO_geterr_level( enum ERR_FACS facility )
{
  return SNO_err_levels[ facility ];
}

/*
 * SNO_seterr_output( output, facility ) -
 * sets the current error output destination to output for facility.  This
 * is used in deciding where error messages are print.  It returns the old
 * output destination.  output is a bitmasked value so it is possible to
 * send to several distinations.
 * If facility is not in range, it returns -1.  
 */
int
SNO_seterr_output( int output, enum ERR_FACS facility )
{
   int old;

   if ( facility >= 0 && facility < MAX_FACILITY ) {
      old = SNO_err_output[ facility ];
      SNO_err_output[ facility ] = output;
   } else {
      fprintf( stderr, "SNO_seterr_output: Invalid facility (%d)\n", facility);
      old = -1;
   }

   return old;
}

/*
 * SNO_printerr( level, facility, string ) -
 * if the current error level for facility is greater than or equal to
 * level, print out string in the fashion difined by SNO_output.  A
 * newline will *NOT* be provided.
 */
void
SNO_printerr( int level, enum ERR_FACS facility, char *string )
{
   char fac[4096];
   time_t now;
   int num, len;
   struct tm *date;
   double the_time;
   
   int slvl = SNO_err_levels[facility];
   if ( level > slvl )
      return;

   if ( facility < 0 && facility > MAX_FACILITY ) {
      fprintf( stderr, "SNO_printerr: Invalid facility (%d)\n", facility );
      fprintf( stderr, "%s", string );
      return;
   }

   if ( level > PERMANENT_LEVEL ) {
     // record time of this call
     the_time = double_time();
#ifdef __MAXIMUM_LINES__
     if( (the_time >= interval_time[facility] + SNO_PRINTF_INTERVAL) || 
     	(interval_time[facility]==0) )
     {
     	interval_time[facility] = the_time;
     	messages_printed_in_this_interval[facility] = 0;
     }
     if( messages_printed_in_this_interval[facility] < MAX_SNO_PRINTF_NUM || slvl >= 99)
     	messages_printed_in_this_interval[facility]++;
     else {
       ++skipped_printf[facility];
       return;
     }
#else // __MAXIMUM_LINES__
     printf_call_times[printf_call_pt++] = the_time;
     if (printf_call_pt >= MAX_SNO_PRINTF_NUM) printf_call_pt = 0;
     if (the_time - printf_call_times[printf_call_pt] < SNO_PRINTF_INTERVAL) {
       if (skipped_printf[facility] || (++sample_printf[facility]>MESSAGE_SAMPLE_NUM && slvl < 99) {
	 ++skipped_printf[facility];
	 return;
       }
     }
#endif // __MAXIMUM_LINES__
   }
   
   if ( (num = skipped_printf[facility]) != 0 ) {
     skipped_printf[facility] = 0;
     sample_printf[facility] = 0;
     len = sprintf(fac,"[...%s skipped %d messages]\n", SNO_fac_string[facility], num);
   } else {
     len = 0;
   }
   
   now = time(NULL);
   date = localtime(&now);
   sprintf( fac + len, "%d%02d%02d %02d:%02d:%02d %s: %s",
   		date->tm_year+1900, date->tm_mon+1, date->tm_mday, date->tm_hour, date->tm_min, date->tm_sec,
   		SNO_fac_string[facility],  string );

   if ( SNO_err_output[facility] & T_STDERR )
      SNO_output_stderr( fac );
   
   if ( SNO_err_output[facility] & T_FILE )
      SNO_output_file_puts( fac );

   return;
}

/*
 * SNO_output_stderr( string ) -
 * prints out string as "string" on stderr
 */
static void
SNO_output_stderr( char *string )
{
   fputs( string, stderr );
   fflush( stderr );

   return;
}

static FILE *fd=(FILE *) NULL;
static char *out_fname;

/*
 * SNO_output_fname( string ) -
 * use string as filename of output file if using T_FILE.  Must be called
 * before the first SNO_printerr to a T_FILE, otherwise it is ignored.
 *
 * P.T. Keener  14 April 96
 */
void
SNO_output_fname( char *string )
{
   if ( fd == (FILE *) NULL )
   {
      if ( out_fname != (char *) NULL )
	 free( out_fname );
      out_fname = strdup( string );
   }

   return;

}

/*
 * SNO_output_file_open( char *mode ) -
 * opens output file with specified mode
 * PH 03/10/98
 */
void
SNO_output_file_open( char *mode )
{
   if ( fd != (FILE *) NULL )
   {
     fclose(fd);
   }
   if ( out_fname == (char *) NULL )
        out_fname = strdup( "run.log" );

   fd = fopen( out_fname, mode );

   if ( fd == (FILE *) NULL )
   {
     fprintf( stderr, "Unable to open file %s", out_fname );
     perror( " " );

     fprintf( stderr, "Opening /dev/null instead\n" );

     fd = fopen( "/dev/null", mode );
     if ( fd == (FILE *) NULL )
     {
       fprintf( stderr, "Unable to open /dev/null" );
       perror( " " );
     }
   }
}

/*
 * SNO_output_file_puts( string ) -
 * prints out string as "string" to current output file
 */
void
SNO_output_file_puts( char *string )
{
   if ( fd == (FILE *) NULL )
   {
      SNO_output_file_open( "w" );
   }

   fputs( string, fd );
   fflush( fd );
}

void
SNO_output_file_close( void )
{

  if ( fd != (FILE *) NULL ) {
      fclose( fd );
      fd = NULL;
  }

   return;
}


void
SNO_printf( int level, enum ERR_FACS facility, char *format, ... )
{
   int num, len;
   char final[4096];
   va_list ap;
   time_t now;
   struct tm *date;
   double the_time;
   
   if ( facility < 0 && facility > MAX_FACILITY ) {
      fprintf( stderr, "SNO_printf: Invalid facility (%d)\n", facility );
      va_start(ap,format );
      vfprintf( stderr, format, ap );
      va_end(ap);
      return;
   }

   int slvl = SNO_err_levels[facility];
   if ( level > slvl )
      return;
   
   if ( level > PERMANENT_LEVEL ) {
     // record time of this call
     the_time = double_time();
#ifdef __MAXIMUM_LINES__
     if( (the_time >= interval_time[facility] + SNO_PRINTF_INTERVAL) || 
     	(interval_time[facility]==0) )
     {
     	interval_time[facility] = the_time;
     	messages_printed_in_this_interval[facility] = 0;
     }
     if( messages_printed_in_this_interval[facility] < MAX_SNO_PRINTF_NUM || slvl >= 99 )
     	messages_printed_in_this_interval[facility]++;
     else {
       ++skipped_printf[facility];
       return;
     }
#else // __MAXIMUM_LINES__
     printf_call_times[printf_call_pt++] = the_time;
     if (printf_call_pt >= MAX_SNO_PRINTF_NUM) printf_call_pt = 0;
     if (the_time - printf_call_times[printf_call_pt] < SNO_PRINTF_INTERVAL) {
       if (skipped_printf[facility] || ++sample_printf[facility]>MESSAGE_SAMPLE_NUM && slvl < 99) {
	 ++skipped_printf[facility];
	 return;
       }
     }
#endif // __MAXIMUM_LINES__
   }
   
   
   if ( (num = skipped_printf[facility]) != 0 ) {
     skipped_printf[facility] = 0;
     sample_printf[facility] = 0;
     len = sprintf(final,"[...%s skipped %d messages]\n", SNO_fac_string[facility], num);
   } else {
     len = 0;
   }
	 
   // print facility and error level information as well as date and time
   now = time(NULL);
   date = localtime(&now);
   len += sprintf( final+len, "%d%02d%02d %02d:%02d:%02d %s.%d: ",
       date->tm_year+1900, date->tm_mon+1, date->tm_mday, date->tm_hour, date->tm_min, date->tm_sec,
       SNO_fac_string[facility], level);

   // add formated user printout
   va_start(ap,format );
   (void) vsprintf(final+len, format, ap);
   va_end(ap);

   if ( SNO_err_output[facility] & T_STDERR )
      SNO_output_stderr( final );
   
   if ( SNO_err_output[facility] & T_FILE )
      SNO_output_file_puts( final );
}

// Printf - print level 0 message for default facility
void Printf( char *format, ... )
{
   int num, len, facility = SNO_default_fac;
   char final[4096];
   va_list ap;
   time_t now;
   struct tm *date;
   double the_time;
   
   if ( (num = skipped_printf[facility]) != 0 ) {
     skipped_printf[facility] = 0;
     sample_printf[facility] = 0;
     len = sprintf(final,"[...skipped %d messages]\n", num);
   } else {
     len = 0;
   }
	 
   // print facility and error level information as well as date and time
   now = time(NULL);
   date = localtime(&now);
   len += sprintf( final+len, "%d%02d%02d %02d:%02d:%02d %s.%d: ",
       date->tm_year+1900, date->tm_mon+1, date->tm_mday, date->tm_hour, date->tm_min, date->tm_sec,
       REFAC_STR, 0);

   // add formated user printout
   va_start(ap,format );
   (void) vsprintf(final+len, format, ap);
   va_end(ap);

   if (SNO_err_output[facility] & T_STDERR) SNO_output_stderr( final );
   if (SNO_err_output[facility] & T_FILE) SNO_output_file_puts( final );
}
