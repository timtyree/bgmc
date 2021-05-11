double comp_gen_extreme_value_pdf(double x, double shape,double location, double scale){
  // returns radially dependent scale that follows a generalize
  // extreme value probability distribution function
  double val;double t;double p;
  shape=-1.*shape;
  val=(x-location)/scale;
  //compute t(x)
  if(shape==0.){
    t=exp(-val);
  }
  else{
    t=pow((1.+shape*val),(-1./shape));
  }
  //compute pdf
  p=pow(t,(shape+1.))*exp(-1.*t)/scale;
  return p;
}
