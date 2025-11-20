import json
import shutil
from pathlib import Path
from tqdm import tqdm
import argh


def convert_images(input_dir: str, output_dir: str) -> None:
    """
    Convert images from sample directories to DPG-Bench format.
    
    Args:
        input_dir: Directory containing sample_XXXXX/ subdirectories
        output_dir: Output directory for converted images
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    filename_from_prompt_file = Path("dpg_bench/filename_from_prompt.json")
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")
    
    if not filename_from_prompt_file.exists():
        raise FileNotFoundError(f"Filename from prompt file not found: {filename_from_prompt_file}")
    
    with open(filename_from_prompt_file, 'r', encoding='utf-8') as f:
        filename_from_prompt = json.load(f)
    
    output_path.mkdir(parents=True, exist_ok=True)
    sample_dirs = sorted([d for d in input_path.iterdir() if d.is_dir() and d.name.startswith("sample_")])
    
    converted_count = 0
    skipped_count = 0
    error_count = 0
    
    for sample_dir in tqdm(sample_dirs):
        prompt_file = sample_dir / "prompt.txt"
        src_image_path = sample_dir / "image.png"
        
        try:
            prompt_text = prompt_file.read_text().strip()
        except Exception as e:
            print(f"Error reading prompt.txt from {sample_dir.name}: {e}")
            error_count += 1
            continue        
        if prompt_text not in filename_from_prompt:
            print(f"Warning: No mapping found for prompt in {sample_dir.name}")
            print(f"  Prompt preview: {prompt_text[:100]}...")
            skipped_count += 1
            continue
        
        dst_image_path = output_path / f"{filename_from_prompt[prompt_text]}.png"
        
        try:
            shutil.copy2(src_image_path, dst_image_path)
            converted_count += 1
        except Exception as e:
            print(f"Error copying image from {sample_dir.name}: {e}")
            error_count += 1
            continue
    
    print("\n" + "="*60)
    print("Conversion Summary:")
    print(f"  Converted: {converted_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total processed: {converted_count + skipped_count + error_count}")
    print("="*60)
    print(f"Converted {converted_count} images to {output_path}")


if __name__ == "__main__":
    argh.dispatch_command(convert_images)

