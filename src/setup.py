from cx_Freeze import setup, Executable

#To build: "python setup.py build"

setup(name = "KiCad Annotator" ,
      version = "0.2" ,
      description = "Annotates sch files, grouping by type, value, footprint, and sheet." ,
      options = {
            "build_exe" : {
                  "build_exe":"../build/",
                  "optimize" : 2,
            },
      },
      executables = [
            Executable("ComponentSorter.py", base="Win32GUI")
      ]
)
