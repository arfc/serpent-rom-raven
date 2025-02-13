# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Created March 17th, 2015

@author: talbpaul
"""
from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)

import os
import copy
import GenericParser
from CodeInterfaceBaseClass import CodeInterfaceBase
import sys
sys.path.append("/projects/sciteam/bahg/projects/raven/framework/CodeInterfaces/scripts")
import output_parser as op

class Serpent(CodeInterfaceBase):
  """
    Provides code to interface RAVEN to SERPENT
    The name of this class is to represent the type in the RAVEN input file

    This class is used as a generic code interface for Model.Code in Raven.  It expects
    input paremeters to be specified by input file, input files be specified by either
    command line or in a main input file, and produce a csv output.  It makes significant
    use of the 'clargs', 'fileargs', 'prepend', 'text', and 'postpend' nodes in the input
    XML file.  See base class for more details.
  """
  def __init__(self):
    """
      Initializes the GenericCode Interface.
      @ In, None
      @ Out, None
    """
    CodeInterfaceBase.__init__(self) # The base class doesn't actually implement this, but futureproofing.
    self.inputExtensions  = []       # list of extensions for RAVEN to edit as inputs
    self.outputExtensions = []       # list of extensions for RAVEN to gather data from?
    self.execPrefix       = ''       # executioner command prefix (e.g., 'python ')
    self.execPostfix      = ''       # executioner command postfix (e.g. -zcvf)
    self.caseName         = None     # base label for outgoing files, should default to inputFileName

  def generateCommand(self,inputFiles,executable,clargs=None, fargs=None):
    """
      See base class.  Collects all the clargs and the executable to produce the command-line call.
      Returns tuple of commands and base file name for run.
      Commands are a list of tuples, indicating parallel/serial and the execution command to use.
      @ In, inputFiles, list, List of input files (lenght of the list depends on the number of inputs have been added in the Step is running this code)
      @ In, executable, string, executable name with absolute path (e.g. /home/path_to_executable/code.exe)
      @ In, clargs, dict, optional, dictionary containing the command-line flags the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 i0extension =0 .inp0/ >< /Code >)
      @ In, fargs, dict, optional, a dictionary containing the axuiliary input file variables the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 aux0extension =0 .aux0/ >< /Code >)
      @ Out, returnCommand, tuple, tuple containing the generated command. returnCommand[0] is the command to run the code (string), returnCommand[1] is the name of the output root
    """
    if clargs==None:
      raise IOError('No input file was specified in clargs!')
    #check for output either in clargs or fargs
    #if len(fargs['output'])<1 and 'output' not in clargs.keys():
    #  raise IOError('No output file was specified, either in clargs or fileargs!')
    #check for duplicate extension use
    usedExt=[]
    for ext in list(clargs['input'][flag] for flag in clargs['input'].keys()) + list(fargs['input'][var] for var in fargs['input'].keys()):
      if ext not in usedExt:
        usedExt.append(ext)
      else:
        raise IOError('GenericCodeInterface cannot handle multiple input files with the same extension.  You may need to write your own interface.')

    #check all required input files are there
    inFiles=inputFiles[:]
    for exts in list(clargs['input'][flag] for flag in clargs['input'].keys()) + list(fargs['input'][var] for var in fargs['input'].keys()):
      for ext in exts:
        found=False
        for inf in inputFiles:
          if '.'+inf.getExt() == ext:
            found=True
            inFiles.remove(inf)
            break
        if not found:
          raise IOError('input extension "'+ext+'" listed in input but not in inputFiles!')
    #TODO if any remaining, check them against valid inputs

    #PROBLEM this is limited, since we can't figure out which .xml goes to -i and which to -d, for example.
    def getFileWithExtension(fileList,ext):
      """
      Just a script to get the file with extension ext from the fileList.
      @ In, fileList, the string list of filenames to pick from.
      @ Out, ext, the string extension that the desired filename ends with.
      """
      found = False
      for index,inputFile in enumerate(fileList):
        if inputFile.getExt() == ext:
          found=True
          break
      if not found:
        raise IOError('No InputFile with extension '+ext+' found!')
      return index,inputFile

    #prepend
    todo = ''
    todo += clargs['pre']+' '
    todo += executable
    index=None
    #inputs
    for flag,exts in clargs['input'].items():
      if flag == 'noarg':
        for ext in exts:
          idx,fname = getFileWithExtension(inputFiles,ext.strip('.'))
          todo+=' '+fname.getFilename()
          if index == None:
            index = idx
        continue
      todo += ' '+flag
      for ext in exts:
        idx,fname = getFileWithExtension(inputFiles,ext.strip('.'))
        todo+=' '+fname.getFilename()
        if index == None:
          index = idx
    #outputs
    #FIXME I think if you give multiple output flags this could result in overwriting
    self.caseName = inputFiles[index].getBase()
    outfile = 'out~'+self.caseName
    if 'output' in clargs.keys():
      todo+=' '+clargs['output']+' '+outfile
    #text flags
    todo+=' '+clargs['text']
    #postpend
    todo+=' '+clargs['post']
    returnCommand = [('parallel',todo)],outfile
    print('Execution Command: '+str(returnCommand[0]))
    return returnCommand

  def createNewInput(self,currentInputFiles,origInputFiles,samplerType,**Kwargs):
    """
      This method is used to generate an input based on the information passed in.
      @ In, currentInputFiles, list,  list of current input files (input files from last this method call)
      @ In, oriInputFiles, list, list of the original input files
      @ In, samplerType, string, Sampler type (e.g. MonteCarlo, Adaptive, etc. see manual Samplers section)
      @ In, Kwargs, dictionary, kwarded dictionary of parameters. In this dictionary there is another dictionary called "SampledVars"
            where RAVEN stores the variables that got sampled (e.g. Kwargs['SampledVars'] => {'var1':10,'var2':40})
      @ Out, newInputFiles, list, list of newer input files, list of the new input files (modified and not)
    """
    indexes=[]
    infiles=[]
    origfiles=[]
    #FIXME possible danger here from reading binary files
    for index,inputFile in enumerate(currentInputFiles):
      if inputFile.getExt() in self.getInputExtension():
        indexes.append(index)
        infiles.append(inputFile)
    for index,inputFile in enumerate(origInputFiles):
      if inputFile.getExt() in self.getInputExtension():
        origfiles.append(inputFile)
    parser = GenericParser.GenericParser(infiles)
    parser.modifyInternalDictionary(**Kwargs)
    parser.writeNewInput(currentInputFiles,origfiles)
    return currentInputFiles


  def finalizeCodeOutput(self, command, output, workDir):
    # filename would be 'publ_core.serpent'
    filename = command.strip().split(' ')[-1]
    # filename_without_extension would be 'publ_core'
    filename_without_extension = output.split('~')[1]
    # resfile would be 'publ_core.serpent_res.m'
    # this is the file produced by RAVEN
    resfile = os.path.join(workDir, filename+"_res.m")
    input_file = os.path.join(workDir, filename)
    inbumatfile = os.path.join(workDir, filename+".bumat0")
    outbumatfile = os.path.join(workDir, filename+".bumat1")
    # get the list of isotopes to track
    script_loc = os.path.dirname(os.path.realpath(sys.argv[0]))
    isofile = os.path.join(script_loc, 'CodeInterfaces/SERPENT/aux-input-files/iso_file')
    iso_list = op.read_file_into_list(isofile)
    # parse files into dictionary
    keff_dict = op.search_keff(resfile)
    # the second argument is the percent cutoff 
    in_bumat_dict = op.bumat_read(inbumatfile, 1e-7)
    out_bumat_dict = op.bumat_read(outbumatfile, 1e-7)

    output_path = os.path.join(workDir, output+'.csv')
    op.make_csv(output_path, in_bumat_dict, out_bumat_dict,
                keff_dict, iso_list, input_file)
