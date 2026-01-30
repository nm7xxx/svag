from PIL import Image
import numpy as np
import os
from pathlib import Path


def convert_folder(src_dir, dst_dir, exts=(".png", ".jpg", ".jpeg", ".bmp")):
    """将整个文件夹中的 8bit 红外图像批量转换为 16bit TIFF。

    src_dir: 输入文件夹路径，里面是 8bit 红外图像（png/jpg/bmp 等）。
    dst_dir: 输出文件夹路径，将在其中按相同子目录结构保存 16bit tiff。
    exts:    认为是图像的扩展名列表（小写）。
    """

    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)

    for src_path in src_dir.rglob("*"):
        if not src_path.is_file():
            continue
        if src_path.suffix.lower() not in exts:
            continue

        # 读原图（8bit 灰度）
        img8 = Image.open(src_path).convert("L")
        arr8 = np.array(img8)
        print("original:", src_path, arr8.dtype, arr8.shape)

        if arr8.dtype != np.uint8:
            arr8 = arr8.astype(np.uint8)

        # 8bit -> 16bit 映射：0~255 -> 0~65535
        arr16 = (arr8.astype(np.uint16) * 257)

        # 目标路径：保持相对目录结构，扩展名改为 .tiff
        rel = src_path.relative_to(src_dir)
        dst_path = dst_dir / rel.with_suffix(".tiff")
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        img16 = Image.fromarray(arr16)
        img16.save(dst_path)
        print("saved   :", dst_path)


if __name__ == "__main__":
    # 修改下面两个路径为你的输入/输出文件夹
    SRC_DIR = r"E:\your_8bit_ir_folder"
    DST_DIR = r"E:\your_16bit_ir_folder"
    
    convert_folder(SRC_DIR, DST_DIR)