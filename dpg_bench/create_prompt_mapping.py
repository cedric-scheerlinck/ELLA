import json
from pathlib import Path


def create_prompt_mapping() -> None:
    prompts_path = Path("dpg_bench/prompts")
    output_dir = Path("dpg_bench")
    if not prompts_path.exists():
        raise FileNotFoundError(f"Prompts directory not found: {prompts_path}")
    
    filename_from_prompt = {}
    prompt_files = sorted(prompts_path.glob("*.txt"))
    for prompt_file in prompt_files:
        prompt_text = prompt_file.read_text().strip()
        prompt_filename = prompt_file.stem
        if prompt_text in filename_from_prompt:
            raise ValueError(f"Duplicate prompt text found: {prompt_text}")
        filename_from_prompt[prompt_text] = prompt_filename
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "filename_from_prompt.json"
    with open(output_path, 'w') as f:
        json.dump(filename_from_prompt, f, indent=2)

    print(f"Saved {len(filename_from_prompt)} prompt mappings to {output_path}")


if __name__ == "__main__":
    create_prompt_mapping()

