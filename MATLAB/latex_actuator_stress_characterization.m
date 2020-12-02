P = 10; % kPa
ID_all = 0.5:0.5:25; % mm, inner diameter
t_all = 0.25:0.25:8.4; % mm, actuator thickness
% ID = 12.7; % mm, inner diameter
% t = 3.2; % mm, actuator thickness

[ID, t] = meshgrid(ID_all, t_all);

r_i = ID / 2;
r_o = r_i + t;
r_avg = (r_i + r_o) / 2;

%% Calculate axial stress
s_l = P*r_i.^2 ./ (r_o.^2 - r_i.^2);  % kPa
F = 2 * pi * s_l .* r_i .* (t / 1000);  % N
N_PVDF = (F / 0.06);
N_PVDF_TrFE = (F / 0.41);

L = 5;
N_squares = (L*2*pi*r_o/10);
percentage_PVDF = N_PVDF ./ N_squares;
percentage_PVDF_TrFE = N_PVDF_TrFE ./ N_squares;

figure(1);
ax = subplot(1, 2, 1);
contour(ID, t, N_PVDF, 10);
colorLim = ax.CLim;
colorbar;
xlabel("Inner diameter (mm)"); ylabel("Wall Thickness (mm)");
title("PVDF (\epsilon = 12, t = 10um)");
ax2 = subplot(1, 2, 2);
contour(ID, t, N_PVDF_TrFE, 10);
colorbar;
xlabel("Inner diameter (mm)"); ylabel("Wall Thickness (mm)");
title("PVDF-TRFE-CFE (\epsilon = 50, t = 8um)");

sgtitle("Number of active 1x1 cm^2 squares to oppose shear force (P = 10 kPa)");

figure(2);
ax = subplot(1, 2, 1);
contour(ID, t, percentage_PVDF, 10);
colorLim = ax.CLim;
colorbar;
xlabel("Inner diameter (mm)"); ylabel("Wall Thickness (mm)");
title("PVDF (\epsilon = 12, t = 10um)");
ax2 = subplot(1, 2, 2);
contour(ID, t, percentage_PVDF_TrFE, 15);
colorbar;
xlabel("Inner diameter (mm)"); ylabel("Wall Thickness (mm)");
title("PVDF-TRFE-CFE (\epsilon = 50, t = 8um)");

sgtitle("Percentage of active 1x1 cm^2 squares to oppose shear force (P = 10 kPa)");