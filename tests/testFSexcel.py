'''
Created on 15 ago. 2017

@author: Val
'''
import unittest
from pyFS.pyfs_open_xlsx import getFSfamily
import os
from pyGeni import profile
import datetime
from tests.FIXTURES import SANDBOX_MAIN_ADDRESS

class Test(unittest.TestCase):
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        #We used the sandbox here
        self.stoken = os.environ['SANDBOX_KEY']
        profile.s.update_geni_address("https://www.sandbox.geni.com")
        profile.s.VERIFY_INPUT = False
        #We locate the folder here
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2



    def test_fs_reader(self):
        '''
        Test reading an input file
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado.xlsx")
        fsclass = getFSfamily(input_file)
        assert(fsclass.correct_execution)
        assert(fsclass.initial_column == "A")
        assert(fsclass.initial_row == 6)
        assert(fsclass.sheet_title == "Sheet0")

    def test_wrong_inputs(self):
        '''
        Test FS reader wrong inputs are detected
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado.xlsx")
        fsclass = getFSfamily(input_file, naming_convention = "wrong_input")
        self.assertFalse(fsclass.correct_execution)
    
    def test_empty_excel(self):
        '''
        Test an empty excel from FS
        '''
        input_file = os.path.join(self.filelocation, "fs-Empty.xlsx")
        fsclass = getFSfamily(input_file)
        self.assertFalse(fsclass.correct_execution)
            
    def test_issue_double_names(self):
        '''
        Test composed names
        '''
        input_file = os.path.join(self.filelocation, "fs-MolpecerezGomez.xls")
        fsclass = getFSfamily(input_file, naming_convention = "spanish_surname")
        for profile in fsclass.profiles:
            assert(profile.gen_data["name"] in ["Eusebio", "Petra", "Román", "Gila", "Segunda", "Julián", "Petra Regalada"]) 
    
    def test_not_existing_file(self):
        '''
        Test file not existing
        '''
        input_file = os.path.join(self.filelocation, "fs-DOESNOTEXIST.xls")
        fsclass = getFSfamily(input_file, naming_convention = "spanish_surname")
        self.assertFalse(fsclass.correct_execution)
    
    def test_fs_reader_single_person(self):
        '''
        Tests in detail the correct reading of a person
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado-singleperson.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname")
        this_profile = fsclass.profiles[0]
        
        assert(fsclass.correct_execution)
        assert (len(fsclass.profiles) == 1)
        assert(this_profile.gen_data["gender"] == "M")
        assert(this_profile.gen_data["name"] == "Wenceslao")
        assert(this_profile.gen_data["surname"] == "Potente Asegurado")
        assert(this_profile.gen_data["birth_date"] == datetime.date(1862,9,28))
        assert(this_profile.gen_data["accuracy_birth_date"] == "EXACT")
        assert(this_profile.gen_data["baptism_date"] == datetime.date(1862,10,2))
        assert(this_profile.gen_data["accuracy_baptism_date"] == "EXACT")
        assert(this_profile.gen_data["residence_date"] == datetime.date(1862,1,1))
        assert(this_profile.gen_data["accuracy_residence_date"] == "ABOUT")
        assert(this_profile.gen_data["death_date"] == datetime.date(1863,6,28))
        assert(this_profile.gen_data["accuracy_death_date"] == "EXACT")
        assert(this_profile.gen_data["burial_date"] == datetime.date(1863,6,28))
        assert(this_profile.gen_data["accuracy_burial_date"] == "EXACT")
        assert(this_profile.gen_data["death_place"]["city"] == 'La Parrilla')
        assert(this_profile.gen_data["birth_place"]["city"] == 'La Parrilla')
        assert(this_profile.gen_data["residence_place"]["state"] == 'Castile and León')
        assert(this_profile.gen_data["baptism_place"]["place_name"] == 'Nuestra Señora de los Remedios')
        assert(len(this_profile.gen_data["nicknames"]))
        assert("Wenceslao Potente" in this_profile.gen_data["nicknames"])
    
    def test_name_with_particle(self):
        '''
        Test bug of names with particle
        '''
        input_file = os.path.join(self.filelocation, "fs-CaballeroBargas.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname", language = "es")
        
        juan_in = False
        
        for prof in fsclass.profiles:
            if ("juan de" in prof.gen_data["name"].lower()): juan_in = True
        
        self.assertFalse(juan_in)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_fs_reader']
    unittest.main()