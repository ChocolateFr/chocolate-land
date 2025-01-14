import log
import utils
import watchdict
import shutil
import sys

logger = log.logging

def run_command(command):
    """Helper function to run shell commands and log their output."""
    try:
        logger.info(f"Running command: {command}")
        utils.cmd(command)
    except Exception as e:
        logger.error(f"Command failed: {command}, Error: {e}")
        sys.exit(1)

def setup_config(path, config_path):
    """Helper function to ensure directories and load config."""
    
    logger.info(f"Loading config from {config_path}...")
    config = watchdict.WatchDict(config_path)
    return config

def configure_rofi(path, config):
    """Configure rofi from the config."""
    logger.info('Configuring rofi...')
    rofi = path.read('dotfiles/config.rasi')
    
    # Replace all placeholders with corresponding values from config using replace
    rofi = rofi.replace("{base}", config['base'])
    rofi = rofi.replace("{base_light}", config['base_light'])
    rofi = rofi.replace("{borders}", config['borders'])
    rofi = rofi.replace("{text}", config['text'])
    rofi = rofi.replace("{highlight}", config['highlight'])
    rofi = rofi.replace("{blue}", config['blue'])
    
    path.write('.config/rofi/config.rasi', rofi)
    logger.info('Rofi is ready.')

def configure_hypr(path, config):
    """Configure hyprland from the config."""
    logger.info('Configuring hyprland...')
    bord = config['borders'][1:] + 'ff'
    hypr = path.read('dotfiles/hyprland.conf')
    
    # Replace placeholders with values
    hypr = hypr.replace("{borders}", bord)
    hypr = hypr.replace("{border_width}", str(config['border_width']))
    
    path.write('.config/hypr/styling.conf', hypr)
    logger.info('Hyprland dotfiles are ready.')

def configure_mako(path, config):
    """Configure mako from the config."""
    logger.info('Configuring mako...')
    mako = path.read('dotfiles/config')
    
    # Replace placeholders with values
    mako = mako.replace("{borders}", config['borders'])
    mako = mako.replace("{highlight}", config['highlight'])
    mako = mako.replace("{base}", config['base'])
    mako = mako.replace("{text}", config['text'])
    
    path.write('.config/mako/config', mako)
    logger.info('Mako is ready.')

def configure_waybar(path, config):
    """Configure waybar from the config."""
    logger.info('Configuring waybar...')
    waybar = path.read('dotfiles/style.css')
    
    # Replace placeholders with values
    waybar = waybar.replace("{base}", config['base'])
    waybar = waybar.replace("{text}", config['text'])
    
    path.write('.config/waybar/style.css', waybar)
    logger.info('Waybar is ready.')

def install_dependencies():
    """Install the required packages."""
    logger.info('Installing required packages...')
    run_command('sudo pacman -S hyprland')
    run_command('sudo pacman -S mako')
    run_command('sudo pacman -S kitty')
    run_command('sudo pacman -S rofi')
    run_command('sudo pacman -S ttf-jetbrains-mono-nerd')
    run_command('sudo pacman -S waybar')
    run_command('pip install psutil watchdict requests --break-system-packages')
    run_command('sudo pacman -S wf-recorder')
    run_command('sudo pacman -S wl-clipboard')
    run_command('sudo pacman -S jq')
    logger.info('All dependencies are installed.')

def write_configs(path, waybar, mako, hypr):
    """Write the config files to the respective locations."""
    logger.info('Writing config files...')
    path.write('.config/waybar/config', path.read('dotfiles/waybar'))
    path.write('.config/waybar/style.css', waybar)
    path.write('.config/mako/config', mako)
    path.write('.config/hypr/styling.conf', hypr)
    logger.info('Config files written successfully.')

def main():
    logger.info('Chocolate-land installer started initializing...')
    
    path = utils.Home()
    
    # Ensure config folders exist
    config_folders = ['.config/hypr', '.config/mako', '.config/rofi', '.config/kitty']
    for folder in config_folders:
        path.ensure(folder)
    
    logger.info('Checking and loading the config file...')
    config_path = path['.chocorc']
    config = setup_config(path, config_path)
    
    # Configure dotfiles
    configure_hypr(path, config)
    configure_rofi(path, config)
    configure_mako(path, config)
    configure_waybar(path, config)
    
    # Install required packages
    install_dependencies()
    
    # Ask user to continue with copying config files
    ask = input('All required tasks are complete. Do you want to copy the config files and finish the installation? [y/n]: ')
    if ask != 'y':
        logger.warning('User opted not to proceed with the installation.')
        print('Installation aborted!')
        sys.exit(0)
    path.ensure('Pictures/Wallpapers')
    path.ensure('.config/scripts')
    shutil.copytree('scripts', path['.config/scripts'])
    print('Installation is finished. please reboot your pc.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
