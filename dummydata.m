%Dummy data for ICHACK ting
clear;
clf;

n_players = 1;

pitch_x = 100;
pitch_y = 100;

v_max = 10;

t_step = 0.1;
t_frames = 200;

posit(1:t_frames,1:(2*n_players)) = zeros;
vel(1:(2*n_players)) = zeros;

bounce_lim = 10;

n_datasets = 5;

c = clock;
hrs = c(4);
min = c(5);
sec = floor(c(6));


for n = 1:n_datasets
    for p = 1:n_players
        posit(1,(2*p)-1) = rand()*pitch_x;
        posit(1,2*p) = rand()*pitch_y;

        vel((2*p)-1) = (0.5-rand())*2*v_max;
        vel(2*p) = (0.5-rand())*2*v_max;

        for t = 2:t_frames        
            posit(t,(2*p)-1) = posit(t-1,(2*p)-1) + vel((2*p)-1)*t_step;
            posit(t,2*p) = posit(t-1,2*p) + vel((2*p)-1)*t_step;
            
            if mod(t,20) == 0
                vel((2*p)-1) = (0.5-rand())*2*v_max;
                vel(2*p) = (0.5-rand())*2*v_max;
            end

            if (posit(t,(2*p)-1) < 0) || (posit(t,(2*p)-1) > pitch_x)
                posit(t,(2*p)-1) = pitch_x/2;
            end
            if (posit(t,(2*p)) < 0) || (posit(t,(2*p)) > pitch_y)
                posit(t,(2*p)) = pitch_y/2;
            end
        end


    end

%     for t = 1:t_frames
%         cur_x = posit(t,2:2:end);
%         cur_y = posit(t,1:2:(end-1));
% 
%         scatter(cur_x,cur_y);
%         axis([0 pitch_x 0 pitch_y]);
% 
%         pause(t_step);
%     end


    filename = strcat(num2str(hrs),num2str(min),num2str(sec),'_',num2str(n),'.csv');
    csvwrite(strcat('/Users/ferhaanmalek/Desktop/ICHack/dummydata/',filename),posit);
end