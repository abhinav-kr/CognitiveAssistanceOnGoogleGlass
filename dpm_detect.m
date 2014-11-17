function goodBoxesNonDups = detect_object( image_path, offset, slice,fidelity,car_model)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
addpath(genpath(('/home/ivashish/voc-dpm-master')));

im = imread(image_path);

%load('VOC2007/car_final.mat');

tt = tic;
goodBoxesNonDups = process(im, car_model, -0.5);
time_taken = toc(tt);

goodBoxesNonDups = [goodBoxesNonDups 10 int32(time_taken*1000)];
display(goodBoxesNonDups)
disp(num2str(time_taken));
end


