import os
import numpy as np
from PIL import Image
import time
from pathlib import Path
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_modality_lut, apply_voi_lut
import argparse

parser = argparse.ArgumentParser(description="Convert DICOM files to PNG")
parser.add_argument("-i", "--input_dir", type=str, required=True, help="Input directory containing DICOM files")
parser.add_argument("-o", "--output_dir", type=str, required=True, help="Output directory to save PNG files")
parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose information")
parser.add_argument("-c", "--contrast", action="store_true", help="Apply contrast enhancement")
# parser.add_argument("-s", "--skip-errors", action="store_true", help="Skip errors during conversion")
args = parser.parse_args()

input_dir, output_dir = args.input_dir, args.output_dir

try:
    if not Path(args.input_dir).exists():
        raise FileNotFoundError(f"Input directory {input_dir} does not exist")
    elif Path(args.input_dir).is_file():
        raise FileNotFoundError(f"Input directory {input_dir} is a file")
    else:
        Path(args.output_dir).mkdir(exist_ok=True)
        i = 0
        for f in sorted(list(Path(args.input_dir).rglob("*.dcm"))):
            i += 1
            ds = dcmread(f)
            
            img = ds.pixel_array

            if args.contrast:
                img = apply_modality_lut(img, ds)
                img = apply_voi_lut(img, ds)

            max_val, min_val = img.max(), img.min()
            img = (img - min_val) / (max_val - min_val) * 255
            img = img.astype(np.uint8)

            filename = f"{args.output_dir}/{f.stem}.png"
            Image.fromarray(img).save(filename)
            if args.verbose:
                print(f"{i:05d}: {filename.split('/')[-1]} saved")
        if i == 0:
            raise FileNotFoundError(f"No DICOM files found in {input_dir}")

    print(f"Conversion completed. {i} files saved in {output_dir}")
except Exception as e:
    print(f"Error: {e}")
os.system("pause")