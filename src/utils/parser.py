import configparser
 
class ConfigManager:
    def __init__(self, config_file_path):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  
        self.config_file_path = config_file_path
        self.config.read(config_file_path)
        
        self.type_map = {
            'CONFIG': {
                'LOG_FILE_PATH' : str,
                'LOG_FILE_NAME' : str,
                'LOG_LEVEL' : str,
            }
        }
        
    def get_config_dict(self):
        all_config_dict = {}
            
        for section in self.config.sections():
            section_dict = {}
            
            if section not in self.type_map:
                print(f"Warning: Section {section} is not in type_map")
                continue
            
            for key, value in self.config[section].items():
                if key in self.type_map[section]:
                    value_type = self.type_map[section][key]
                    section_dict[key] = value_type(value)
                else:
                    section_dict[key] = value
            
            all_config_dict[section] = section_dict
            
        return all_config_dict