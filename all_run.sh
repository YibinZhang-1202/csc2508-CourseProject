# run vehicle detection
deactivate
cd VehicleDetection
source ./env/bin/activate
CUDA_VISIBLE_DEVICES=0 \
python3 VehicleDC.py \
	-src-dir ../aic19-track2-reid/small_example \
	-dst-dir ../aic19-track2-reid/small_example/vehicle_detect_classification_result \
	-vehicle-color all \
	-vehicle-type all
cd ..

# run reid
deactivate
cd 2019-CVPR-AIC-Track-2-UWIPL/Video-Person-ReID
source ./env/bin/activate
CUDA_VISIBLE_DEVICES=0 \
python main_video_person_reid.py \
    --train-batch 16 \
    --workers 0 \
    --seq-len 4 \
    --arch resnet50ta_surface_nu \
    --width 224 \
    --height 224 \
    --dataset aictrack2 \
    --dataset-dir ../../aic19-track2-reid/small_example/ \
    --use-surface \
    --evaluate \
    --pretrained-model log/ta_surface_nu_checkpoint_ep300.pth.tar \
    --save-dir log-test \
    --gpu-devices 1 \
    --re-ranking \
    --metadata-model v2m100 \
    --query-set set1 \
    --gallery-set set2 \
    --feature-dir log-test/feature_ep0300
cd ../..

# result process
deactivate
cd Result_process
python3 result_process.py \
	-dir-path ../aic19-track2-reid/small_example/ \
	-detect-result detect_result.txt \
	-reid-result-self reid_result_self.txt \
	-reid-result-cross reid_result_cross.txt
