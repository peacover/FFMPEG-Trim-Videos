# import subprocess
# import sys
# import os

# # Default resolution for mobile screens (reduced to 720p for smaller file size)
# DEFAULT_WIDTH = 720
# DEFAULT_HEIGHT = 1280

# def get_video_bitrate(input_file):
#     ffprobe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
#     output = subprocess.check_output(ffprobe_cmd, shell=True).decode('utf-8').strip()
#     return int(output) if output.isdigit() else None

# def trim_video(input_file, output_file, target_width=DEFAULT_WIDTH, target_height=DEFAULT_HEIGHT):
#     # Get video dimensions
#     ffprobe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{input_file}"'
#     dimensions = subprocess.check_output(ffprobe_cmd, shell=True).decode('utf-8').strip().split('x')
#     width, height = map(int, dimensions)

#     # Calculate crop parameters
#     crop_width = min(width, int(height * target_width / target_height))
#     crop_height = min(height, int(width * target_height / target_width))
#     x_offset = (width - crop_width) // 2
#     y_offset = (height - crop_height) // 2

#     # Get original video bitrate
#     original_bitrate = get_video_bitrate(input_file)
    
#     # Calculate target bitrate (25% of original for aggressive compression)
#     target_bitrate = int(original_bitrate * 0.25)

#     # Construct FFmpeg command
#     ffmpeg_cmd = [
#         'ffmpeg',
#         '-i', input_file,
#         '-filter:v', f'crop={crop_width}:{crop_height}:{x_offset}:{y_offset},scale={target_width}:{target_height}',
#         '-c:v', 'libx264',
#         '-preset', 'veryslow',  # Slowest preset for best compression
#         '-crf', '30',  # Even higher CRF value for more aggressive compression
#         '-maxrate', f'{target_bitrate}',
#         '-bufsize', f'{target_bitrate * 2}',
#         '-profile:v', 'baseline',  # Use baseline profile for better compatibility
#         '-level', '3.0',
#         '-an',  # Remove audio
#         '-movflags', '+faststart',  # Optimize for web streaming
#         '-y',  # Overwrite output file if it exists
#         output_file
#     ]

#     # Execute FFmpeg command
#     process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

#     # Print FFmpeg logs
#     for line in process.stdout:
#         print(line, end='')

#     # Wait for the process to finish
#     process.wait()

#     if process.returncode != 0:
#         print(f"Error: FFmpeg command failed with return code {process.returncode}")
#         sys.exit(1)

# if __name__ == "__main__":
#     if len(sys.argv) < 3 or len(sys.argv) > 5:
#         print("Usage: python script.py <input_file> <output_file> [target_width] [target_height]")
#         print(f"Default resolution: {DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
#         sys.exit(1)

#     input_file = sys.argv[1]
#     output_file = sys.argv[2]

#     if not os.path.exists(input_file):
#         print(f"Error: Input file '{input_file}' does not exist.")
#         sys.exit(1)

#     target_width = DEFAULT_WIDTH
#     target_height = DEFAULT_HEIGHT

#     if len(sys.argv) == 5:
#         target_width = int(sys.argv[3])
#         target_height = int(sys.argv[4])

#     trim_video(input_file, output_file, target_width, target_height)
#     print(f"Video trimmed and saved as {output_file}")
#     print(f"Output resolution: {target_width}x{target_height}")

#     # Print file size comparison
#     input_size = os.path.getsize(input_file)
#     output_size = os.path.getsize(output_file)
#     size_change = (output_size - input_size) / input_size * 100

#     print(f"Input file size: {input_size / 1024 / 1024:.2f} MB")
#     print(f"Output file size: {output_size / 1024 / 1024:.2f} MB")
#     print(f"Size change: {size_change:.2f}% ({'increase' if size_change > 0 else 'decrease'})")


import subprocess
import os
import shutil

# Default resolution for mobile screens (reduced to 720p for smaller file size)
DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1280

# Fixed folder names
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

def get_video_bitrate(input_file):
    ffprobe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
    output = subprocess.check_output(ffprobe_cmd, shell=True).decode('utf-8').strip()
    return int(output) if output.isdigit() else None

def trim_video(input_file, output_file, target_width=DEFAULT_WIDTH, target_height=DEFAULT_HEIGHT):
    # Get video dimensions
    ffprobe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{input_file}"'
    dimensions = subprocess.check_output(ffprobe_cmd, shell=True).decode('utf-8').strip().split('x')
    width, height = map(int, dimensions)

    # Calculate crop parameters
    crop_width = min(width, int(height * target_width / target_height))
    crop_height = min(height, int(width * target_height / target_width))
    x_offset = (width - crop_width) // 2
    y_offset = (height - crop_height) // 2

    # Get original video bitrate
    original_bitrate = get_video_bitrate(input_file)
    
    # Calculate target bitrate (25% of original for aggressive compression)
    target_bitrate = int(original_bitrate * 0.25) if original_bitrate else 1000000

    # Construct FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-filter:v', f'crop={crop_width}:{crop_height}:{x_offset}:{y_offset},scale={target_width}:{target_height}',
        '-c:v', 'libx264',
        '-preset', 'veryslow',  # Slowest preset for best compression
        '-crf', '30',  # Even higher CRF value for more aggressive compression
        '-maxrate', f'{target_bitrate}',
        '-bufsize', f'{target_bitrate * 2}',
        '-profile:v', 'baseline',  # Use baseline profile for better compatibility
        '-level', '3.0',
        '-an',  # Remove audio
        '-movflags', '+faststart',  # Optimize for web streaming
        '-y',  # Overwrite output file if it exists
        output_file
    ]

    # Execute FFmpeg command
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Print FFmpeg logs
    for line in process.stdout:
        print(line, end='')

    # Wait for the process to finish
    process.wait()

    if process.returncode != 0:
        print(f"Error: FFmpeg command failed with return code {process.returncode}")
        return False

    return True

def process_videos():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Input folder '{INPUT_FOLDER}' does not exist.")
        return

    # Remove output folder if it exists
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
        print(f"Removed existing output folder: {OUTPUT_FOLDER}")

    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Process each video in the input folder
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, f"processed_{filename}")

            print(f"Processing: {filename}")
            success = trim_video(input_path, output_path)

            if success:
                print(f"Video processed and saved as {output_path}")
                # Print file size comparison
                input_size = os.path.getsize(input_path)
                output_size = os.path.getsize(output_path)
                size_change = (output_size - input_size) / input_size * 100

                print(f"Input file size: {input_size / 1024 / 1024:.2f} MB")
                print(f"Output file size: {output_size / 1024 / 1024:.2f} MB")
                print(f"Size change: {size_change:.2f}% ({'increase' if size_change > 0 else 'decrease'})")
            else:
                print(f"Failed to process: {filename}")

            print("\n")  # Add a blank line between video processing outputs

if __name__ == "__main__":
    process_videos()
    print("All videos processed.")