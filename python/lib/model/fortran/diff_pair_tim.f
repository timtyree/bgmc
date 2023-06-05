      implicit real*8  (a-h,o-z)
      integer n
      parameter (n=1000)
      integer i,j,iter,niter
      character*80 filename
      real*8 x(n)
      real*8 y(n)
      real*8 xn(n)
      real*8 yn(n)
      real*8 dmin(3)
      real*8 dist(n,n)
      real*8 dis_x(n,n)
      real*8 dis_y(n,n)
      integer iremove(n)
      real*8 rate(n)
      integer*4 timeArray(3)

c random seed generator
      call itime(timeArray)     ! Get the current time
      i =  (24*timeArray(1)+60*timeArray(2)+3600*timeArray(3) )
      idum=-i

c input file
        filename='input_diff'
        open(unit=77,file=filename,status='unknown')
        read(77,*)diff
        read(77,*)dt,tmod
        read(77,*)tmax,itot
        read(77,*)a_att,rad,xkappa
        read(77,*)xl,n_num,ico_stop

        prob=xkappa*dt
        xisq=sqrt(2.*dt*diff)
        niter=int(tmax/dt)
        imod=int(tmod/dt)
        threshold=0.5

        xl2=xl*xl
        i_iter=0
        do i=1,n
          rate(i)=0.
        enddo

c i_iter counts the number of independent simulations
901     continue
        i_iter=i_iter+1

c random placement of particles
        do i=1,n_num
          x(i)=ran2_new(idum)*xl
          y(i)=ran2_new(idum)*xl
          iremove(i)=0
        enddo
        ico=n_num
        tprev=0.

c compute distance between part. i and j; take into account pb conditions
        do i=1,n_num
        do j=i+1,n_num
           dmin(1)=abs(x(i)-x(j))
           dmin(2)=abs(x(i)+xl-x(j))
           dmin(3)=abs(x(i)-xl-x(j))
           call find_min(dmin,xmin,facx,xl)
           dis_x(i,j)=x(i)+facx-x(j)
           dmin(1)=abs(y(i)-y(j))
           dmin(2)=abs(y(i)+xl-y(j))
           dmin(3)=abs(y(i)-xl-y(j))
           call find_min(dmin,xmin,facy,xl)
           dis_y(i,j)=y(i)+facy-y(j)
           dist(i,j)=(x(i)+facx-x(j))**2+(y(i)+facy-y(j))**2
        enddo
        enddo

        do i=1,n_num
        do j=i+1,n_num
           dist(j,i)=dist(i,j)
           dis_x(j,i)=-dis_x(i,j)
           dis_y(j,i)=-dis_y(i,j)
        enddo
        enddo

c compute force sum
      do iter=1,niter
        do i=1,n_num
          if (iremove(i).eq.1) go to 600
          sum_att_x=0.
          sum_att_y=0.
          do j=1,n_num
             if (iremove(j).eq.1) go to 601
             if (j.ne.i) then
                sum_att_x=sum_att_x-dt*a_att*dis_x(i,j)/dist(i,j)
                sum_att_y=sum_att_y-dt*a_att*dis_y(i,j)/dist(i,j)
             endif
601          continue
           enddo
c add diffusive term
           xran=gasdev(idum)
           xn(i)=x(i)+xisq*xran+sum_att_x
           xran=gasdev(idum)
           yn(i)=y(i)+xisq*xran+sum_att_y
600        continue
        enddo

c figure out if particle has left the box
        do i=1,n_num
           if (iremove(i).eq.1) go to 610
           if (xn(i).gt.xl) then
             x(i)=xn(i)-xl
           else
             if (xn(i).lt.0.) then
                x(i)=xn(i)+xl
             else
                x(i)=xn(i)
             endif
           endif
           if (yn(i).gt.xl) then
             y(i)=yn(i)-xl
           else
             if (yn(i).lt.0.) then
                y(i)=yn(i)+xl
             else
                y(i)=yn(i)
             endif
           endif
610        continue
        enddo

c recompute distances
        do i=1,n_num
        if (iremove(i).eq.1) go to 620
        do j=i+1,n_num
           if (iremove(j).eq.1) go to 621
           dmin(1)=abs(x(i)-x(j))
           dmin(2)=abs(x(i)+xl-x(j))
           dmin(3)=abs(x(i)-xl-x(j))
           call find_min(dmin,xmin,facx,xl)
           dis_x(i,j)=x(i)+facx-x(j)
           dmin(1)=abs(y(i)-y(j))
           dmin(2)=abs(y(i)+xl-y(j))
           dmin(3)=abs(y(i)-xl-y(j))
           call find_min(dmin,xmin,facy,xl)
           dis_y(i,j)=y(i)+facy-y(j)
           dist(i,j)=(x(i)+facx-x(j))**2+(y(i)+facy-y(j))**2
621        continue
        enddo
620     continue
        enddo

        do i=1,n_num
        if (iremove(i).eq.1) go to 630
        do j=i+1,n_num
           if (iremove(j).eq.1) go to 631
           dist(j,i)=dist(i,j)
           dis_x(j,i)=-dis_x(i,j)
           dis_y(j,i)=-dis_y(i,j)
631        continue
        enddo
630     continue
        enddo

c determine if particle should be removed
        do i=1,n_num
        if (iremove(i).eq.1) go to 800
         do j=i+1,n_num
           if (iremove(j).eq.1) go to 801
           if (sqrt(dist(i,j)).le.rad) then
             xran=ran2_new(idum)
             if (xran.le.prob) then
c remove particl pair
                iremove(i)=1
                iremove(j)=1
                rate(ico)=iter*dt-tprev+rate(ico)
                ico=ico-2
                tprev=iter*dt
c stop if number of tips has reached ico_stop
                if (ico.eq.ico_stop) go to 900
             endif
           endif
801        continue
         enddo
800      continue
        enddo
           
      enddo

900   continue
      if (i_iter.le.itot) go to 901

c compute rates
      do i=ico_stop+2,n_num,2
         rate(i)=rate(i)/itot
         if (rate(i).ne.0.) then
           write(80,*)i,1./rate(i),rate(i)
           write(81,*)i/xl2,1./(xl2*rate(i))
         endif
      enddo


      end

      REAL*8 FUNCTION GASDEV(IDUM)
      implicit real*8(a-h,o-z)
C
      SAVE FAC,GSET,ISET,R,V1,V2
C
      DATA ISET/0/
C
      IF (ISET.EQ.0) THEN
c1       V1=2.D0*RAN2(IDUM)-1.
c        V2=2.D0*RAN2(IDUM)-1.
1       V1=2.D0*ran2_new(idum)-1.d0
        V2=2.D0*ran2_new(idum)-1.d0
        R=V1**2+V2**2
        IF(R.GE.1.0)GO TO 1
        FAC=SQRT(-2.0*LOG(R)/R)
        GSET=V1*FAC
        GASDEV=V2*FAC
        ISET=1
      ELSE
        GASDEV=GSET
        ISET=0
      ENDIF
      RETURN
      END

      FUNCTION ran2_new(idum)
      implicit real*8(a-h,o-z)
C
C     Long period (>2E18) random number generator of L'Ecuyer with
C     Bays-Durham shuffle and added safeguards.
C     Returns a uniform random deviate between 0.0 and 1.0 (endpoints
C     excluded). 
C
C     Call with IDUM a negative integer to initialize. Thereafter
C     IDUM shouln't be altered between subsequent calls.
C     RNMX should approximate the largest floating value that is less than 1.
C
C---------------------------------------------------------------------------
      INTEGER idum,IM1,IM2,IMM1,IA1,IA2,IQ1,IQ2,IR1,IR2,NTAB,NDIV
      real*8 ran2,AM,EPS,RNMX
      
      PARAMETER (IM1=2147483563,IM2=2147483399,AM=1.d0/IM1,IMM1=IM1-1,
     *IA1=40014,IA2=40692,IQ1=53668,IQ2=52774,IR1=12211,IR2=3791,
     *NTAB=32,NDIV=1+IMM1/NTAB,EPS=1.2d-7,RNMX=1.d0-EPS)
      
      INTEGER idum2,j,k,iv(NTAB),iy
      SAVE iv,iy,idum2
      DATA idum2/123456789/, iv/NTAB*0/, iy/0/
C-----Initialize
      if (idum.le.0) then
        idum=max(-idum,1)                  ! prevents IDUM=0
        idum2=idum
        do 11 j=NTAB+8,1,-1                ! load the shuffle table
          k=idum/IQ1
          idum=IA1*(idum-k*IQ1)-k*IR1
          if (idum.lt.0) idum=idum+IM1
          if (j.le.NTAB) iv(j)=idum
11      continue
        iy=iv(1)
      endif

C-----Start here if not initializing
      k=idum/IQ1
      idum=IA1*(idum-k*IQ1)-k*IR1          ! Computes IDUM = MOD(IA1*IDUM,IM1)
      if (idum.lt.0) idum=idum+IM1
      k=idum2/IQ2
      idum2=IA2*(idum2-k*IQ2)-k*IR2        ! IDUM2 = MOD(IA2*IDUM2,IM2)
      if (idum2.lt.0) idum2=idum2+IM2
      j=1+iy/NDIV                          ! J in range 1:NTAB
C-----IDUM is shuffled, IDUM and IDUM2 are combined to compute RAN2
      iy=iv(j)-idum2
      iv(j)=idum
      if(iy.lt.1)iy=iy+IMM1                
      ran2_new=min(AM*iy,RNMX)                 ! to avoid endpoint values
        
      return
      END 
          

      SUBROUTINE find_min(dmin,xmin,fac,xl)
      implicit real*8(a-h,o-z)
      real*8 dmin(3)

      xmin=2.*xl
      do i=1,3
         if (dmin(i).lt.xmin) then
            xmin=dmin(i)
            imin=i
         endif
      enddo
      if (imin.eq.1)then
        fac=0.
      else
        if (imin.eq.2)  then
          fac=xl
        else
          fac=-xl
        endif
      endif

      return
      end
