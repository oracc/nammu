"""
Compilation of methods to be used from all Nammu classes.
"""
import os
import zipfile
import shutil
from java.lang import ClassLoader, System
from java.io import InputStreamReader, BufferedReader
from java.awt import Font


def set_font(font_name):
    """
    Loads font from resources' ttf file.
    """
    path_to_ttf = 'resources/fonts/dejavu/ttf/{}.ttf'.format(font_name)
    loader = ClassLoader.getSystemClassLoader()
    stream = loader.getResourceAsStream(path_to_ttf)
    font = Font.createFont(Font.TRUETYPE_FONT, stream)
    font = font.deriveFont(Font.PLAIN, 14)
    return font


def get_home_env_var():
    '''
    Works out user's OS and returns appropriate path to home directory.
    In Unix it should be $HOME and in Windows is %USERPROFILE%.
    '''
    # Check user's OS to save log in appropriate place.
    # Note it has to be done with Java libraries and not python os, since
    # Python's os module returns always Java as OS.
    os_name = System.getProperty("os.name").lower()
    unix_os = ['mac', 'nix', 'nux', 'sunos', 'solaris']
    env_var_name = ''

    if any(x in os_name for x in unix_os):
        env_var_name = "HOME"
    elif 'win' in os_name:
        # Windows machines don't always have a %HOME% variable in place, but
        # they should always have %USERPROFILE% set up pointing to ~
        env_var_name = "USERPROFILE"

    return env_var_name


def get_log_path(filename):
    '''
    Works out which path nammu.log and nammu.yaml should be saved to.
    Depends on user's OS and there are no permissions to save it in
    /var/log or %APPDATA%, so it'll be saved in ~/.nammu folder.
    If home_env_var is not set, then saves it in the local folder.
    '''
    log_dir = ''
    try:
        log_dir = os.environ['NAMMU_CONFIG_PATH']
    except KeyError:
        home_env_var = get_home_env_var()
        try:
            log_dir = os.path.join(os.environ[home_env_var], '.nammu')
        except KeyError:
            # Has to be a print statement since log is not yet in place at
            # this stage
            print "Couldn't find {} environment variable.".format(home_env_var)
            print "Saving log file in current directory."

    # If Nammu has never been run, the path won't exist, so create it.
    if not os.path.exists(log_dir) and log_dir is not "":
        try:
            os.makedirs(log_dir)
        except OSError:
            msg = "Couldn't create directory to store Nammu's log in {}."
            print msg.format(log_dir)
            print "Saving log file and configuration in current folder."

    return os.path.join(log_dir, filename)


def get_yaml_config():
    '''
    Load contents of logging.yaml into dictionary.
    Note file_handler's filename needs to be an absolute path and hence
    manually changed from here.
    '''
    # Create helper object to load log config from jar resources
    # Load config details from yaml file.
    # Note getResource returns a java.net.URL object which is incompatible
    # with Python's open method, so we need to work around it by copying the
    # file to the home directory and open from there.
    yaml_filename = 'logging.yaml'
    yaml_path = 'resources/config/{}'.format(yaml_filename)
    loader = ClassLoader.getSystemClassLoader()
    config_file_url = loader.getResource(yaml_path)
    # In Unix getResource returns the path with prefix "file:" but in
    # Windows prefix is "jar:file:"
    path_to_jar = str(config_file_url).split('file:')[1]
    path_to_jar = path_to_jar.replace('!{}'.format(yaml_path), '')

    path_to_config = get_log_path(yaml_filename)

    # Check if log config file exists already. If so, just read it.
    # Otherwise, paste it from JAR's resources to there.
    if not os.path.isfile(path_to_config):
        get_ver(path_to_jar, yaml_path, path_to_config)

    # Load YAML config
    # This is a temporary hack to work around the mvn test stage not finding
    # yaml
    try:
        import yaml
    except:
        pass

    yaml_dict = yaml.load(open(path_to_config, 'r'))

    # Replace user given basename with absolute path to log file
    logfile = yaml_dict['handlers']['file_handler']['filename']
    yaml_dict['handlers']['file_handler']['filename'] = get_log_path(logfile)

    return yaml_dict


def get_ver(jar_file_path, source_rel_path, target_path):
    '''
    Opens Nammu's jar as a zip file, looks for the yaml config file and copies
    it to ~/.nammu.
    '''
    zf = zipfile.ZipFile(jar_file_path, 'r')
    try:
        lst = zf.infolist()
        for zi in lst:
            fn = zi.filename
            if fn.lower() == source_rel_path:
                source_file = zf.open(fn)
                target_file = file(target_path, "wb")
                with source_file, target_file:
                    shutil.copyfileobj(source_file, target_file)
    finally:
        zf.close()
