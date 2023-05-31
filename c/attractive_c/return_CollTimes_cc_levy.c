/* Program that returns collision times using a Monte Carlo method */
#include "CommonDefines.h"
// using namespace std;
int main(int argc, char* argv[])
{
  /* parse exteral inputs */
  /*                                |
  |  Parse Model Key Word Arguments |
  |                                 */
  double r,D,L,kappa,Dt,dt,varkappa,x0;
  printf("Enter the reaction range (cm): ");
  scanf("%lg",&r);printf("r=%g",r);
  printf("\nEnter the diffusion coefficient (cm^2/s): ");
  scanf("%lg",&D);printf("D=%g",D);
  printf("\nEnter the domain width/height (cm): ");
  scanf("%lg",&L);printf("L=%g",L);
  printf("\nEnter the reaction rate (Hz): ");
  scanf("%lg",&kappa);printf("kappa=%g",kappa);
  printf("\nEnter the spring rate (Hz): ");
  scanf("%lg",&varkappa);printf("varkappa=%g",varkappa);
  printf("\nEnter the unpreferred distance (cm): ");
  scanf("%lg",&x0);printf("x0=%g",x0);
  printf("\nEnter the timestep of motion: ");
  scanf("%lg",&Dt);printf("Dt=%g",Dt);
  printf("\nEnter the timestep of reaction: ");
  scanf("%lg",&dt);printf("dt=%g",dt);

  /*                                      |
  |  Parse Simulation Key Word Arguments  |
  |                                      */
  // double no_rep,no_att,nite,refl,set_sec,see;
  printf("\nEnter the number of tips to observe: ");int N;
  scanf("%d",&N);printf("N=%d",N);
  printf("\nEnter the number of trials: ");
  int niter;scanf("%d",&niter);printf("niter=%d\n",niter);
  printf("Enter the randomization seed: ");
  int seed;scanf("%d",&seed);printf("seed=%d\n",seed);
  printf("Use reflecting boundary conditions? (Enter 1/0): ");
  int reflect;scanf("%d",&reflect);printf("reflect=%d\n",reflect);
  printf("Set second particle within reaction range of first? (Enter 1/0): ");
  int set_second;scanf("%d",&set_second);printf("set_second=%d\n",set_second);
  printf("Do not allow repulsive forces? (Enter 1/0): ");
  int no_repulsion;scanf("%d",&no_repulsion);printf("no_repulsion=%d\n",no_repulsion);
  printf("Do not allow attractive forces? (Enter 1/0): ");
  int no_attraction;scanf("%d",&no_attraction);printf("no_attraction=%d\n",no_attraction);
  printf("Only allow nearest neighbor forces? (Enter 1/0): ");
  int neighbor;scanf("%d",&neighbor);printf("neighbor=%d\n",neighbor);
  printf("Which force model should be used?\n(Enter 1:spring, 2:QED2, 3:QED3, 4:QED2 + const. repulsion, 5:QED3 + const. repulsion, else:no force): ");
  int force_code;scanf("%d",&force_code);printf("force_code=%d\n",force_code);

  //DONE: clean up unnecessary input variables by using
  //DONE: printf( all input parameters such that I can redirect ^this to a text file )
  printf("the repeatable inputs are:\n");
  printf("%lg %lg %lg %lg %lg %lg %lg %lg %d %d %d %d %d %d %d %d %d\n",r,D,L,kappa,varkappa,x0,Dt,dt,N,niter,seed,reflect,set_second,no_repulsion,no_attraction,neighbor,force_code);
  int i,j,k,q,s;
  int Nmax=N;
  int nparticles=Nmax;
  double facy; double facx;
  double x[Nmax];double y[Nmax];
  // double X[Nmax];double Y[Nmax];
  // double X_old[Nmax];double Y_old[Nmax];
  double X_new[Nmax];double Y_new[Nmax];
  // double x_old[Nmax];double y_old[Nmax];
  // double x_new[Nmax];double y_new[Nmax];
  double Fx_net[Nmax];double Fy_net[Nmax];
  double Time; double t;  // time of motion and reaction, respectivly
  double frac; // temporal fraction for interpolation
  double cfrac; //1-frac
  double T;
  double T_prev;
  double dx,dy,dxt,dyt,dxW,dyW;
  bool still_running[Nmax];
  bool caught[Nmax];
  double Tsum_array[Nmax+1];
  int Tcount_array[Nmax+1];
  bool dont_terminate_trial;
  bool all_valid;
  bool boo;
  double step;
  double dmin[3];
  double sum_att_x; double sum_att_y;
  double stepscale=sqrt(2*D*Dt);
  double probreact=kappa*dt; //double sig;
  double min_dist_old[Nmax];
  double dist; double dist2;
  double distances[Nmax][Nmax];
  double displacements_x[Nmax][Nmax];
  double displacements_y[Nmax][Nmax];
  double facarray_x[Nmax][Nmax];
  double facarray_y[Nmax][Nmax];
  double tiarray[Nmax];
  double tfarray[Nmax];
  bool in_range; bool reacts;int ineigh;
  double Tavg;
  double T_value; double Rad; double Theta;
  srand(seed); // randomize seed.
  // double tmax=5000.;
  double tmax=5000.e100;
  int iter_per_movestep = round(Dt/dt);
  int i_neighbor[Nmax];
  double impulse_prefactor= varkappa * Dt;
  double impulse_constant = -1. * impulse_prefactor / x0;
  double impulse_factor;
  double xn; double yn;
  double ul; double th;
  int N0_end=0;
  // int N0_end=2;
  // int N0_end=10;
  double alpha=x0;
  double powerscale=-1./alpha;

  // initialize record to zero
  // for (i = 0; i < Nmax+2; i++) {
  for (i = 0; i < Nmax+1; i++) {
    Tsum_array[i]=0.;
    Tcount_array[i]=0;
  }
  /*                              |
  |  N Iterations of Monte Carlo  |
  |                              */
  printf("\nrunning simulation...\n");
  /* for each trial... */
  for (q = 0; q < niter; q++) {
    t=0.;T=0.;
    Time=0.;
    dont_terminate_trial=true;
    // still_running=true;
    // exit_code=-1;
    //T = -9999.; //initialize stopping times to -9999
    /* initialize uniform random points in the unit square n*/
    for (j = 0; j < Nmax; j++ ) {
      x[j] = L*uniformRandom();
      y[j] = L*uniformRandom();
      still_running[j]=true;
      // todo(later?): check if any particles are within the minimum allowable distance
      // todo(later?): reseed any particles that are within the minimum allowable distance
    }
    nparticles=Nmax;
    // optionally, set_second particle to be within distance r of the first particle
    if (set_second==1){
      Rad = r*uniformRandom();
      Theta = 2.*3.141592653589793*uniformRandom();
      x[1]=x[0]+Rad*cos(Theta);
      y[1]=y[0]+Rad*sin(Theta);
      if (reflect==0){
        x[1]=pbc(x[1],L);
        y[1]=pbc(y[1],L);
      }else{
        //enforce RBC for x coordinate
        if (x[1]>L){
          x[1]=2.*L-x[1];
        }else if (x[1]<0){
          x[1]=-1.*x[1];
        }
        //enforce RBC for y coordinate
        if (y[1]>L){
          y[1]=2.*L-y[1];
        }else if (y[1]<0){
          y[1]=-1.*y[1];
        }
      }
    }//end set_second kernel

    // compute distances between particle i and j; optionally take into account periodic boundary conditions
    for (i = 0; i < Nmax-1; i++ ) {
      if (still_running[i]) {
        for (j = i+1; j < Nmax; j++ ) {
          if (still_running[j]) {
            // compute displacement
            if (reflect==0){
              // dx = subtract_pbc_1d(x[i],x[j],L);
              // dy = subtract_pbc_1d(y[i],y[j],L);
              dmin[0]=fabs(x[i]-x[j]);
              dmin[1]=fabs(x[i]+L-x[j]);
              dmin[2]=fabs(x[i]-L-x[j]);
              facx = find_min(dmin,L);
              dmin[0]=fabs(y[i]-y[j]);
              dmin[1]=fabs(y[i]+L-y[j]);
              dmin[2]=fabs(y[i]-L-y[j]);
              facy = find_min(dmin,L);
              dx=x[i]+facx-x[j];
              dy=y[i]+facy-y[j];
            }
            else{
              dx = x[i]-x[j];
              dy = y[i]-y[j];
              facx=0.;facy=0.;
            }
            dist2=dx*dx+dy*dy;
            // record distances and displacements
            distances[i][j]=dist2;
            distances[j][i]=dist2;
            displacements_x[i][j]=-dx;
            displacements_y[i][j]=-dy;
            displacements_x[j][i]=dx;
            displacements_y[j][i]=dy;
            // record the pbc unwrapping function
            facarray_x[i][j]=facx;
            facarray_x[j][i]=facx;
            facarray_y[i][j]=facy;
            facarray_y[j][i]=facy;
            // update nearest neighbor distance and i_neighbor
            if (dist2<min_dist_old[i]){
              min_dist_old[i]=dist2;
              i_neighbor[i]=j;
            }
            if (dist2<min_dist_old[j]){
              //this choice does not imply symplectic deterministic forces
              min_dist_old[j]=dist2;
              i_neighbor[j]=i;
            }
          }
        }
      }
    }

    /*                                   |
    |   run simulation for given trial   |
    |                                   */
    step=0;  // <<< matches what wj did
    // step=-1; // <<< looks wrong at N=Nmax
    while(dont_terminate_trial){
      step=step+1;
      // one step of motion
      for (i = 0; i < Nmax; i++ ) {
        if (still_running[i]) {
          // compute force sum
          sum_att_x=0.;
          sum_att_y=0.;
          for (j = 0; j < Nmax; j++ ) {
            if (still_running[j] && i!=j) {
              sum_att_x=sum_att_x-impulse_prefactor*displacements_x[i][j]/distances[i][j];
              sum_att_y=sum_att_y-impulse_prefactor*displacements_y[i][j]/distances[i][j];
            }
          }
          // dxW=stepscale*normalRandom();
          // dyW=stepscale*normalRandom();
          ul=stepscale*pow(uniformRandom(),powerscale);
          th=angleRandom();
          dxW=ul*cos(th);
          dyW=ul*sin(th);
          X_new[i]=x[i]+dxW+sum_att_x;
          Y_new[i]=y[i]+dyW+sum_att_y;
          //enforce boundary conditions
          // if (reflect==0){
          //   //enforce PBC
          //   x[i]=periodic(X_new[i],L);
          //   y[i]=periodic(Y_new[i],L);
          // }else{
          //   //enforce RBC
          //   x[i]=reflection(X_new[i],L);
          //   y[i]=reflection(Y_new[i],L);
          // }
        }
      }
      //enforce periodic boundary conditions
      for (i = 0; i < Nmax; i++ ) {
        if (still_running[i]) {
          xn=X_new[i];
          yn=Y_new[i];
          if (xn>L) {
            x[i]=xn-L;
          }
          else {
            if (xn<0.) {
              x[i]=xn+L;
            }
            else {
              x[i]=xn;
            }
          }
          if (yn>L) {
            y[i]=yn-L;
          }
          else {
            if (yn<0.) {
              y[i]=yn+L;
            }
            else {
              y[i]=yn;
            }
          }
        }
      }

      // compute distances between particle i and j; optionally take into account periodic boundary conditions
      for (i = 0; i < Nmax-1; i++ ) {
        if (still_running[i]) {
          for (j = i+1; j < Nmax; j++ ) {
            if (still_running[j]) {
              // compute displacement
              if (reflect==0){
                // dx = subtract_pbc_1d(x[i],x[j],L);
                // dy = subtract_pbc_1d(y[i],y[j],L);
                dmin[0]=fabs(x[i]-x[j]);
                dmin[1]=fabs(x[i]+L-x[j]);
                dmin[2]=fabs(x[i]-L-x[j]);
                facx = find_min(dmin,L);
                dmin[0]=fabs(y[i]-y[j]);
                dmin[1]=fabs(y[i]+L-y[j]);
                dmin[2]=fabs(y[i]-L-y[j]);
                facy = find_min(dmin,L);
                dx=x[i]+facx-x[j];
                dy=y[i]+facy-y[j];
              }
              else{
                dx = x[i]-x[j];
                dy = y[i]-y[j];
                facx=0.;facy=0.;
              }
              dist2=dx*dx+dy*dy;
              // record distances and displacements
              distances[i][j]=dist2;
              distances[j][i]=dist2;
              displacements_x[i][j]=dx;
              displacements_y[i][j]=dy;
              displacements_x[j][i]=-dx;
              displacements_y[j][i]=-dy;
              // record the pbc unwrapping function
              facarray_x[i][j]=facx;
              facarray_x[j][i]=facx;
              facarray_y[i][j]=facy;
              facarray_y[j][i]=facy;
              // update nearest neighbor distance and i_neighbor
              if (dist2<min_dist_old[i]){
                min_dist_old[i]=dist2;
                i_neighbor[i]=j;
              }
              if (dist2<min_dist_old[j]){
                //this choice does not imply symplectic deterministic forces
                min_dist_old[j]=dist2;
                i_neighbor[j]=i;
              }
            }
          }
        }
      }

      ///////////////////////////////////////////////
      // one step of random, pairwise annihilation //
      ///////////////////////////////////////////////
      for (i = 0; i < Nmax; i++ ) {
        if(still_running[i]) {
          for (j = i+1; j < Nmax; j++ ) {
            if(still_running[j]){
            dist=sqrt(distances[i][j]);
            if(dist<=r){
              // determine whether those two particles react
              reacts=probreact>=uniformRandom();
              // optionally determine whether those two particles react via smeared rxn rate
              // sig=sigmoid(dist, r, beta);
              // reacts=probreact*sig>uniformRandom();
              if(reacts){
                // compute time since last reaction
                T_prev=T;
                T=step*dt;
                // record
                Tsum_array[nparticles] = Tsum_array[nparticles] + T - T_prev;
                Tcount_array[nparticles] = Tcount_array[nparticles] + 1;
                nparticles=nparticles-2;
                // remove the two reacting particles from the simulation
                still_running[i]=false;
                still_running[j]=false;
              }
            }
          }
        }
      }
    }

    if (nparticles <= N0_end){
      dont_terminate_trial=false;
    }
    }//end while running

  }//end for each trial
  printf("simulation complete!\n");
  // Print results
  printf("\nPrinting Inputs...\n");
  printf("r=%g\n",r);
  printf("D=%g\n",D);
  printf("L=%g\n",L);
  printf("kappa=%g\n",kappa);
  printf("varkappa=%g\n",varkappa);
  printf("x0=%g\n",x0);
  printf("dt=%g\n",dt);
  printf("Dt=%g\n",Dt);
  // printf("N=%d\n",N);
  printf("niter=%d\n",niter);
  // printf("seed=%d\n",seed);
  printf("reflect=%d\n",reflect);
  printf("set_second=%d\n",set_second);
  printf("no_repulsion=%d\n",no_repulsion);
  printf("no_attraction=%d\n",no_attraction);
  printf("neighbor=%d\n",neighbor);
  printf("force_code=%d\n",force_code);
  printf("iter_per_movestep=%d\n",iter_per_movestep);

  /*                              |
  |  Record Mean Collision Times  |
  |                              */
  // print mean output of T_lst to stdout
  printf("\nPrinting Outputs...\n");
  // printf("exit_code=%d\n",exit_code);
  // printf("max ntips=%d\n",Nmax);
  // printf("max ntips_over_area=%g\n",Nmax/(L*L));
  // printf("Tcount=%d\n",count_net);
  // printf("Tsum=%g\n",T_net);
  // printf("Tavg=%g\n",T_net/count_net);
  // printf("rate=%g\n",count_net/T_net);
  // printf("rate_over_area=%g\n",count_net/(L*L*T_net));
  // T_value=T_net/count_net;
  boo=true;
  for(i = 0; i < (Nmax - N0_end);i++){ // <<< this unshifts the output
  // for(i = 0; i < (Nmax - N0_end - 2);i++){
    if (boo){
      printf ("%d,",Nmax-i);
      // printf ("%d,",i+1);
    }
    boo=!boo;
  }
  printf ("\n");
  boo=true;
  for(i = 0; i < (Nmax-N0_end);i++){  // <<< this unshifts the output
  // for(i = 2; i < (Nmax - N0_end); i++){
    if (boo){
      Tavg=Tsum_array[Nmax-i]/Tcount_array[Nmax-i];
      // printf ("%d,",Tcount_array[Nmax-i]);
      // printf ("%f,",Tsum_array[Nmax-i]);
      printf ("%f,",Tavg);
      // printf ("%d,",i+1);
    }
    boo=!boo;
  }
  printf("\n");
  return 0;
}

// print dense output of T_lst to stdout
// printf("\nPrinting Outputs...\n");
// for(i = 0; i < Nmax;i++){
//   printf ("%d,",i+1);
// }
// printf ("\n");
// /* print*/
// for (q = 0; q < niter; q++){
//   for(i = 0; i < Nmax;i++){
//     printf ("%.7lg,",T_lst[q][i]);
//   }
//   printf ("\n");
// }

// // save dense output of T_lst to file
// FILE * fp;
// /* open the file for writing*/
// fp = fopen ("out.csv","w");
// for(i = 0; i < Nmax;i++){
//   fprintf (fp, "%d,",i);
// }
// fprintf (fp, "\n");
// //  write into the file stream
// for (q = 0; q < niter; q++){
//   for(i = 0; i < Nmax;i++){
//     fprintf (fp, "%.5le,",T_lst[q][i]);
//   }
//   fprintf (fp, "\n");
// }
// /* close the file*/
// fclose (fp);
