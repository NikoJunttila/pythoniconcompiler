from cx_Freeze import setup, Executable

setup(
    name="icon-compiler",
    version="1.0",
    description="Make huge icon sets into a smaller folder",
    executables=[Executable("copyfiles.py")]
)