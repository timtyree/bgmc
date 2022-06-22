        PROGRAM eval
        implicit real*8(a-h,o-z)
        parameter(n=10000)
        parameter(nmax=100)
        dimension x(n)
        dimension y(n)
        dimension sig(n)
        dimension a(nmax)
        dimension dyda(nmax)
        dimension ia(nmax)
        dimension covar(nmax,nmax)
        dimension alpha(nmax,nmax)
        character*80 filename1,filename2
        external funcs
        common/per/omega

        pi=4.d0*datan(1.d0)
        twopi=2.d0*pi
        del=2.*pi/50.
        omega=0.035

        open(unit=70,file='dd_lr',status='unknown')

        do j=1,n
            sig(j)=1.0
            read(70,*,end=990)x(j),y(j)
            y(j)=y(j)*1000.
c           read(70,*,end=990)xx,yy
c           x(j)=log(xx)
c           y(j)=log(yy)
            write(71,*)x(j),y(j)
        enddo
990     ndata=j-1

        ma=3
        do i=1,ma
          a(i)=0.1
          ia(i)=1
        enddo

        thresh=5.e-3
        a0=0.1
        a(1)=3.
        a(2)=4.0
        a(3)=0.57

        dela=0
        do k=1,1

          do i1=1,nmax
          do i2=1,nmax
            covar(i1,i2)=0.
            alpha(i1,i2)=0.
          enddo
          enddo
          chisq=0.

          alamda=-1.
          nca=nmax

            call mrqmin(x,y,sig,ndata,a,ia,ma,covar,alpha,nca,chisq,
     *        funcs,alamda)
            alamda_prev=alamda

          niter=10
          do i=1,niter
            call mrqmin(x,y,sig,ndata,a,ia,ma,covar,alpha,nca,chisq,
     *        funcs,alamda)
            write(6,*)a(1),chisq
c           if (alamda.gt.2.*alamda_prev) then
c                   go to 777
c           endif
          enddo

777       continue

c         if (i.eq.niter+1) then
            do i=1,ndata
              call funcs(x(i),a,ymod,dyda,ma)
              write(74,*)x(i),ymod,y(i)
              write(77,*)exp(x(i)),exp(ymod),exp(y(i))
              write(76,*)x(i),y(i)-ymod,ymod
            enddo
            write(75,*)a(1),a(2),a(3),chisq
            write(6,*)a(1),a(2),a(3),chisq
        gamma=20.
        alinear=a(1)+a(2)/(1.+gamma**2*omega**2)
        period=twopi/omega
            write(6,*)'a0,a1,period,phi,alinear'
            write(6,*)a(1),a(2),period,a(3),alinear
            stop
c         else
c             go to 778
c         endif

        enddo

99    format(i4,1x,5(f12.6,1x))
      end


      SUBROUTINE mrqmin(x,y,sig,ndata,a,ia,ma,covar,alpha,nca,chisq,
     *funcs,alamda)
      implicit real*8(a-h,o-z)
      INTEGER ma,nca,ndata,ia(ma),MMAX
      REAL*8 alamda,chisq,a(ma),alpha(nca,nca),covar(nca,nca),
     *sig(ndata),x(ndata),y(ndata)
      PARAMETER (MMAX=100)
CU    USES covsrt,gaussj,mrqcof
      INTEGER j,k,l,mfit
      REAL*8 ochisq,atry(MMAX),beta(MMAX),da(MMAX)
      SAVE ochisq,atry,beta,da,mfit
      EXTERNAL funcs

      if(alamda.lt.0.)then
        mfit=0
        do 11 j=1,ma
          if (ia(j).ne.0) mfit=mfit+1
11      continue
        alamda=0.001
        call mrqcof(x,y,sig,ndata,a,ia,ma,alpha,beta,nca,chisq,funcs)
        ochisq=chisq
        do 12 j=1,ma
          atry(j)=a(j)
12      continue
      endif
      do 14 j=1,mfit
        do 13 k=1,mfit
          covar(j,k)=alpha(j,k)
13      continue
        covar(j,j)=alpha(j,j)*(1.+alamda)
        da(j)=beta(j)
14    continue

      call gaussj(covar,mfit,nca,da,1,1)
      if(alamda.eq.0.)then
        call covsrt(covar,nca,ma,ia,mfit)
        call covsrt(alpha,nca,ma,ia,mfit)
        return
      endif
      j=0
      do 15 l=1,ma
        if(ia(l).ne.0) then
          j=j+1
          atry(l)=a(l)+da(j)
        endif
15    continue
      call mrqcof(x,y,sig,ndata,atry,ia,ma,covar,da,nca,chisq,funcs)
      if(chisq.lt.ochisq)then
        alamda=0.1*alamda
        ochisq=chisq
        do 17 j=1,mfit
          do 16 k=1,mfit
            alpha(j,k)=covar(j,k)
16        continue
          beta(j)=da(j)
17      continue
        do 18 l=1,ma
          a(l)=atry(l)
18      continue
      else
        alamda=10.*alamda
        chisq=ochisq
      endif
      return
      END

      SUBROUTINE covsrt(covar,npc,ma,ia,mfit)
      implicit real*8(a-h,o-z)
      INTEGER ma,mfit,npc,ia(ma)
      REAL*8 covar(npc,npc)
      INTEGER i,j,k
      REAL*8 swap
      do 12 i=mfit+1,ma
        do 11 j=1,i
          covar(i,j)=0.
          covar(j,i)=0.
11      continue
12    continue
      k=mfit
      do 15 j=ma,1,-1
        if(ia(j).ne.0)then
          do 13 i=1,ma
            swap=covar(i,k)
            covar(i,k)=covar(i,j)
            covar(i,j)=swap
13        continue
          do 14 i=1,ma
            swap=covar(k,i)
            covar(k,i)=covar(j,i)
            covar(j,i)=swap
14        continue
          k=k-1
        endif
15    continue
      return
      END

      SUBROUTINE GAUSSJ(A,N,NP,B,M,MP)
      implicit real*8(a-h,o-z)
C
      PARAMETER (NMAX=100)
C
      DIMENSION A(NP,NP),B(NP,MP),IPIV(NMAX),INDXR(NMAX),INDXC(NMAX)
C
      DO 11 J=1,N
        IPIV(J)=0
11    CONTINUE
      DO 22 I=1,N
        BIG=0.
        DO 13 J=1,N
          IF(IPIV(J).NE.1)THEN
            DO 12 K=1,N
              IF (IPIV(K).EQ.0) THEN
                IF (ABS(A(J,K)).GE.BIG)THEN
                  BIG=ABS(A(J,K))
                  IROW=J
                  ICOL=K
                ENDIF
              ELSE IF (IPIV(K).GT.1) THEN
                WRITE(*,*)'GAUSSJ - Fatal error, singular matrix'
                RETURN
              ENDIF
12          CONTINUE
          ENDIF
13      CONTINUE
        IPIV(ICOL)=IPIV(ICOL)+1
        IF (IROW.NE.ICOL) THEN
          DO 14 L=1,N
            DUM=A(IROW,L)
            A(IROW,L)=A(ICOL,L)
            A(ICOL,L)=DUM
14        CONTINUE
          DO 15 L=1,M
            DUM=B(IROW,L)
            B(IROW,L)=B(ICOL,L)
            B(ICOL,L)=DUM
15        CONTINUE
        ENDIF
        INDXR(I)=IROW
        INDXC(I)=ICOL
        IF (A(ICOL,ICOL).EQ.0.)THEN
          WRITE(*,*)'GAUSSJ - Fatal error, singular matrix.'
          RETURN
          ENDIF
        PIVINV=1./A(ICOL,ICOL)
        A(ICOL,ICOL)=1.
        DO 16 L=1,N
          A(ICOL,L)=A(ICOL,L)*PIVINV
16      CONTINUE
        DO 17 L=1,M
          B(ICOL,L)=B(ICOL,L)*PIVINV
17      CONTINUE
        DO 21 LL=1,N
          IF(LL.NE.ICOL)THEN
            DUM=A(LL,ICOL)
            A(LL,ICOL)=0.
            DO 18 L=1,N
              A(LL,L)=A(LL,L)-A(ICOL,L)*DUM
18          CONTINUE
            DO 19 L=1,M
              B(LL,L)=B(LL,L)-B(ICOL,L)*DUM
19          CONTINUE
          ENDIF
21      CONTINUE
22    CONTINUE
      DO 24 L=N,1,-1
        IF(INDXR(L).NE.INDXC(L))THEN
          DO 23 K=1,N
            DUM=A(K,INDXR(L))
            A(K,INDXR(L))=A(K,INDXC(L))
            A(K,INDXC(L))=DUM
23        CONTINUE
        ENDIF
24    CONTINUE
      RETURN
      END

      SUBROUTINE mrqcof(x,y,sig,ndata,a,ia,ma,alpha,beta,nalp,chisq,
     *funcs)
      implicit real*8(a-h,o-z)
      INTEGER ma,nalp,ndata,ia(ma),MMAX
      REAL*8 chisq,a(ma),alpha(nalp,nalp),beta(ma),sig(ndata),x(ndata),
     *y(ndata)
      EXTERNAL funcs
      PARAMETER (MMAX=100)
      INTEGER mfit,i,j,k,l,m
      REAL*8 dy,sig2i,wt,ymod,dyda(MMAX)

      mfit=0
      do 11 j=1,ma
        if (ia(j).ne.0) mfit=mfit+1
11    continue
      do 13 j=1,mfit
        do 12 k=1,j
          alpha(j,k)=0.
12      continue
        beta(j)=0.
13    continue
      chisq=0.
      do 16 i=1,ndata
        call funcs(x(i),a,ymod,dyda,ma)
        sig2i=1./(sig(i)*sig(i))
        dy=y(i)-ymod
        j=0
        do 15 l=1,ma
          if(ia(l).ne.0) then
            j=j+1
            wt=dyda(l)*sig2i
            k=0
            do 14 m=1,l
              if(ia(m).ne.0) then
                k=k+1
                alpha(j,k)=alpha(j,k)+wt*dyda(m)
              endif
14          continue
            beta(j)=beta(j)+dy*wt
          endif
15      continue
        chisq=chisq+dy*dy*sig2i
16    continue
      do 18 j=2,mfit
        do 17 k=1,j-1
          alpha(k,j)=alpha(j,k)
17      continue
18    continue

      return
      END

      subroutine funcs(x,a,ymod,dyda,ma)
        implicit real*8(a-h,k,o-z)
        parameter(nmax=100)
        dimension a(nmax)
        dimension dyda(nmax)
        common/per/omega

        ymod=4.64*x+4.*a(1)*x+4.*a(2)*(sin(omega*x+a(3))-
     1           sin(a(3)))/omega
        dyda(1)=4.*x
        dyda(2)=4.*(sin(omega*x+a(3))-sin(a(3)))/omega
        dyda(3)=4.*a(2)*(cos(omega*x+a(3))-cos(a(3)))/omega
             write(2,*)a(1),a(2),a(3)
             write(3,*)dyda(1),dyda(2),dyda(3)
             write(1,*)x,ymod
        
        return
        end
