function f = ratePfit2(N,data)

% Find a polynomial fit of the form = a*N*(N-1) to data.

if size(N) ~= size(data)
    N = N';
end

if size(N) ~= size(data)
    error('Error. \nDependent and independent data vectors do not match in length.')
end

powerfittype = fittype('a*x*(x-1)',...
    'dependent',{'y'},'independent',{'x'},...
    'coefficients',{'a'});

f = fit(N,data,powerfittype);

end