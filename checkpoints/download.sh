
#
# Copyright 2025 The Board of Trustees of the University of Illinois. All Rights Reserved.
#
# Licensed under the terms of Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# The License is included in the distribution as LICENSE file.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Download all SAM-2 checkpoints

BASE_URL="https://dl.fbaipublicfiles.com/segment_anything_2/072824/"
sam2_hiera_t_url="${BASE_URL}sam2_hiera_tiny.pt"
sam2_hiera_s_url="${BASE_URL}sam2_hiera_small.pt"
sam2_hiera_b_plus_url="${BASE_URL}sam2_hiera_base_plus.pt"
sam2_hiera_l_url="${BASE_URL}sam2_hiera_large.pt"

wget -nc -O sam2_hiera_tiny.pt $sam2_hiera_t_url
wget -nc -O sam2_hiera_small.pt $sam2_hiera_s_url
wget -nc -O sam2_hiera_base_plus.pt $sam2_hiera_b_plus_url
wget -nc -O sam2_hiera_large.pt $sam2_hiera_l_url




