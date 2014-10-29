#!/usr/bin/env python 
#
# Cloudlet Infrastructure for Mobile Computing
#
#   Author: Kiryong Ha <krha@cmu.edu>
#
#   Copyright (C) 2011-2013 Carnegie Mellon University
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

class Protocol_client(object):
    CONTROL_MESSAGE_KEY = "control"
    RESULT_MESSAGE_KEY = "result"
    RESULT_ID_MESSAGE_KEY = "result_frame_id"
    FRAME_MESSAGE_KEY = "id"
    OFFLOADING_ENGINE_NAME_KEY = "engine_id"
    TOKEN_INJECT_KEY = "token_inject"


class Protocol_application(object):
    JSON_KEY_SENSOR_TYPE = "sensor_type"
    JSON_VALUE_SENSOR_TYPE_JPEG = "mjepg"
    JSON_VALUE_SENSOR_TYPE_ACC = "acc"
    JSON_VALUE_SENSOR_TYPE_GPS = "gps"
    JSON_VALUE_SENSOR_TYPE_AUDIO = "wave"

class Video_application(object):
    JSON_CURRENT_VM_COUNT = "total_vm_count"
    JSON_THREAD_ID = "thread_id"
    JSON_THREAD_NAME ="thread_name"
    JSON_VM_SLICE="vm_slice"
    JSON_VM_OFFSET="vm_offset"
    JSON_APP_SENT_TIME = "app_sent_time"
    JSON_APP_RCV_TIME = "app_rcv_time"
    JSON_OBJECT_DETECTION_TIME = "odt"


class Protocol_measurement(object):
    JSON_KEY_CONTROL_SENT_TIME = "control_sent_time"
    JSON_KEY_APP_RECV_TIME = "app_recv_time"
    JSON_KEY_APP_SENT_TIME = "app_sent_time"
    JSON_KEY_UCOMM_RECV_TIME = "ucomm_recv_time"
    JSON_KEY_UCOMM_SENT_TIME = "ucomm_sent_time"

    JSON_KEY_ALLOWED_APP_LIST = "allowed_app_list"
    JSON_KEY_REGISTER_APP_UUID = "register_app"

    APP_MOTION = "motion-classifier"
    APP_MOPED = "moped"
    APP_STF = "stf"
    APP_FACE = "face"
    APP_TESSERACT = "ocr-tesseract"
    APP_OCR_COMM = "ocr-comm"
    APP_ACTIVITY = "activity"
    APP_AR = "ar"
    APP_DUMMY = "dummy"
    APP_DUMMY_SYNTHETIC = "dummy-synthetic"
    APP_NAME_LIST = (APP_MOTION, APP_MOPED, APP_STF, APP_FACE, \
            APP_TESSERACT, APP_OCR_COMM, APP_ACTIVITY, APP_AR, \
            APP_DUMMY, APP_DUMMY_SYNTHETIC)
