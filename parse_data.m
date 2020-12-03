F = -F;
figure(1); plot(td, d); hold on; plot(tF, F);

td_new_idx = find(td >= 18.9);
td_new = td(td_new_idx) - min(td(td_new_idx));
d_new = d(td_new_idx);
td_delta = max(td_new);

[val, idx_end] = max(F);
val = tF(idx_end);
[val, idx_start] = min(abs(tF - (val - td_delta)));
tF_new = tF(idx_start:idx_end) - min(tF(idx_start:idx_end));
F_new = F(idx_start:idx_end);

figure(2); plot(td_new, d_new); hold on; plot(tF_new, F_new);

t_f = 0:0.05:td_delta;
d_f = [];
F_f = [];
for t=t_f
    [val, idx] = min(abs(td_new - t));
    d_f = [d_f, d_new(idx)];
    [val, idx] = min(abs(tF_new - t));
    F_f = [F_f, F_new(idx)];
end
e_f = (d_f - min(d_f))/min(d_f);
plot(F_f, e_f, 'LineWidth', 3);
xlabel("Force (N)"); ylabel("Strain = \epsilon = \Delta L / L_0");
set(gca,'fontsize', 18);
title("Mylar");