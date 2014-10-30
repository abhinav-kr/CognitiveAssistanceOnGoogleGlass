function goodBoxesNonDups = detect_object( image_path, offset, slice )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
addpath(genpath(('/home/ivashish/exemplarsvm-master')));

I = imread(image_path);

load('voc2007-bus');

models_len = length(models);
slice_size = int32(models_len/total_vm)

start = ceil( (offset*models_len)/100 )

last = floor( ((offset+slice)*models_len)/100 )

if last>models_len
        last = models_len;
end



%Using default 
esvmParams = esvm_get_default_params();
%esvmParams.detect_add_flip =0;
%esvmParams.detect_levels_per_octave =1;
fprintf(1,'Start is %d end is %d ', start, last);

tt = tic;
rs = esvm_detect(I,models(1:50),esvmParams);
bboxes = cat(1,rs.bbs{:});
if(~isempty(bboxes))
    scores = bboxes(:,12);
    goodBoxInds = scores>-0.75;
    goodBoxes = bboxes(goodBoxInds,:);
    goodBoxesNonDups = esvm_nms(goodBoxes,0.5); %remove duplicate detections
    
else
    goodBoxesNonDups = [];
    
end

time_taken = toc(tt);
disp(num2str(time_taken));
end


