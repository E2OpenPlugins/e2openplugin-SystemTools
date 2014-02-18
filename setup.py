from distutils.core import setup, Extension

pkg = 'Extensions.SystemTools'
setup (name = 'enigma2-plugin-extensions-systemtools',
       version = '0.4',
       description = 'SystemTools for enigma2 stb',
       packages = [pkg],
       package_dir = {pkg: 'plugin'},
       package_data = {pkg: ['memorysimple.sh']},
      )
