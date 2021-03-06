from templateFileGeneration import *


class GenerateCHeader(TemplateGeneration):

    FILE_ENDING = '.hpp'
    BIT_DEFINE_STRING = '\t\tconst int {2} = {1};\n'
    GENERAL_REGISTER_DEFINITION = '\tconst int {0} = {1}; //{2}\n'
    REGISTER_BIT_INFORMATION = '\tnamespace {0}_BITS\n\t{{\n{1}\t}}\n'
    COMPONENT_NAMING_AND_DEFINTION = 'namespace {0} /* IP Core Version: {1}*/\n{{\n{2}}}\n\n'
    AUTOGENERATION_HINT = '/* This file is automatically generated, don''t modify it!*/\n'
    INCLUDE_GUARD = '{0}_H'

    def _extract_register_information(self):
        ''' extraction of the slave register and all including bits '''
        return_string = ''
        keylist = sorted(self.parsed_file.register)
        for temp_reg in keylist:
            return_string += self.GENERAL_REGISTER_DEFINITION.format(self._extract_variable_name(temp_reg),
                                                                     self._calculate_register_offset(self.parsed_file.register[temp_reg].binary_coded[2:]),
                                                                     self._extract_read_write_option(self.parsed_file.register[temp_reg].option))
            return_string += self.REGISTER_BIT_INFORMATION.format(self._extract_variable_name(temp_reg),
                                                                  self._extract_bit_defintion(self.parsed_file.register[temp_reg].bit_definition))
        return return_string

    def _write(self):
        ''' write the whole file '''
        if(not self.INCLUDE_GUARD_WRITTEN):
            self.output_file.write('#ifndef {0}\n#define {0}\n\n'.format(self.INCLUDE_GUARD.format(self.output_file_name.format("").upper())))
        self.output_file.write(self.AUTOGENERATION_HINT)
        self.output_file.write(self.COMPONENT_NAMING_AND_DEFINTION.format(self.parsed_file.component_name,
                                                                          self.parsed_file.ip_core_version,
                                                                          self._extract_register_information()))
