function kappa = rrate2(r,kap,Param)
%#codegen
% Reaction rate based on base rate kap and interaction distance r between two
% particles.
if Param > r
    kappa = -kap*log(r/Param); %Inverse transform sampling for exponential distribution?
else
    kappa = 0;
end
end 
