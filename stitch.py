import argparse
import glob
from math import ceil, floor
from pathlib import Path
from typing import Generator, Optional, Sequence, Tuple

from loguru import logger
from PIL import Image


def main(args: Optional[Sequence[str]] = None) -> int:
    pargs = parse_args(args=args)

    in_path = pargs.input_path
    out_path = pargs.output_path
    max_count = pargs.max_count
    right_chop = 1 / pargs.right_chop
    top_chop = 1 / pargs.top_chop
    bottom_chop = 1 / pargs.bottom_chop

    logger.info("Running SMX Stitcher...")
    logger.info(f"Input Path: {in_path}")
    logger.info(f"Output Path: {out_path}")
    logger.info(f"Max Count: {max_count}")
    logger.info(f"Right Chop: {right_chop}")
    logger.info(f"Top Chop: {top_chop}")
    logger.info(f"Bottom Chop: {bottom_chop}")

    stitch(in_path, out_path, max_count, right_chop, top_chop, bottom_chop)

    return 0


def stitch(
    in_path: Path,
    out_path: Path,
    max_count: int,
    right_chop: float,
    top_chop: float,
    bottom_chop: float,
) -> None:
    x, y = find_image_size(in_path)

    # Multiply image size by chops
    x = int(x * right_chop)
    y = int(y * top_chop) - (y - int(y * bottom_chop))

    # Grab all images
    image_paths = glob.glob(str(in_path / "*"))

    for out_idx, images in enumerate(chunks(image_paths, max_count)):
        img_count = len(images)

        # Assume 2 Columns
        new_img = Image.new(
            "RGB", (x if img_count == 1 else x * 2, y * ceil(img_count / 2))
        )

        x_offset = 0
        y_offset = 0
        for idx, img_file in enumerate(images):
            x_offset = x * (idx % 2)
            y_offset = y * floor(idx / 2)
            offset = (x_offset, y_offset)

            with Image.open(img_file) as img:
                width, height = img.size

                img = img.crop(
                    (
                        0,
                        height - int(height * top_chop),
                        int(width * right_chop),
                        int(height * bottom_chop),
                    )
                )
                new_img.paste(img, box=offset)

        # Save original image size
        save_path = out_path / f"{out_idx}.png"
        logger.info(f"Saving: {save_path}")
        new_img.save(str(save_path), format="png")

        # Resize and save smaller image
        new_size = (new_img.size[0] // 2, new_img.size[1] // 2)
        new_img = new_img.resize(new_size, Image.Resampling.LANCZOS)
        save_path = out_path / f"{out_idx}_small.png"
        logger.info(f"Saving: {save_path}")
        new_img.save(str(save_path), format="png")


def chunks(lst: list, n: int) -> Generator:
    """
    Yield successive n-sized chunks from lst.

    If the result is less than n, make sure it's even, or a single image
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def find_image_size(path: Path) -> Tuple[int, int]:
    # Find first image file in dir
    for _file in glob.glob(str(path / "*")):
        # Open up the first file we find
        with Image.open(_file) as img:
            return img.size

    return 0, 0


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stitch SMX Scores")

    # Default Paths
    in_path = Path(__file__).parent / "Input"
    out_path = Path(__file__).parent / "Output"

    parser.add_argument(
        "-i", "--input-path", type=Path, default=in_path, help="Picture Input Path"
    )
    parser.add_argument(
        "-o", "--output-path", type=Path, default=out_path, help="Picture Output Path"
    )
    parser.add_argument(
        "-m", "--max-count", type=int, default=6, help="Max images per output"
    )

    def check_over_one(value: str) -> float:
        fval = float(value)
        if fval < 1.0:
            raise argparse.ArgumentTypeError(
                f"{value} must be greater than or equal to 1.0"
            )
        return fval

    parser.add_argument(
        "-r",
        "--right-chop",
        type=check_over_one,
        default=1.62,
        help="ratio of image to chop off the right side. Must be a float >= 1.0",
    )
    parser.add_argument(
        "-t",
        "--top_chop",
        type=check_over_one,
        default=1.08,
        help="ratio of image to chop off the top side. Must be a float >= 1.0",
    )
    parser.add_argument(
        "-b",
        "--bottom-chop",
        type=check_over_one,
        default=1.23,
        help="ratio of image to chop off the bottom size. Must be a float >= 1.0",
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
