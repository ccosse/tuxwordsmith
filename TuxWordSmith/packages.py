"""
/***************************************************************************

	Author			:Charles B. Cosse 
	
	Email			:ccosse@gmail.com
					
	Website			:www.asymptopia.org
	
	Copyright		:(C) 2002-2007 Asymptopia Software.
	
 ***************************************************************************/
"""
from math import *
pi=acos(-1.)

def mkpkgs(w,h):
		pkgs=[]
		
		twopi=2.*pi
		piov2=pi/2.
		desc='KA_BOOM_BOOM'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,    5, piov2,pi/30.,  30,  255, 000, 000, 000, 000, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 4.0, 0.0,    	2, 999, 999, 999, 999,  30,   10,     0, twopi,  30,  255, 000, 255, 000, 255, 000,  2,	  10, 20,  0, False,   True,   True],
			[ 5.0, 0.1,    	1, 999, 999, 999, 999,  50,   20,     0, twopi,  30,  200, 055, 000, 000, 255, 000,  2,	  10,  5,  2,  True,   True,   True],
		]
		pkgs.append({desc:package})
		
		
		desc='RED_RING_YELLOW_SPARKLES'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-155,   15, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  4,	  20,  1,  0, False,   True,  False],
			[ 3.5, 0.0,    	2, 999, 999, 999, 999, 030,   20,     0, twopi,  30,  255, 000, 000, 000, 000, 000,  2,	  25, 20,  5, False,   True,   True],
			[ 5.0, 0.1,    	1, 999, 999, 999, 999,  10,    2,     0, twopi,  30,  255, 000, 255, 000, 000, 000,  2,	   0, 10,  4, False,  False,   True],
		]
		pkgs.append({desc:package})
		
		
		desc='RED_ORANGE_ROCKET_CLUSTER_WITH_SPARKLES'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     1, w/2,   0,   h,   0,-180,   35, piov2,pi/20.,  30,  200, 000, 200, 000, 000, 000,  5,	  01, 01, 00, False,   False,   True],
			[ 2.5, 0.1,    	2, 999, 999, 999, 999,  10,    5,     0, twopi,  30,  200, 000, 100, 010, 000, 000,  3,	  10, 25, 01, False,    True,   True],
			[ 5.2, 0.0,    	1, 999, 999, 999, 999,  10,   10,     0, twopi,  30,  235, 020, 235, 020, 235, 020,  4,	  00, 15, 05, False,   False,   True],
		]
		pkgs.append({desc:package})
		
		desc='WHITE_EXPLOSION_RED_TRAILS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,  50,   h,   0,-170,    5, piov2, pi/8.,  30,  255, 000, 255, 000, 255, 000,  4,	  10,  1,  0, False,    True,  False],
			[ 2.5, 0.2,    	3, 999, 999, 999, 999,  04,    2,     0, twopi,  30,  255, 000, 255, 000, 255, 000,  4,	  20, 15,  2, False,    True,   True],
			[ 5.0, 0.0,    	1, 999, 999, 999, 999,  30,    0,     0, twopi,  30,  200, 055, 200, 055, 050, 050,  2,	   0, 10,  5, False,   False,  False],
		]
		pkgs.append({desc:package})
		
		desc='FEW_RED_TO_PURPLE_CLUSTERS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     2, w/2,   0,   h,   0,-160,    5, piov2,pi/10.,  30,  255, 000, 255, 000, 255, 000,  5,	   5,  1,  0, False,   True,   True],
			[ 3.5, 0.0,    	2, 999, 999, 999, 999,  30,   25,     0, twopi,  30,  255, 000, 000, 000, 000, 000,  2,	   0, 20, 10, False,  False,   True],
			[ 3.6, 0.0,    	1, 999, 999, 999, 999,   0,    0,     0,     0,  30,  100, 000, 100, 000, 255, 000,  3,	  20, 01,  0, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='BLUE_BLAST_WTAILS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-155,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 4.0, 0.0,    	3, 999, 999, 999, 999,  80,   10,     0, twopi,  30,  100, 055, 100, 055, 255, 000,  3,	  15, 50, 20, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='WHITE_BLAST_WTAILS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-155,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 4.0, 0.0,    	3, 999, 999, 999, 999,  80,   10,     0, twopi,  30,  255, 000, 255, 000, 255, 000,  3,	  15, 50, 20, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='RED_BLAST_WTAILS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-155,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 4.0, 0.0,    	3, 999, 999, 999, 999,  50,   50,     0, twopi,  30,  255, 000, 000, 000, 000, 000,  3,	  15, 50, 20, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='REDRING_TO_WHITETIP'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     1, w/2,   0,   h,   0,-155,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	   0,  1,  0, False,  False,  False],
			[ 3.0,  .1,    	3, 999, 999, 999, 999,  50,    0,     0, twopi,  30,  255, 000, 000, 000, 100, 100,  3,	  20, 30, 15,  True,   True,  False],
			[ 4.5,  .1,    	2, 999, 999, 999, 999,  10,    1,     0, twopi,  30,  200, 000, 255, 000, 200, 000,  3,	  03, 02, 01, False,   True,   True],
		]
		pkgs.append({desc:package})
		
		desc='WHITE_TIPPED_BOUQUET'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.0,     1, w/2,   0,   h,   0,-160,    5, piov2,pi/30.,  30,  155, 100, 155, 100, 155, 100,  5,	  30,  1,  0, False,   True,  False],
			[ 2.6, 0.0,     2, 999, 999, 999, 999,   5,    5,	  0, twopi,  30,  155, 100, 155, 100, 155, 100,  2,    5,  5,  1, False,   True,   True],
			[ 4.0, 0.2,    	2, 999, 999, 999, 999,   3,    3,     0, twopi,  30,  255, 000, 255, 000, 255, 000,  4,	   8, 10,  5, False,   True,  False],
		]
		pkgs.append({desc:package})

		desc='SWARM'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-155,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 3.0, 0.1,    	2, 999, 999, 999, 999,  10,   05,     0, twopi,  30,  000, 000, 000, 000, 200, 000,  3,	   5, 20, 10,  True,   True,   True],
			[ 4.5, 0.1,    	1, 999, 999, 999, 999,  40,    0,     0, twopi,  30,  255, 000, 255, 000, 255, 000,  2,   10,  5,  1,  True,   True,   True],
		]
		pkgs.append({desc:package})

		
		"""		
		
		
		desc='BLUGRN_RING_BLAST_WTAILS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 4.2, 0.2,    	3, 999, 999, 999, 999, 050,   10,     0, twopi,  30,  010, 010, 245, 010, 245, 010,  5,	  10, 50,  0, False,   True,  False],
		]
		pkgs.append({desc:package})
		
		desc='RED_BLAST_WTAILS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  20,  1,  0, False,  False,  False],
			[ 4.2, 0.0,    	3, 999, 999, 999, 999,  50,   30,     0, twopi,  30,  245, 010, 035, 010, 000, 000,  3,	  10, 55,  1, False,   True,   False],
		]
		pkgs.append({desc:package})

		
		desc='REDRING_TO_BLUETIP'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     1, w/2,   0,   h,   0,-180,   20, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	   0,  1,  0, False,  False,  False],
			[ 3.0,  .1,    	3, 999, 999, 999, 999,  50,    0,     0, twopi,  30,  255, 000, 000, 000, 100, 100,  3,	  20, 30, 15,  True,   True,  False],
			[ 4.5,  .1,    	2, 999, 999, 999, 999,  10,   10,     0, twopi,  30,  000, 000, 000, 000, 200, 020,  3,	  03, 02, 01, False,   True,   True],
		]
		pkgs.append({desc:package})
		
		desc='COLORLOCK_RING'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.0,     1, w/2,   0,   h,   0,-180,   20, piov2,pi/30.,  30,  155, 100, 155, 100, 155, 100,  5,	  30,  1,  0, False,   True,  False],
			[ 4.0, 0.1,     2, 999, 999, 999, 999,  30,    0,	  0, twopi,  30,  155, 100, 155, 100, 155, 100,  3,   30, 30,  5,  True,   True,   True],
			[ 5.0, 0.0,    	2, 999, 999, 999, 999,  10,   10,     0, twopi,  30,  155, 100, 155, 100, 155, 100,  2,	   5,  3,  1, False,   True,   True],
		]
		pkgs.append({desc:package})
		
		desc='RED_TO_BLUE'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.1,     1, w/2,   0,   h,   0,-180,   20, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  30,  1,  0, False,   True,  False],
			[ 2.0, 0.1,    	2, 999, 999, 999, 999,  10,   10,	  0, twopi,  30,  255, 000, 000, 000, 000, 000,  3,	   0, 20,  5, False,  False,   True],
			[ 3.5, 0.0,    	2, 999, 999, 999, 999,   5,    5,     0, twopi,  30,  000, 000, 000, 000, 255, 000,  3,	  10,  5,  1, False,   True,   True],
		]
		pkgs.append({desc:package})
		
		desc='2xEFFICIENT_CLUSTER'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,    5, piov2,pi/30.,  30,  255, 000, 255, 000, 255, 000,  3,	  20,  1,  0, False,  False,  False],
			[ 2.7, 0.3,    	3, 999, 999, 999, 999,   3,    2,     0, twopi,  30,  200, 055, 200, 055, 200, 055,  3,	  40, 20,  5, False,   True,   True],
		]
		pkgs.append({desc:package})

		
		"""
		"""
		###############BELOW ARE FROM MSTATION 0.4:
		desc='TEST'#'2xEFFICIENT_CLUSTER_BLOW'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,   15, pi/2.,pi/20.,  30,  200, 055, 200, 000, 000, 000,  5,	  30,  1,  0, False,   True,   True],
			[ 4.0, 0.1,    	2, 999, 999, 999, 999,  30,    5,     0, 2.*pi,  30,  255, 000, 000, 000, 000, 000,  2,	   2, 10,  5, False,  False,   True],
			[ 5.2, 0.5,    	2, 999, 999, 999, 999,   5,    2,     0, 2.*pi,  30,  200, 055, 000, 000, 200, 055,  3,	  20, 10,  5, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='FEW_RED_TO_PURPLE_CLUSTERS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,   15, pi/2.,pi/20.,  30,  200, 055, 200, 000, 000, 000,  5,	  30,  1,  0, False,   True,   True],
			[ 4.0, 0.1,    	2, 999, 999, 999, 999,  30,    5,     0, 2.*pi,  30,  255, 000, 000, 000, 000, 000,  2,	   2, 10,  5, False,  False,   True],
			[ 5.2, 0.5,    	2, 999, 999, 999, 999,   5,    2,     0, 2.*pi,  30,  000, 000, 200, 055, 200, 055,  3,	  20, 10,  5, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='FEW_GREEN_TO_RED_CLUSTERS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,   15, pi/2.,pi/20.,  30,  200, 055, 200, 000, 000, 000,  5,	  30,  1,  0, False,   True,   True],
			[ 4.0, 0.1,    	2, 999, 999, 999, 999,  30,    5,     0, 2.*pi,  30,  000, 000, 200, 055, 100, 055,  2,	   2, 10,  5, False,  False,   True],
			[ 5.2, 0.5,    	2, 999, 999, 999, 999,   5,    2,     0, 2.*pi,  30,  255, 000, 100, 055, 100, 055,  3,	  20, 10,  5, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='GREEN_PUFF_DUD'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-200,    5, pi/2.,pi/30.,  30,  000, 000, 255, 000, 000, 000,  5,	  60,  1,  0, False,   True,   True],
			[ 4.5, 0.2,    	4, 999, 999, 999, 999,   2,    0,     0, 2.*pi,  30,  000, 000, 200, 055, 100, 055,  4,	  50, 10,  5, False,   True,   True],
		]
		pkgs.append({desc:package})

		desc='2xEFFICIENT_CLUSTER_BLOW'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,    5, pi/2.,pi/30.,  30,  255, 000, 255, 000, 255, 000,  3,	  20,  1,  0, False,  False,  False],
			[ 2.7, 0.3,    	3, 999, 999, 999, 999,   3,    2,     0, 2.*pi,  30,  200, 055, 200, 055, 200, 055,  2,	  40, 20,  5, False,   True,   True],
			[ 4.5, 0.0,    	2, 999, 999, 999, 999,  50,   30,     0, 2.*pi,  30,  100, 055, 100, 055, 255, 000,  4,	  15,  5,  1, False,   True,   False],
		]
		pkgs.append({desc:package})

		desc='4x'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     3, w/2,   0,   h,   0,-180,    5, pi/2.,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  40,  1,  0, False,  False,  False],
			[ 2.5, 0.3,    	2, 999, 999, 999, 999,  30,   30,     0, 2.*pi,  30,  200, 055, 100, 055, 200, 055,  3,	  20,  7,  1, False,   True,   True],
			[ 3.3, 0.2,    	2, 999, 999, 999, 999,  20,   15,     0, 2.*pi,  30,  200, 055, 200, 055, 200, 055,  2,	   5,  8,  1,  True,   True,   True],
			[ 5.0, 0.2,    	2, 999, 999, 999, 999,   0,    0,     0, 2.*pi,  30,  255, 000, 255, 000, 255, 000,  3,	   5,  1,  0, False,   True,   True],
		]
		pkgs.append({desc:package})

		
		desc='REDRING_TO_WHITETIP'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0,  .1,     1, w/2,   0,   h,   0,-180,   20, pi/2.,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	   0,  1,  0, False,  False,  False],
			[ 3.0,  .1,    	2, 999, 999, 999, 999,  50,    0,     0, 2.*pi,  30,  255, 000, 000, 000, 100, 100,  3,	  30, 30, 15,  True,   True,  False],
			[ 4.5,  .1,    	3, 999, 999, 999, 999,  10,   10,     0, 2.*pi,  30,  255, 000, 155, 100, 000, 000,  3,	  10,  2,  1, False,   True,   True],
		]
		pkgs.append({desc:package})

		
		desc='RED_TO_BLUE'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.1,     1, w/2,   0,   h,   0,-180,   20, pi/2.,pi/30.,  30,  255, 000, 255, 000, 255, 000,  5,	  30,  1,  0, False,   True,  False],
			[ 2.0, 0.1,    	2, 999, 999, 999, 999,  10,   10,	  0, 2.*pi,  30,  255, 000, 000, 000, 000, 000,  3,	   0, 20,  5, False,  False,   True],
			[ 3.5, 0.0,    	2, 999, 999, 999, 999,   5,    5,     0, 2.*pi,  30,  000, 000, 000, 000, 255, 000,  3,	  10,  5,  1, False,   True,   True],
		]
		pkgs.append({desc:package})
		
		desc='REDTAILS_TO_COLORLOCK_PUFFS'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.1,     1, w/2,   0,   h,   0,-180,   20, pi/2.,pi/30.,  30,  000, 000, 255, 000, 000, 000,  5,	  30,  1,  0, False,   True,  False],
			[ 3.5, 0.0,    	2, 999, 999, 999, 999,  20,   20,	  0, 2.*pi,  30,  255, 000, 000, 000, 000, 000,  3,    5, 30,  5, False,   True,   True],
			[ 4.5, 0.1,    	2, 999, 999, 999, 999,  10,   10,     0, 2.*pi,  30,  155, 100, 155, 100, 155, 100,  3,	   0,  5,  2, False,  False,   True],
		]
		pkgs.append({desc:package})
		
		desc='COLORLOCK_RING'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.0,     1, w/2,   0,   h,   0,-180,   20, pi/2.,pi/30.,  30,  155, 100, 155, 100, 155, 100,  5,	  30,  1,  0, False,   True,  False],
			[ 4.0, 0.1,     2, 999, 999, 999, 999,  30,    0,	  0, 2.*pi,  30,  155, 100, 155, 100, 155, 100,  3,   30, 30,  5,  True,   True,   True],
			[ 5.0, 0.0,    	2, 999, 999, 999, 999,  10,   10,     0, 2.*pi,  30,  155, 100, 155, 100, 155, 100,  2,	   5,  3,  1, False,   True,   True],
		]
		pkgs.append({desc:package})
		
		desc='WHITE_TIPPED_BOUQUET'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.0,     1, w/2,   0,   h,   0,-180,   20, pi/2.,pi/30.,  30,  155, 100, 155, 100, 155, 100,  5,	  30,  1,  0, False,   True,  False],
			[ 2.6, 0.0,     2, 999, 999, 999, 999,   5,    5,	  0, 2.*pi,  30,  155, 100, 155, 100, 155, 100,  2,    5,  5,  1, False,   True,   True],
			[ 4.0, 0.2,    	2, 999, 999, 999, 999,   3,    3,     0, 2.*pi,  30,  255, 000, 255, 000, 255, 000,  4,	   8, 10,  5, False,   True,  False],
		]
		pkgs.append({desc:package})
		
		
		desc='COLORLOCK_BOUQUET'
		package=[
		# tblow,dtblow,radius,  x0, dx0,  y0, dy0,   v,   dv, theta,dtheta,  ay,    r,  dr,   g,  dg,   b,  db,ttl,   tl,  n, dn,  ring,   tail colorlock
			[ 0.0, 0.0,     1, w/2,   0,   h,   0,-180,   20, pi/2.,pi/30.,  30,  155, 100, 155, 100, 155, 100,  5,	  30,  1,  0, False,   True,  False],
			[ 2.2, 0.2,     2, 999, 999, 999, 999,  10,   10,	  0, 2.*pi,  30,  155, 100, 155, 100, 155, 100,  3,    5, 20,  5, False,  False,  True],
			[ 3.6, 0.1,    	2, 999, 999, 999, 999,  10,   10,     0, 2.*pi,  30,  155, 100, 155, 100, 155, 100,  4,	   7,  5,  3, False,   True,  True],
		]
		pkgs.append({desc:package})
		"""		
		return pkgs
		
