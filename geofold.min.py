import math
class PT:
 def __init__(self,x,y):self.c=complex(x,y)
 def __str__(self):return"PT({}, {})".format(self.c.real,self.c.imag)
 def __eq__(self,o):return self.c==o.c
 def __hash__(self):return hash(self.c)
 def __repr__(self):return str(self)
 @property
 def x(self):return self.c.real
 @property
 def y(self):return self.c.imag
 def dist(self,o):
  if type(o)==PT:return abs(self.c-o.c)
  if type(o)==LN:return abs(o.project(self))/math.sqrt(o.m**2+1)
class LN:
 def __init__(self,m,b):self.m=m;self.b=b
 def __str__(self):return"LN y = {}x + {}".format(self.m,self.b)
 def __eq__(self,o):return self.m==o.m and self.b==o.b
 def __hash__(self):return hash((self.m,self.intersect))
 def __repr__(self):return str(self)
 def project(self,s):return self.m*s.x-s.y+self.b
 def xtoy(self,x):return self.m*x+self.b
 def ytox(self,y):return(y-self.b)/self.m
 def intersect(self,o):
  if type(o)==LN:
   if self.m==o.m:return None
   x=(o.b-self.b)/(self.m-o.m);y=self.xtoy(x);return PT(x, y)
  if type(o)==SG:print("Error: Use line.intersect(segment.line) instead");exit(1)
  if type(o)==CC:
   A,B,C=self.m,-1,self.b;h,k,r=o.c.x,o.c.y,o.r;a=A**2+B**2;b=2*A*C+2*A*B*k-2*h*B**2;c=C**2+2*B*C*k-B**2*(r**2-h**2-k**2);z=b**2-4*a*c
   if z<0:return[]
   if z==0:x=-b/(2 * a);y=self.xtoy(x);return[PT(x, y)]
   return stp([PT((-b+math.sqrt(z))/(2*a),self.xtoy((-b+math.sqrt(z))/(2*a))),PT((-b-math.sqrt(z))/(2*a),self.xtoy((-b-math.sqrt(z))/(2*a)))])
 def perpendicular(self,s):return LN(-1/self.m,s.y-s.x*-1/self.m)
 def parallel(self,s):return LN(self.m,s.y-s.x*self.m)
ptln=lambda a,b:LN((b.y-a.y)/(b.x-a.x),a.y-a.x*(b.y-a.y)/(b.x-a.x))
def stp(v):
 if v[0].x>v[1].x:return[v[1],v[0]]
 if v[0].x == v[1].x and v[0].y > v[1].y:return[v[1],v[0]]
 return[v[0],v[1]]
class SG:
 def __init__(self,p1,p2):self.p1=p1;self.p2=p2
 def __str__(self):return"SG({}, {})".format(self.p1,self.p2)
 def __eq__(self,o):return self.p1==o.p1 and self.p2==o.p2
 @property
 def length(self):return self.p1.dist(self.p2)
 @property
 def line(self):return ptln(self.p1,self.p2)
 @property
 def midpt(self):return PT((self.p1.x+self.p2.x)/2,(self.p1.y+self.p2.y)/2)
class CC:
 def __init__(self,c,r):self.c=c;self.r=r
 def __str__(self):return"CC({}, {})".format(self.c,self.r)
 def __eq__(self,o):return self.c==o.c and self.r==o.r
 def xtoy(self,x):
  z=self.r**2-(x-self.c.x)**2
  if z<0:return[]
  if z==0:return[PT(x,self.c.y)]
  return stp([PT(x,self.c.y-math.sqrt(z)),PT(x,self.c.y+math.sqrt(z))])
 def intersect(self,o):
  if type(o)==LN:return o.intersect(self)
  if type(o)==SG:print("Error: Use circle.intersect(segment.line) instead");exit(1)
  if type(o)==CC:
   x0,y0,r0=self.c.x,self.c.y,self.r;x1,y1,r1=o.c.x,o.c.y,o.r;d=math.sqrt((x1-x0)**2+(y1-y0)**2);a=(r0**2-r1**2+d**2)/(2*d);h=math.sqrt(r0**2-a**2);x2=x0+a*(x1-x0)/d;y2=y0+a*(y1-y0)/d;x3_1=x2+h*(y1-y0)/d;y3_1=y2-h*(x1-x0)/d;x3_2=x2-h*(y1-y0)/d;y3_2=y2+h*(x1-x0)/d
   if x3_1==x3_2 and y3_1==y3_2:return[PT(x3_1,y3_1)]
   return stp([PT(x3_2,y3_2),PT(x3_1,y3_1)])

ORIGIN = PT(0,0)

if __name__ == "__main__":
    C1 = CC(ORIGIN, 200)
    E = PT(200, 0)
    C2 = CC(E, 180)
    C3 = CC(E, 108)
    D = C1.intersect(C2)[0]
    K = C3.xtoy(D.x)[0]
    EK = ptln(E, K)
    F = C1.intersect(EK)[0]
    print(F.dist(K))
