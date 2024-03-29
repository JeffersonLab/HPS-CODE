####################################################
# Python functions to support CODA scons build files
####################################################

import re, sys, glob, os, string, subprocess
from os import sep, symlink
from subprocess import Popen, PIPE

from SCons.Script  import Configure
from SCons.Builder import Builder

################
# File handling
################

def recursiveDirs(root) :
    """Return a list of all subdirectories of root, top down,
       including root, but without .svn directories"""
    return filter( (lambda a : (a.rfind( ".svn")==-1) and \
                               (a.rfind( ".Linux")==-1) and \
                               (a.rfind( ".SunOS")==-1) and \
                               (a.rfind( ".Darwin")==-1) and \
                               (a.rfind( ".vxworks")==-1)),  [ a[0] for a in os.walk(root)]  )



def unique(list) :
    """Remove duplicates from list"""
    return dict.fromkeys(list).keys()



def scanFiles(dir, accept=["*.cpp"], reject=[]) :
    """Return a list of selected files from a directory & its subdirectories"""
    sources = []
    paths = recursiveDirs(dir)
    for path in paths :
        for pattern in accept :
            sources+=glob.glob(path+"/"+pattern)
    for pattern in reject :
        sources = filter( (lambda a : a.rfind(pattern)==-1 ),  sources )
    return unique(sources)



def subdirsContaining(root, patterns):
    """Return a list of subdirectories containing files of the given pattern"""
    dirs = unique(map(os.path.dirname, scanFiles(root, patterns)))
    dirs.sort()
    return dirs



###################
# Operating System
###################

def CheckHas64Bits(context, flags):
    """Define configure-type test function to
       see if operating system is 64 or 32 bits"""
       
    context.Message( 'Checking for 64/32 bits ...' )
    lastCCFLAGS = context.env['CCFLAGS']
    lastLFLAGS  = context.env['LINKFLAGS']
    context.env.Append(CCFLAGS = flags, LINKFLAGS = flags)
    # (C) program to run to check for bits
    ret = context.TryRun("""
#include <stdio.h>
int main(int argc, char **argv) {
  printf(\"%d\", 8*sizeof(0L));
  return 0;
}
""", '.c')
    # Restore original flags
    context.env.Replace(CCFLAGS = lastCCFLAGS, LINKFLAGS = lastLFLAGS)
    # If program successfully ran ...
    if ret[0]:
        context.Result(ret[1])
        if ret[1] == '64':
            return 64
        return 32
    # Else if program did not run ...
    else:
        # Don't know if it's a 32 or 64 bit operating system
        context.Result('failed')
        return 0



def is64BitMachine(env, platform, machine):
    """Determine if machine has 64 or 32 bit architecture"""
    if platform == 'Linux'and machine == 'x86_64':
            return True
    else:
        ccflags = ''
        if platform == 'SunOS':
            ccflags = '-xarch=amd64'
        
        # Run the test
        conf = Configure( env, custom_tests = { 'CheckBits' : CheckHas64Bits } )
        ret = conf.CheckBits(ccflags)
        env = conf.Finish()
        if ret < 1:
            print 'Cannot run test, assume 32 bit system'
            return False
        elif ret == 64:
            # Test shows 64 bit system'
            return True
        else:
            # Test shows 32 bit system'
            return False



def configure32bits(env, use32bits, platform):
    """Setup environment on 64 bit machine to handle 32 or 64 bit libs and executables."""
    if platform == 'SunOS':
        if not use32bits:
            if machine == 'sun4u':
                env.Append(CCFLAGS =   ['-xarch=native64', '-xcode=pic32'],
                           LINKFLAGS = ['-xarch=native64', '-xcode=pic32'])
            else:
                env.Append(CCFLAGS =   ['-xarch=amd64'],
                           LINKFLAGS = ['-xarch=amd64'])

    elif platform == 'Darwin':
        if not use32bits:
            env.Append(CCFLAGS =   ['-arch','x86_64','-arch','i386'],
                       LINKFLAGS = ['-arch','x86_64','-arch','i386','-Wl', '-bind_at_load'])

    elif platform == 'Linux':
        if use32bits:
            env.Append(CCFLAGS = ['-m32'], LINKFLAGS = ['-m32'])

    return



def configureVxworks(env, vxVersion, platform):
    """Setup everything for vxWorks cross compilation."""
    ## Figure out which version of vxworks is being used.
    ## Do this by finding out which ccppc is first in our PATH.
    #vxCompilerPath = Popen('which ccppc', shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
    
    ## Then ty to grab the major version number from the PATH
    #matchResult = re.match('/site/vxworks/(\\d).+', vxCompilerPath)
    #if matchResult != None:
        ## Test if version number was obtained
        #try:
            #vxVersion = int(matchResult.group(1))
        #except IndexError:
            #print 'ERROR finding vxworks version, set to 6 by default\n'
    
    vxInc = ''

    if vxVersion == 5.5:
        vxbase = '/site/vxworks/5.5/ppc'
        vxInc  = [vxbase + '/target/h']
        env.Append(CPPDEFINES = ['VXWORKS_5'])
    elif vxVersion == 6.0:
        vxbase = '/site/vxworks/6.0/ppc/gnu/3.3.2-vxworks60'
        vxInc  = ['/site/vxworks/6.0/ppc/vxworks-6.0/target/h',
                  '/site/vxworks/6.0/ppc/vxworks-6.0/target/h/wrn/coreip']
        env.Append(CPPDEFINES = ['VXWORKS_6'])
    else:
        print 'Unknown version of vxWorks, exiting'
        return 0


    if platform == 'Linux':
        if vxVersion == 5.5:
            vxbin = vxbase + '/host/x86-linux/bin/'
        else:
            vxbin = vxbase + '/x86-linux2/bin/'
    elif platform == 'SunOS':
        if vxVersion >= 6:
            print '\nVxworks 6.x compilation not allowed on solaris'
            return 0
        vxbin = vxbase + '/host/sun4-solaris2/bin/'
        if machine == 'i86pc':
            print '\nVxworks compilation not allowed on x86 solaris'
            return 0
    else:
        print '\nVxworks compilation not allowed on ' + platform
        return 0
        
                    
    # If the supplied vxworks path is bad, rely
    # on the PATH to find vxworks executables
    if not os.path.exists(vxbin):
        vxbin = ''
    

    env.Replace(SHLIBSUFFIX = '.o')
    # Get rid of -shared and use -r
    env.Replace(SHLINKFLAGS = '-r')
    # Redefine SHCFLAGS/SHCCFLAGS to get rid of -fPIC (in Linux)
    vxFlags = '-fno-builtin -fvolatile -fstrength-reduce -mlongcall -mcpu=604'
    env.Replace(SHCFLAGS  = vxFlags)
    env.Replace(SHCCFLAGS = vxFlags)
    env.Append(CFLAGS     = vxFlags)
    env.Append(CCFLAGS    = vxFlags)
    env.Append(CPPPATH    = vxInc)
    env.Append(CPPDEFINES = ['CPU=PPC604', 'VXWORKS', '_GNU_TOOL', 'VXWORKSPPC', 'POSIX_MISTAKE', 'NO_RW_LOCK'])
    env['CC']     = vxbin + 'ccppc'
    env['CXX']    = vxbin + 'g++ppc'
    env['SHLINK'] = vxbin + 'ldppc'
    env['AR']     = vxbin + 'arppc'
    env['RANLIB'] = vxbin + 'ranlibppc'
    
    return 1



###########################
# Installation Directories
###########################

def getInstallationDirs(osname, prefix, incdir, libdir, bindir):
    """Determine installation directories."""
    
    # Get CODA env variable if any         
    codaHomeEnv = os.getenv('CODA','')
    
    # The installation directory is the user-specified "prefix"
    # by first choice, "CODA" secondly.
    # Any user specified command line installation path overrides default
    if (prefix == None) or (prefix == ''):
        # prefix not defined try CODA env var
        if codaHomeEnv == "":
            if (incdir == None) or (libdir == None) or (bindir == None):
                print "\nNeed to define CODA, or use the --prefix option,"
                print "or all the --incdir, --libdir, and --bindir options.\n"
                raise SystemExit
        else:
            prefix = codaHomeEnv
    
    osDir = prefix + "/" + osname
    
    # Set our install directories
    if incdir != None:
        incDir = incdir
        archIncDir = incdir
    else:
        incDir = prefix + '/common/include'
        archIncDir = osDir + '/include'
    
    if libdir != None:
        libDir = libdir
    else:
        libDir = osDir + '/lib'
    
    if bindir != None:
        binDir = bindir
    else:
        binDir = osDir + '/bin'
    
    # Return absolute paths in list
    return [os.path.abspath(prefix),
            os.path.abspath(osDir),
            os.path.abspath(incDir),
            os.path.abspath(archIncDir),
            os.path.abspath(libDir),
            os.path.abspath(binDir)]



###########################
# Include File Directories
###########################

def makeIncludeDirs(includeDir, archIncludeDir, archDir):
    """Function to make include directories"""
    #
    # Create main include dir if it doesn't exist
    #
    if not os.path.exists(includeDir):
        os.makedirs(includeDir)
    # Make sure it's a directory (if we didn't create it)
    elif not os.path.isdir(includeDir):
        print
        print "Error:", includeDir, "is NOT a directory"
        print
        raise SystemExit

    if includeDir == archIncludeDir:
        return

    #
    # If an install has never been done, the arch dir needs
    # to be made first so the symbolic link can be created.
    #
    if not os.path.exists(archDir):
        try:
            os.makedirs(archDir)
        except OSError:
            return
    elif not os.path.isdir(archDir):
        print
        print "Error:", archDir, "is NOT a directory"
        print
        raise SystemExit

    #
    # If the architecture include dir does NOT exist,
    # make link to include dir
    #
    if not os.path.exists(archIncludeDir):
        # Create symbolic link: symlink(source, linkname)
        try:
            symlink(includeDir, archIncludeDir)
        except OSError:
            # Failed to create symbolic link, so
            # just make it a regular directory
            os.makedirs(archIncludeDir)
    elif not os.path.isdir(archIncludeDir):
        print
        print "Error:", archIncludeDir, "is NOT a directory"
        print
        raise SystemExit

    return


 
###########
# JAVA JNI
###########

def configureJNI(env):
    """Configure the given environment for compiling Java Native Interface
       c or c++ language files."""

    # first look for a shell variable called JAVA_HOME
    java_base = os.environ.get('JAVA_HOME')
    if not java_base:
        if sys.platform == 'darwin':
            # Apple's OS X has its own special java base directory
            java_base = '/System/Library/Frameworks/JavaVM.framework'
        else:
            # Search for the java compiler
            print "JAVA_HOME environment variable not set. Searching for javac to find jni.h ..."
            if not env.get('JAVAC'):
                print "The Java compiler must be installed and in the current path, exiting"
                return 0
            jcdir = os.path.dirname(env.WhereIs('javac'))
            if not jcdir:
                print "   not found, exiting"
                return 0
            # assuming the compiler found is in some directory like
            # /usr/jdkX.X/bin/javac, java's home directory is /usr/jdkX.X
            java_base = os.path.join(jcdir, "..")
            print "  found, dir = " + java_base        
        
    if sys.platform == 'darwin':
        # Apple does not use Sun's naming convention
        java_headers = [os.path.join(java_base, 'include'),os.path.join(java_base, 'include/darwin')]
        java_libs = [os.path.join(java_base, 'lib')]
    else:
        # linux
        java_headers = [os.path.join(java_base, 'include')]
        java_libs = [os.path.join(java_base, 'lib')]
        # Sun's windows and linux JDKs keep system-specific header
        # files in a sub-directory of include
        if java_base == '/usr' or java_base == '/usr/local':
            # too many possible subdirectories. Just use defaults
            java_headers.append(os.path.join(java_headers[0], 'linux'))
            java_headers.append(os.path.join(java_headers[0], 'solaris'))
        else:
            # add all subdirs of 'include'. The system specific headers
            # should be in there somewhere
            java_headers = recursiveDirs(java_headers[0])

    # add Java's include and lib directory to the environment
    env.Append(CPPPATH = java_headers)
    # (only need the headers right now so comment out next line)
    #env.Append(LIBPATH = java_libs)

    # add any special platform-specific compilation or linking flags
    # (only need the headers right now so comment out next lines)
    #if sys.platform == 'darwin':
    #    env.Append(SHLINKFLAGS = '-dynamiclib -framework JavaVM')
    #    env['SHLIBSUFFIX'] = '.jnilib'

    # Add extra potentially useful environment variables
    #env['JAVA_HOME']   = java_base
    #env['JNI_CPPPATH'] = java_headers
    #env['JNI_LIBPATH'] = java_libs

    return 1




###################
# Documentation
###################

def generateDocs(env, doC=False, doCPP=False, doJava=False, javaDir=''):
    """Generate and install generated documentation (doxygen & javadoc)."""

    if doC:
        # Function that does the documentation creation
        def docGeneratorC(target, source, env):
            cmd = 'doxygen doc/doxygen/DoxyfileC'
            pipe = Popen(cmd, shell=True, env={"TOPLEVEL": "./"}, stdout=PIPE).stdout
            return
            
        # Doc files builders
        docBuildC = Builder(action = docGeneratorC)
        env.Append(BUILDERS = {'DocGenC' : docBuildC})
        
        # Generate documentation
        env.Alias('doc', env.DocGenC(target = ['#/doc/doxygen/C/html/index.html'],
              source = scanFiles("src/libsrc", accept=["*.[ch]"]) ))
    
    
    if doCPP:
        def docGeneratorCC(target, source, env):
            cmd = 'doxygen doc/doxygen/DoxyfileCC'
            pipe = Popen(cmd, shell=True, env={"TOPLEVEL": "./"}, stdout=PIPE).stdout
            return
        
        docBuildCC = Builder(action = docGeneratorCC)
        env.Append(BUILDERS = {'DocGenCC' : docBuildCC})
        
        env.Alias('doc', env.DocGenCC(target = ['#/doc/doxygen/CC/html/index.html'],
              source = scanFiles("src/libsrc++", accept=["*.[ch]", "*.cc", "*.hxx"]) ))
    
    
    if doJava:
        def docGeneratorJava(target, source, env):
            cmd = 'ant javadoc'
            output = os.popen(cmd).read()
            return
        
        docBuildJava = Builder(action = docGeneratorJava)
        env.Append(BUILDERS = {'DocGenJava' : docBuildJava})
        
        env.Alias('doc', env.DocGenJava(target = ['#/doc/javadoc/index.html'],
            source = scanFiles(javaDir, accept=["*.java"]) ))
    
    return 1




def removeDocs(env):
    """Remove all generated documentation (doxygen & javadoc)."""

    def docRemover(target, source, env):
        cmd = 'rm -fr doc/javadoc doc/doxygen/C doc/doxygen/CC'
        output = os.popen(cmd).read()
        return
    
    docRemoveAll = Builder(action = docRemover)
    env.Append(BUILDERS = {'DocRemove' : docRemoveAll})
    
    # remove documentation
    env.Alias('undoc', env.DocRemove(target = ['#/.undoc'], source = None))
    
    return 1



###################
# Tar file
###################

def generateTarFile(env, baseName, majorVersion, minorVersion):
    """Generate a gzipped tar file of the current directory."""
                
    # Function that does the tar. Note that tar on Solaris is different
    # (more primitive) than tar on Linux and MacOS. Solaris tar has no -z option
    # and the exclude file does not allow wildcards. Thus, stick to Linux for
    # creating the tar file.
    def tarballer(target, source, env):
        dirname = os.path.basename(os.path.abspath('.'))
        cmd = 'tar -X tar/tarexclude -C .. -c -z -f ' + str(target[0]) + ' ./' + dirname
        pipe = Popen(cmd, shell=True, stdin=PIPE).stdout
        return pipe

    # name of tarfile (software package dependent)
    tarfile = 'tar/' + baseName + '-' + majorVersion + '.' + minorVersion + '.tgz'

    # Use a Builder instead of env.Tar() since I can't make that work.
    # It runs into circular dependencies since we copy tar file to local
    # ./tar directory
    tarBuild = Builder(action = tarballer)
    env.Append(BUILDERS = {'Tarball' : tarBuild})
    env.Alias('tar', env.Tarball(target = tarfile, source = None))

    return 1
