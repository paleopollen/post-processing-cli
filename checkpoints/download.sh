
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




