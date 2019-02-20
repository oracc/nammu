'''
Copyright 2015 - 2018 University College London.

This file is part of Nammu.

Nammu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nammu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import zipfile
import shutil
import yaml
import logging
import re
import urllib
from java.lang import ClassLoader, System
from java.awt import Font

'''
This is a compilation of methods to be used from all Nammu classes.
'''


def set_font(font_size):
    '''
    Loads font from resources' ttf file.
    DejaVuSans doesn't work in Retina display screens properly, so check OS,
    if OSX then use Monaco instead.
    '''
    # Take into account user preferred font size
    if "mac" in System.getProperty("os.name").lower():
        font = Font("Monaco", Font.PLAIN, font_size)
    else:
        path_to_ttf = 'resources/fonts/dejavu/ttf/DejaVuSans.ttf'
        loader = ClassLoader.getSystemClassLoader()
        stream = loader.getResourceAsStream(path_to_ttf)
        font = Font.createFont(Font.TRUETYPE_FONT, stream)
        font = font.deriveFont(Font.PLAIN, font_size)
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


def get_yaml_config(yaml_filename):
    '''
    Load contents of <yaml_filename> into dictionary.
    Note file_handler's filename needs to be an absolute path and hence
    manually changed from here.
    '''
    # Create helper object to load log config from jar resources
    # Load config details from yaml file.
    # Note getResource returns a java.net.URL object which is incompatible
    # with Python's open method, so we need to work around it by copying the
    # file to the home directory and open from there.
    yaml_path = 'resources/config/{}'.format(yaml_filename)
    loader = ClassLoader.getSystemClassLoader()
    config_file_url = loader.getResource(yaml_path)
    # In Unix getResource returns the path with prefix "file:" but in
    # Windows prefix is "jar:file:"
    path_to_jar = str(config_file_url).split('file:')[1]
    # The path will be of the form /path/to/jar!path/inside/jar
    # Take everything up to the final !, in case previous parts also contain !
    path_to_jar = path_to_jar.rsplit('!', 1)[0]
    # Decode any special characters contained in the path so that, for example,
    # we use 'dir name' instead of 'dir%20name'
    # NB: The standard way to do it is to create a URI from the URL, which will
    # automatically handle the encoding, and then go back to a URL or String.
    # However, the URI class doesn't seem to handle the jar:file: prefix well,
    # so using urllib directly seems a better solution.
    path_to_jar = urllib.unquote(path_to_jar)

    path_to_config = get_log_path(yaml_filename)

    # Check if log config file exists already.
    # If it doesn't, paste it from JAR's resources to there.
    # If it does, check is up to date with latest version
    if not os.path.isfile(path_to_config):
        copy_yaml_to_home(path_to_jar, yaml_path, path_to_config)
    else:
        # We are running from the JAR file, not the local console
        update_yaml_config(path_to_jar, yaml_path, path_to_config)

    # Load local YAML file and perform required patches on the settings in
    # memory if the settings version is different between the jar and the local
    # file. Ensures that memory and file settings always match.
    (jar_config, local_config,
     jar_version, local_version) = get_config_versions(path_to_jar, yaml_path,
                                                       path_to_config)

    if yaml_filename == 'settings.yaml':
        if different_versions(jar_version, local_version):
            return patch_config(local_config)

    return local_config


def patch_config(yaml):
    '''
    Wrapper around the config patching methods.
    '''
    yaml = fix_old_default_project_yaml(yaml)
    yaml = patch_styles(yaml)
    return patch_server_settings(yaml)


def fix_old_default_project_yaml(yaml):
    '''
    Method to ensure compatability between old config files and verisons
    of nammu > 0.8
    '''
    if 'projects' in yaml.keys():
        if isinstance(yaml['projects']['default'], basestring):
            yaml['projects']['default'] = [yaml['projects']['default']]
    return yaml


def patch_styles(yaml):
    '''
    Following the release of 1.0 any user with a config generated by version
    0.8 will crash without this method to restructure the style parts of the
    config file.
    '''
    if 'console_style' in yaml.keys():
        yaml['console_style'] = {'fontsize': {'default': 11, 'user': 11},
                                 'background_color': {'default': 'Gray',
                                                      'user': 'Gray'},
                                 'font_color': {'default': 'Black',
                                                'user': 'Black'}}

    if 'edit_area_style' in yaml.keys():
        yaml['edit_area_style'] = {'fontsize': {'default': 14, 'user': 14}}

    return yaml


def patch_server_settings(yaml):
    '''
    Following the change in server address we need to update user's config
    files without overwriting their other settings.
    '''
    old_url = 'http://oracc.museum.upenn.edu'
    new_url = 'http://build-oracc.museum.upenn.edu'
    if 'servers' in yaml.keys() and 'upenn' in yaml['servers'].keys():
        if yaml['servers']['upenn']['url'] == old_url:
            yaml['servers']['upenn']['url'] = new_url

    return yaml


def different_versions(version1, version2):
    '''
    Examine two version tuples. Return 0 if unequal, 1 if equal.
    http://stackoverflow.com/questions/1714027/version-number-comparison
    '''
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
    return cmp(normalize(version1), normalize(version2))


def get_config_versions(path_to_jar, yaml_path, path_to_config):
    '''
    Method to return the jar and local config files and their versions.
    '''
    try:
        jar_contents = zipfile.ZipFile(path_to_jar, 'r')
    except zipfile.BadZipfile:
        jar_config = yaml.load(open(path_to_jar, 'r'))
    else:
        jar_config = yaml.load(jar_contents.open(yaml_path))

    local_config = yaml.load(open(path_to_config, 'r'))
    jar_version = str(jar_config['version'])
    local_version = str(local_config['version'])

    return jar_config, local_config, jar_version, local_version


def update_yaml_config(path_to_jar, yaml_path, path_to_config, verbose=False,
                       test_mode=False):
    '''
    Load local config and jar config. Compare versions. If they differ,
    it will scan the key-value pairs, and add new key-values not present
    in the local config. If the same keys are present in the local and jar,
    the local values will be maintained.
    It also needs to compare what's in the jar and add new dictionaries to the
    local jar.
    '''
    logger = logging.getLogger("NammuController")

    (jar_config, local_config,
     jar_version, local_version) = get_config_versions(path_to_jar, yaml_path,
                                                       path_to_config)

    if different_versions(jar_version, local_version):
        d = {}
        logger.debug("Comparing install and local settings files...")
        for key in jar_config:
            if(isinstance(jar_config[key], dict)):  # Nested dics within a key
                if key in local_config:
                    tmp = {}  # for the nested dics
                    for sub_key in jar_config[key]:
                        if sub_key in local_config[key]:
                            logger.debug("%s: %s: %s --> Using local values.",
                                         key,
                                         sub_key,
                                         jar_config[key][sub_key])
                            tmp[sub_key] = local_config[key][sub_key]
                        else:
                            logger.debug("%s: %s: %s --> Using jar values.",
                                         key,
                                         sub_key,
                                         jar_config[key][sub_key])
                            tmp[sub_key] = jar_config[key][sub_key]
                    d[key] = tmp
                else:
                    logger.debug("%s doesnt exist locally, creating...", key)
                    d[key] = jar_config[key]
            else:  # One level deep dictionary
                if key in local_config:
                    logger.debug("%s: %s --> Using local values.",
                                 key,
                                 jar_config[key])
                    d[key] = local_config[key]
                else:
                    logger.debug("%s: %s --> Using jar values.",
                                 key,
                                 jar_config[key])
                    d[key] = jar_config[key]
        logger.debug("Updating version number in local config: %s --> %s",
                     local_config['version'], jar_config['version'])
        d['version'] = jar_config['version']
        if test_mode:  # This is for running tests, a dic is returned to check
            return d  # keys are correct.
        else:
            # Need to apply the patching to correct any problems between
            # version 0.8 and version 1.0
            d = patch_config(d)
            save_yaml_config(d)
    else:
        return


def save_yaml_config(config):
    '''
    Overwrites settings with given config dict.
    '''
    # Get config path
    path_to_config = get_log_path('settings.yaml')

    # Save given config in yaml file
    with open(path_to_config, 'w') as outfile:
        outfile.write(yaml.safe_dump(config))


def copy_yaml_to_home(jar_file_path, source_rel_path, target_path):
    '''
    Opens Nammu's jar as a zip file, looks for the yaml config file and copies
    it to ~/.nammu.
    '''
    try:
        with zipfile.ZipFile(jar_file_path, 'r') as zf:
            for zi in zf.infolist():
                fn = zi.filename
                if fn.lower() == source_rel_path:
                    source_file = zf.open(fn)
                    target_file = file(target_path, "wb")
                    with source_file, target_file:
                        shutil.copyfileobj(source_file, target_file)
    except zipfile.BadZipfile:
        shutil.copyfileobj(file(source_rel_path, "wb"),
                           file(target_path, "wb"))


def find_image_resource(name):
    # Create helper object to load icon images in jar
    loader = ClassLoader.getSystemClassLoader()
    # Load image
    return loader.getResource("resources/images/" + name.lower() + ".png")
