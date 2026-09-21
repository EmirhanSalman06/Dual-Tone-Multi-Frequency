%% Dual-Tone Multi-Frequency (DTMF) Touch-Tone Analysis and Decoder
clear; clc; close all;

%% -------------------------------------------------------------------------
% 1. SYSTEM PARAMETERS & LOOKUP TABLE
% -------------------------------------------------------------------------
Fs = 8192;                  % Sampling rate (Hz)
duration = 0.1;             % Signal duration (100 ms)
N = round(Fs * duration);   % Total samples
n = 0:(N - 1);              % Sample index vector

% Discrete angular frequencies (radians/sample)
row_freqs = [0.5346, 0.5906, 0.6535, 0.7217];
col_freqs = [0.9273, 1.0247, 1.1328];

% Keypad 4x3 matrix layout
keypad_layout = [
    '1', '2', '3';
    '4', '5', '6';
    '7', '8', '9';
    '*', '0', '#'
];

%% -------------------------------------------------------------------------
% 2. KEY SELECTION (INTERACTIVE OR STATIC)
% -------------------------------------------------------------------------
% Key Selection Configuration:
% Set statically (e.g., target_key = '5';) to bypass interactive prompt, or leave dynamic:
target_key = input('Enter a key from keypad (0-9, *, #): ', 's');
target_key = strtrim(target_key);

% Input validation loop
while ~ismember(target_key, keypad_layout)
    fprintf('Invalid key! Please enter one of: 0-9, *, #\n');
    target_key = input('Enter a key: ', 's');
    target_key = strtrim(target_key);
end

%% -------------------------------------------------------------------------
% 3. SIGNAL SYNTHESIS
% -------------------------------------------------------------------------
% Locate key coordinates in keypad matrix
[r_idx, c_idx] = find(keypad_layout == target_key);
w_row = row_freqs(r_idx);
w_col = col_freqs(c_idx);

% Synthesize signal: d[n] = sin(w_row * n) + sin(w_col * n)
signal = sin(w_row * n) + sin(w_col * n);

%% -------------------------------------------------------------------------
% 4. DTFT / FFT ANALYSIS
% -------------------------------------------------------------------------
N_fft = 2048;
D = fft(signal, N_fft);
half_N = N_fft / 2;

magnitude = abs(D(1:half_N)) / (N / 2);
omega_axis = linspace(0, pi, half_N);

%% -------------------------------------------------------------------------
% 5. AUTOMATED DTMF DECODER
% -------------------------------------------------------------------------
% Search row peak in [0.45, 0.80] rad
row_mask = (omega_axis >= 0.45) & (omega_axis <= 0.80);
[~, max_r_idx] = max(magnitude(row_mask));
sub_omega_row = omega_axis(row_mask);
detected_w_row = sub_omega_row(max_r_idx);

% Search column peak in [0.85, 1.25] rad
col_mask = (omega_axis >= 0.85) & (omega_axis <= 1.25);
[~, max_c_idx] = max(magnitude(col_mask));
sub_omega_col = omega_axis(col_mask);
detected_w_col = sub_omega_col(max_c_idx);

% Map detected frequencies to nearest grid coordinates
[~, detected_r_idx] = min(abs(row_freqs - detected_w_row));
[~, detected_c_idx] = min(abs(col_freqs - detected_w_col));
decoded_key = keypad_layout(detected_r_idx, detected_c_idx);

% Print diagnostic results to Command Window
fprintf('\n--- DTMF Analysis for Key ''%s'' ---\n', target_key);
fprintf('Expected Frequencies -> w_row: %.4f, w_col: %.4f\n', w_row, w_col);
fprintf('Detected Frequencies -> w_row: %.4f, w_col: %.4f\n', detected_w_row, detected_w_col);
fprintf('Decoded Key          -> ''%s'' (Success: %d)\n', decoded_key, strcmp(decoded_key, target_key));

%% -------------------------------------------------------------------------
% 6. VISUALIZATION
% -------------------------------------------------------------------------
figure('Name', sprintf('DTMF Analysis - Key %s', target_key), 'Color', [1 1 1]);

% Time-domain waveform
subplot(2, 1, 1);
plot(n(1:120), signal(1:120), 'b', 'LineWidth', 1.5);
grid on;
title(sprintf('Time-Domain Waveform for Key ''%s'' (First 120 Samples)', target_key));
xlabel('Sample Index n');
ylabel('Amplitude d[n]');

% Frequency-domain magnitude spectrum
subplot(2, 1, 2);
plot(omega_axis, magnitude, 'r', 'LineWidth', 1.5);
grid on; hold on;
xline(w_row, '--g', sprintf('\\omega_{row} = %.4f', w_row), 'LineWidth', 1.2);
xline(w_col, '--m', sprintf('\\omega_{col} = %.4f', w_col), 'LineWidth', 1.2);
title(sprintf('DTFT Magnitude Spectrum |D(e^{j\\omega})| for Key ''%s''', target_key));
xlabel('Discrete Angular Frequency \omega (rad/sample)');
ylabel('Normalized Magnitude');
xlim([0, pi]);
legend('Magnitude Spectrum', 'Row Frequency', 'Column Frequency', 'Location', 'northeast');