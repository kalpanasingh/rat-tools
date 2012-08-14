#ifndef __CUtil_h__
#define __CUtil_h__

#define REC_FAC		((enum ERR_FACS)11)
#define DISP_FAC	((enum ERR_FACS)12)
#define ORCA_FAC	((enum ERR_FACS)13)

#define REFAC_STR	"RE"
#define DIFAC_STR	"DI"
#define ORCAFAC_STR "OR"

#ifdef __cplusplus
extern "C" {
#endif

#include "sys_util/error.h"

// the code for this function is located in error_ph.c...
void	Printf(char *fmt, ...);

#ifdef __cplusplus
}
#endif

#endif // __CUtil_h__
