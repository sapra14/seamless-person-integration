import os
from utils.background_removal import remove_background
from utils.blending import blend_images_auto_position

def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

def main():
    person_img_path = "/Users/sunitasapra/seamless_integration_project/assets/person.jpg"
    background_img_path = "/Users/sunitasapra/seamless_integration_project/assets/background.jpg"
    person_fg_path = "/Users/sunitasapra/seamless_integration_project/assets/person_fg.png"
    final_output_path = "/Users/sunitasapra/seamless_integration_project/results/blended_output.jpg"

    check_file_exists(person_img_path)
    check_file_exists(background_img_path)

    print("Removing background...")
    remove_background(person_img_path, person_fg_path)

    print("Blending person onto background with adjusted size and position...")
    blend_images_auto_position(
        fg_path=person_fg_path,
        bg_path=background_img_path,
        output_path=final_output_path,
        scale_ratio=0.55,  # slightly smaller person
        debug=False
    )

    print(f"Process completed! Final blended image saved at:\n{final_output_path}")

if __name__ == "__main__":
    main()
