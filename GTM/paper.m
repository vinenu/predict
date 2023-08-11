% Demonstrates the GTM with a 2D target space and a 1D latent space.
%
%		This script generates a simple data set in 2 dimensions, 
%		with an intrinsic dimensionality of 1, and trains a GTM 
%		with a 1-dimensional latent variable to model this data 
%		set, visually illustrating the training process
%
% Synopsis:	gtm_demo
%
% Notes:	The script generates a number of variables which may
%		overwrite variables already existing in the workspace.
%		The generated variables remain in the work space after
%		the script has finished executing.
%

% Version:	The GTM Toolbox v1.0 beta
%
% Copyright:	The GTM Toolbox is distributed under the GNU General Public 
%		Licence (version 2 or later); please refer to the file 
%		licence.txt, included with the GTM Toolbox, for details.
%
%		(C) Copyright Markus Svensen, 1996


%%%%% Generate and plot a 2D data set %%%%%

clear all;close all;
clc;

% 
% fprintf(['\nYou''ve started the GTM demo, please wait while ', ...
% 	 'data is being generated.\n\n']);
T = xlsread('pater_date.xlsx');
% fprintf([...
% 'The generation of data is accomplished!'...
% '\nPress any key to continue ...\n\n']);
% pause(0.1);






%%%%% Generate and plot (along with the data) an initial GTM model %%%%%
% 
% fprintf('Please wait while the GTM model is set up.\n\n');
[X, MU, FI, W, b] = GTM_STP2(T,441,36,1.2);
% Y =  FI*W;

% fprintf([...
% 'The figure shows the starting point for the GTM, before the training.\n', ...
% 'A discrete latent variable distribution of 20 points in 1 dimension \n', ...
% 'is mapped to the 1st principal component of the target data.\n', ...
% 'Each of the 20 points defines the centre of a Gaussian in a Gaussian \n', ...
% 'mixture, marked by the green ''+''-signs. The mixture components have \n', ...
% 'all equal variance, illustrated by the filled circle around each \n', ...
% '''+''-sign, the raddii corresponding to 2 standard deviations.\n', ...
% 'The ''+''-signs are connected with a line according to their \n', ...
% 'corresponding ordering in latent space.\n\n', ...
% 'Press any key to begin training ...\n\n']);
% pause(0.1);



%%%% Train the GTM and plot it (along with the data) as training proceeds %%%%

%for j = 1:100
  [W, b] = GTM_TRN(T, FI, W, 0.001, 100, b, 'quiet');
  

%   if (j == 4)
%     fprintf([...
% 'The GTM initiallaly adapts relatively quickly - already after \n', ...
% '4 iterations of training, a rough fit is attained.\n\n', ...
% 'Press any key to continue training ...\n\n']);
%    pause(0.1);
%   elseif (j == 8)
%     fprintf([...
% 'After another 4 iterations of training:  from now on further \n', ...
% 'training only makes small changes to the mapping, which combined with \n', ...
% 'decrements of the Gaussian mixture variance, optimize the fit in \n', ...
% 'terms of likelihood.\n\n', ...
% 'Press any key to continue training ...\n\n']);
%     pause(0.1);
%   else
%     pause(0.1);
%   end
% end
Y =  FI*W;

% fprintf([...
% 'After 15 iterations of training the GTM can be regarded as converged. \n', ...
% 'Is has been adapted to fit the target data distribution as well \n', ...
% 'as possible, given prior smoothness constraints on the mapping. It \n', ...
% 'captures the fact that the probabilty density is higher at the two \n', ...
% 'bends of the curve, and lower towards its end points.\n\n', ...
% 'Thanks for your interest in running the GTM demo'....
% 'Press any key to continue training ...\n\n']);
% 
% pause(0.1);

modes = GTM_PMD(T, X, FI, W);
axis([-1 1 -1 1]);
plot(modes(:,1),modes(:,2),'bo');

n=1;
XV=[length(X),2];
for k= 1:length(X)
    for m = 1 :length(modes)
        if (X(k,:) == modes(m,:))
            break;
        elseif (m == length(modes))
            XV(n,:) = X(k,:);
            n = n+1;
        end
    end
end

TV=[length(X),2];
sigmaTV = 2*(MU(1,2)-MU(2,2));
FI = GTM_GBF(MU, sigmaTV,XV);
TV=FI*W;




