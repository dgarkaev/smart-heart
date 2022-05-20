function [fn_out] = pcg_waveform(fn_inp)
[sample_data, sample_rate] = audioread(fn_inp);
% To mono
sample_data = sample_data(:,1);
sample_length=length(sample_data);
tx=(0:sample_length-1)/sample_rate;

% Настраиваем графику
% -------------------------------------------------------------------------
figure('Visible', 'Off');

% Рисуем сигнал
% -------------------------------------------------------------------------
plot(tx,sample_data);
% plot(periodogram(sample_data,'Fs',fs,'NFFT',length(sample_data)));
xlabel('Время, c');
ylabel('Амплитуда');
grid on;


[path,namenm,~] = fileparts(fn_inp);

fn=strcat(namenm,'_', string(posixtime(datetime)*1000), '_spec');
ff=fullfile(path, fn);
ff=strcat(ff,'.png');
saveas(gcf,ff);
fn_out=ff;
end