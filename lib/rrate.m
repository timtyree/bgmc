function kappa = rrate(r,kap,Param)

% Reaction rate based on base rate kap and interaction distance r between two
% particles.
kappa = kap*heaviside(Param-r);

end