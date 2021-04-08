function f = ratePfit(N,data)

% Find a polynomial fit of the form = a*(N-1)^b to given data.

if size(N) ~= size(data)
    N = N';
end

if size(N) ~= size(data)
    error('Error. \nDependent and independent data vectors do not match in length.')
end

powerfittype = fittype('a*(x-1)^b',...
    'dependent',{'y'},'independent',{'x'},...
    'coefficients',{'a','b'});

f = fit(N,data,powerfittype);

end