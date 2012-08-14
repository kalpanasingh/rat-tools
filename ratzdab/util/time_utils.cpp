#include <time.h>

/*
 * get current time in seconds using system clock - PH 02/01/98
 * (rumoured to be accurate to about 25ms)
 */
double double_time() {
#ifdef USE_FTIME
        /* support for systems without clock_gettime() - PH 08/12/98 */
        struct timeb tb;
        ftime(&tb);
        return(tb.time + 1e-3 * tb.millitm);
#elif defined(USE_GETTIMEOFDAY)
        /* add support for systems without clock_gettime() or ftime() - PH 01/20/99 */
        struct timeval tv;
        struct timezone tz;
        gettimeofday(&tv,&tz);
        return(tv.tv_sec + 1e-6 * tv.tv_usec);
#else
        struct timespec ts;
        /* (rumoured to be accurate to about 25ms) */
        clock_gettime(CLOCK_REALTIME, &ts);
        return(ts.tv_sec + 1e-9 * ts.tv_nsec);
#endif
}

