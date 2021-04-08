function kappa = rrate(r,kap,Param)
%#codegen
% Reaction rate based on base rate kap and interaction distance r between two
% particles.
if Param > r
    kappa = kap;%*heaviside(Param-r);
else
    kappa = 0;
end
end
 
