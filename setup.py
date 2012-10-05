from distutils.core import setup, Extension

pkg = 'Extensions.SystemTools'
setup (name = 'enigma2-plugin-extensions-SystemTools',
       version = '0.1',
       description = 'SystemTools for enigma2 stb',
       packages = [pkg],
       package_dir = {pkg: 'plugin'},
      )
