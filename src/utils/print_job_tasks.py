#  Copyright 2025 The Board of Trustees of the University of Illinois. All Rights Reserved.
#
#  Licensed under the terms of Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  The License is included in the distribution as LICENSE file.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

tiles_folder_names = ["PAL1999_B6_sample71_slide1", "PAL1999_B6_sample55", "PAL1999_B2_sample95_slide1",
                      "PAL1999_B6_sample17", "PAL1999_C3_sample13_slide1", "PAL1999_B6_sample20",
                      "PAL1999_B2_sample136_slide1", "PAL1999_B2_sample109_slide1", "PAL1999_B2_sample86_slide1",
                      "PAL1999_B2_sample76_slide1", "PAL1999_B2_sample92_slide1", "PAL1999_B2_sample122_slide1",
                      "PAL1999_B2_sample101_slide1", "PAL1999_B2_sample97_slide1", "PAL1999_B2_sample134_slide1",
                      "PAL1999_B2_sample120_slide1", "PAL1999_B2_sample78_slide1", "PAL1999_B2_sample103_slide1",
                      "PAL1999_B2_sample93_slide1", "PAL1999_B2_sample98_slide1", "PAL1999_B2_sample87_slide1",
                      "PAL1999_B2_sample135_slide1", "PAL1999_B2_sample132_slide1", "PAL1999_B2_sample127_slide1",
                      "PAL1999_B2_sample72_slide1", "PAL1999_B2_sample71_slide1"]

for folder in tiles_folder_names:
    print(
        "srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK zip -r " + folder + ".zip " + folder + " &")
