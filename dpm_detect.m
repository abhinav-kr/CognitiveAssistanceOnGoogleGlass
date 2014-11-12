function goodBoxesNonDups = detect_object( image_path, offset, slice,fidelity )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
addpath(genpath(('/home/ivashish/voc-dpm-master')));

I = imread(image_path);

load('VOC2007/bottle_final.mat');

models_len = length(models);

tt = tic;
goodBoxesNonDups = process(im, model, -0.5);
time_taken = toc(tt);

goodBoxesNonDups = [goodBoxesNonDups 10 int32(time_taken*1000)];
display(goodBoxesNonDups)
disp(num2str(time_taken));
end


