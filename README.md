# SMX Photo Stitch

Given full SMX screenshots, this script will crop the images to show the impotant parts (scores), and compose multiple images into a single image.

This could be used for any images really, but the defaults are tuned to SMX (specifically the left player).

## Installation

On MacOS or Linux you should simply be able to plop this folder somewhere and run the `setupvenv.sh` script. This will create a python venv, upgrade pip and install the `requirements.txt`.

## Usage

Once installed you should be able to activate the venv with `. venv/bin/activate` and run the script.

Make sure you have the images you want to use in the `Input` folder, run the script `python ./stitch.sh` and the results will be in the `Output` folder.

Personally I like to keep the original images around so I manually move them to the `Finished Input` folder once I'm done.

Use `python ./stitch.sh -h` to see the various arguments you can use to modify how the images are processed.

## Notes

The defaults assume you are taking full resolution screenshots from your StepManiaX machine (usually during streaming). I personally use the `obs-screenshot-plugin` that can be found here: https://github.com/synap5e/obs-screenshot-plugin

## License

This project is licensed under the MIT License.
