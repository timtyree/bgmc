function return_CollTime_test(r,D,reflect)
% Monte Carlo parallel simulation for first reaction rate of N Brownian particles diffusion in
% scaled 2-D domain [0,1]^2 where reactions are determined through a minimum allowable distance pariwise 
% between particles. Once particles are withing a certain distance of each
% other, a particle can disappear at a rate proportional to the number of
% particles within the allowed distance. Similar to DistReactionSimPar.m but
% with a different method of checking probabilities of reaction based on
% heaviside function.

clear;%clc;
%tic % Used to calculate computer run time.
%% Parameters
% r = 0.2;             % Unscaled interaction range for the particles. 
% D = 1.56;              % Diffusion coefficient cm^2/s
% reflect = 0;         % Set to 1 if reflecting boundary, 0 if periodic.


SAVE_DATA = false;  % CBoolean variable for saving final data
use_instantaneous=false; % 0 is false
n = 11:70;           % Number of diffusing particles
l = sqrt([20.25, 25, 39, 50, 66]);       % Length of side of square.
kap = 10;            % Base reaction rate when particles are close.
dt=1e-5;            % Time step size.
tend=50000;         % Ending time. Want it to be as large as possible,
                    % while still making the code finish in a reasonable amount of time.
numtrials=1e2;     % The number of monte carlo trials. Again, want it
                    % to be as large as possible, while still making the code finish
                    % in a reasonable amount of time.                
                   
%fast test case
l = sqrt([20.25]);      %COMMENT_HERE
dt=1e-4;                %COMMENT_HERE
tend=10000;             %COMMENT_HERE
numtrials=1e1;          %COMMENT_HERE
r=1.;                   %COMMENT_HERE                
SAVE_DATA = false;      %COMMENT_HERE     

%allocate virtual memory
FirstCollTime = zeros(numtrials,length(n),length(l),length(r),length(kap)); % Preallocates first collision times.
[T,N,L] = ndgrid(1:numtrials,n,l);
minAllowableDistance=r;

%% Monte Carlo Loop
% Create waitbar for parfor loop.
% DQ = parallel.pool.DataQueue;
% h = waitbar(0, 'Please wait ...');
% afterEach(DQ, @nUpdateWaitbar);
Nruns = numel(FirstCollTime);
p = 1;

fprintf('running %d runs of the simulation...',Nruns)
% parfor makes a parallel loop that runs over all possible parameter combinations. 
% parfor trial=1:Nruns
for trial=1:Nruns
    % Each time through this loop is an independent Monte Carlo trial.    
    
    % Initialize
        % Set parameters for a particular trial
        Numb = N(trial);
        Len = L(trial);
        minDistance = r;%/Len;
        Dif = D;%/Len^2; % unScaled diffusion coefficient
        
        % Initialize particle locations uniformly.
        keeperX = rand(1,Numb)*Len;
        keeperY = rand(1,Numb)*Len;
        % Set last particle to be within minDistance of one other particle (if desired).
        Theta = rand*2*pi;
        Rad = rand*minDistance;
        lastX = keeperX(end-1)+Rad*cos(Theta);
        lastY = keeperY(end-1)+Rad*sin(Theta);
        if lastX < 0
            keeperX(end) = 1+lastX;
        elseif lastX > 1
            keeperX(end) = lastX-1;
        else
            keeperX(end) = lastX;
        end
        if lastY < 0
            keeperY(end) = 1+lastY;
        elseif lastY > 1
            keeperY(end) = lastY-1;
        else
            keeperY(end) = lastY;
        end
    flag = 0; % Flag for when to stop the trial run.
    t = 0;
    W = [keeperX',keeperY']; % Set initial position
    
    % Simulate
    while t < tend
        t = t+dt; % Update master time
        
        dW=sqrt(2*Dif*dt)*randn(Numb,2); % Generate next step in diffusion process.
        Wtemp = W + dW;
        
        Check0 = logical(Wtemp < 0);
        Check1 = logical(Wtemp > 1);
        
        if reflect ==1
            % Reflection condition if particle reaches boundary.

            Wtemp = Wtemp-2*Check0.*Wtemp;
            Wtemp = Wtemp+2-2*Check1.*Wtemp;
        else
            % Periodic condition if particle passes boundary.

            Wtemp = Wtemp+Len*Check0;
            Wtemp = Wtemp-Len*Check1;
        end
        
        % Check number of particles pairwise that are within min distance.
        if reflect == 1
            Dist = triu(pdist2(Wtemp,Wtemp),1); %Euclidean Distance
        else
            Distx = pdist2(Wtemp(:,1),Wtemp(:,1)); %Periodic Distance
            Disty = pdist2(Wtemp(:,2),Wtemp(:,2));
            Dx = triu(min(Distx,1-Distx),1);
            Dy = triu(min(Disty,1-Disty),1);
            Dist = sqrt(Dx.^2+Dy.^2);
        end
        
        if use_instantaneous==1
            %React the particles instantly
            % Check if any pair of particles reached min distance.
            Dist = pdist2(Wtemp,Wtemp);
            Ind = eye(size(Dist));
            DistCheck = min(Dist(~Ind),[],'all');
            if DistCheck <= minAllowableDistance 
                flag = 1;
            end
        else
            % Probabilities of reaction happening in interval dt based on particle
            % distance and rate.
            probs = triu(rrate(Dist,kap,minDistance),1)*dt; 

            TestProb = rand(Numb,Numb);         % Generate N^2 uniformly dist random 
                                                % numbers to compare to the
                                                % probabilities of an event occuring
                                                % based on pairwise interactions.
            TestAns = logical(TestProb < probs);
            if sum(TestAns,'all') > 0
                flag = 1;
            end
        end
        
        % Update state and consider terminating simulation
        W = Wtemp;
        if flag == 1
            FirstCollTime(trial) = t;
            break       % Exiting condition (reaction occured) met for this run.
        end
    end
%     send(DQ,trial);
end

% Average over successful trials.
% Normalize rate based on area(?) and convert from seconds to milliseconds
% (ms).
CollRate = squeeze(sum(FirstCollTime~=0,1)./sum(FirstCollTime,1)/1000);
% CollTime = 1/CollRate:   %TODO: PM % expected collision times
% delta_CollTime = bootci(TODO); %TODO: PM % bootstrap uncertainties/SE for collision times

% Count number of successful trials for reference.
NumSuccTrials = squeeze(sum(FirstCollTime~=0,1));

%% Printing Results
fprintf('\n=============')
fprintf(datestr(now,'yyyy-mmm-dd_HH-MM-SS'))
fprintf('=============\n')
fprintf('\nPrinting Inputs: ')
C = { 'r', 'D', 'reflect';
    r,   D,    reflect};
str = sprintf('%s_%d, ',C{:});
fprintf(str)
fprintf('\nPrinting Outputs:')
n_values=N(1,:,1)';
C = { 'N_min', 'N_max';
    min(n_values),   max(n_values)};
str = sprintf('%s_%d, ',C{:});
fprintf(str)
fprintf('\nCollRate:\n');%%1.0f', CollRate);
disp(CollRate')
% fprintf('\nCollRate:\n')
% str = sprintf(CollRate);
% fprintf(str)
% disp(CollRate)


%% saving data
% This saves the data with an appropriate filename.

if SAVE_DATA
  filename=['../data/results_CollTime_',datestr(now,'yyyy-mmm-dd_HH-MM-SS')];
  save(filename);
end

end


%%
% %% Plotting and Scaling Law Check
% 
% sc = 1./repmat(l.^2,length(n),1);
% Density = repmat(n',1,length(l)).*sc; 
% ScaledRates = CollRate.*sc;
% 
% hold on
% for ii = 1:length(l)
%    plot(Density(:,ii),ScaledRates(:,ii),'*') 
% end
% hold off
% ll = legend('Reaction Rate $L^2 = 20.25$',...
%     'Reaction Rate $L^2 = 25$',...
%     'Reaction Rate $L^2 = 39$',...
%     'Reaction Rate $L^2 = 50$',...
%     'Reaction Rate $L^2 = 66$');
% xl = xlabel('Particle Density $q$');
% yl = ylabel('Rate/A $cm^{-2}$');
% set(ll,'Interpreter','Latex');
% set(xl,'Interpreter','Latex');
% set(yl,'Interpreter','Latex');
% 
% figure()
% hold on
% for ii = 1:length(l)
%    plot(n,CollRate(:,ii),'*')
% end
% hold off
% xl = xlabel('Particle Number $n$');
% yl = ylabel('Reaction Rate');
% ll = legend('Reaction Rate $L^2 = 20.25$',...
%     'Reaction Rate $L^2 = 25$',...
%     'Reaction Rate $L^2 = 39$',...
%     'Reaction Rate $L^2 = 50$',...
%     'Reaction Rate $L^2 = 66$');
% set(ll,'Interpreter','Latex');
% set(xl,'Interpreter','Latex');
% set(yl,'Interpreter','Latex');


%% Calculate polynomial fit
% 
% % Power fit f(N) = a*N^b.
% % Set storage.
% sz1 = size(CollRate,2);
% sz2 = size(CollRate,3);
% sz3 = size(CollRate,4);
% fitfun = squeeze(cell(sz1,sz2,sz3));
% % Calculate fit.
% for kk = 1:numel(fitfun)
% fitfun{kk} = ratePfit(n,CollRate(:,kk));
% end
% 
% % Quadratic fit a*N*(N-1).
% fitfun2 = squeeze(cell(sz1,sz2,sz3));
% for kk = 1:numel(fitfun2)
% fitfun2{kk} = ratePfit2(n,CollRate(:,kk));
% end
% 
% % Power fit a*q^b for scaled rates.
% fitfunS = ratePfitScaled(Density(:),ScaledRates(:));


%toc % Display computer run time.

%% Functions called in script
% function nUpdateWaitbar(~)
%     waitbar(p/Nruns, h);
%     p = p + 1;
% end
% 
% function y = heaviside(x)
%     if x >= 0
%         y= 1;
%     else
%         y= 0;
%     end
% end

%% TODO
% TODO: compute variance in collision times
% TODO: compute print inputs
% TODO: print results
% TODO: allow for external arguments. consider allowing for a good few
% arguements
% TODO: compile to binary from command line
% TODO: test run the binary
% TODO: generate run_test.dat in python
% TODO: generate run_1.dat in python
% TODO: to the osg!
% end
